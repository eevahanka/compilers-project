from compiler.token import Token
import compiler.ast as ast

def parse(tokens: list[Token]) -> ast.Expression:
    if not tokens:
        return None
    # This keeps track of which token we're looking at.
    pos = 0
    # 'peek()' returns the token at 'pos',
    # or a special 'end' token if we're past the end
    # of the token list.
    # This way we don't have to worry about going past
    # the end elsewhere.
    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(
                location=tokens[-1].location,
                type="end",
                text="",
            )

    # 'consume()' returns the token at 'pos'
    # and increments 'pos' by one.
    #
    # If the optional parameter 'expected' is given,
    # it checks that the token being consumed has that text.
    # If 'expected' is a list, then the token must have
    # one of the texts in the list.
    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos # Python'"nonlocal" lets us modify `pos`
                     # without creating a local variable of the same name.
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.location}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.location}: expected one of: {comma_separated}')
        pos += 1
        return token
    def parse_int_literal() -> ast.Literal:
        if peek().type != 'int_literal':
            raise Exception(f'{peek().location}: expected an integer literal')
        token = consume()
        return ast.Literal(token.location, int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type !='identifier':
            raise Exception(f'{peek().location}: expected an identifier')
        token = consume()
        return ast.Identifier(token.location, token.text)

    def parse_function_call(function: ast.Identifier) -> ast.FunctionCall:
        consume('(')
        arguments: list[ast.Expression] = []
        if peek().text != ')':
            arguments.append(parse_assignment())
            while peek().text == ',':
                consume(',')
                arguments.append(parse_assignment())
        
        consume(')')
        return ast.FunctionCall(function.location, function, arguments)

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        # Recursively call the top level pars function
        #  pars inside parentheses.
        expr = parse_assignment()
        consume(')')
        return expr

    def parse_if_expression() -> ast.Expression:
        consume('if')
        condition = parse_assignment()
        consume('then')
        then_branch = parse_assignment()
        
        # optional else branch
        else_branch = None
        if peek().text == 'else':
            consume('else')
            else_branch = parse_assignment()
        
        return ast.IfExpression(condition.location, condition, then_branch, else_branch)

    def parse_block() -> ast.Block:
        """Parse a block: { statement; statement; ... }"""
        block_location = peek().location
        consume('{')
        statements: list[ast.Expression] = []
        
        last_was_compound = True  
        
        while peek().text != '}':
            stmt = parse_statement()
            statements.append(stmt)
            is_compound = isinstance(stmt, (
                ast.IfExpression,
                ast.Block,
                ast.FunctionCall,
                ast.VariableDeclaration
            ))
            
            # Handle what comes next
            if peek().text == ';':
                consume(';')
                last_was_compound = True  
            elif peek().text != '}':
                if not is_compound:
                    raise Exception(
                        f'{peek().location}: expected ";" before this statement '
                        f'(previous statement was not compound)'
                    )
                last_was_compound = is_compound
            else:
                last_was_compound = is_compound
        
        consume('}')
        return ast.Block(block_location, statements)

    def parse_statement() -> ast.Expression:
        """Parse a statement, which can be a variable declaration or an expression."""
        if peek().text == 'var':
            return parse_variable_declaration()
        else:
            return parse_assignment()

    def parse_variable_declaration() -> ast.VariableDeclaration:
        """Parse a variable declaration: var name = value"""
        var_location = peek().location
        consume('var')
        
        if peek().type != 'identifier':
            raise Exception(f'{peek().location}: expected an identifier after "var"')
        name_token = consume()
        variable_name = name_token.text
        
        consume('=')
        
        value = parse_assignment()
        
        return ast.VariableDeclaration(var_location, variable_name, value)

    def parse_atom() -> ast.Expression:
        """Parse atomic expressions: literals, identifiers, if, parentheses, unary ops, blocks."""
        if peek().text in ['-', 'not']:
            operator_token = consume()
            operator = operator_token.text
            operand = parse_atom()  # Right-associative for unary operators
            return ast.UnaryOp(operator_token.location, operator, operand)
        
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == '{':
            return parse_block()
        elif peek().text == 'if':
            return parse_if_expression()
        elif peek().type == 'int_literal':
            return parse_int_literal()
        elif peek().type ==  'identifier':
            identifier = parse_identifier()
            #function call
            if peek().text == '(':
                return parse_function_call(identifier)
            return identifier
        else:
            raise Exception(f'{peek().location}: expected "(", "if", an integer literal, an identifier, a block, or a unary operator')

    left_associative_binary_operators = [
        ['='], # right-associative!!
        ['or'],
        ['and'],
        ['==', '!='],
        ['<', '<=', '>', '>='],
        ['+', '-'],
        ['*', '/', '%'],
    ]

    def parse_binary_op_level(level: int) -> ast.Expression:
        if level >= len(left_associative_binary_operators):
            return parse_atom()
        
        left = parse_binary_op_level(level + 1)
        
        operators_at_this_level = left_associative_binary_operators[level]
        
        #right-associative =
        if operators_at_this_level == ['=']:
            while peek().text == '=':
                operator_token = consume()
                operator = operator_token.text
                right = parse_binary_op_level(level)
                left = ast.BinaryOp(
                    operator_token.location,
                    left,
                    operator,
                    right
                )
        else:
            # left-associative operators
            while peek().text in operators_at_this_level:
                operator_token = consume()
                operator = operator_token.text
                right = parse_binary_op_level(level + 1)
                left = ast.BinaryOp(
                    operator_token.location,
                    left,
                    operator,
                    right
                )
        
        return left

    def parse_assignment() -> ast.Expression:
        """Entry point for expression parsing."""
        return parse_binary_op_level(0)

    parsed = parse_assignment()
    if peek().type != 'end':
        raise Exception(f'{peek().location}: unexpected token "{peek().text}"')
    return parsed
