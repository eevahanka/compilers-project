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
        return ast.Literal(int(token.text), token.location)

    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception(f'{peek().location}: expected an identifier')
        token = consume()
        return ast.Identifier(token.location, token.text)

    def parse_term() -> ast.Expression:
    # Same structure as in 'parse_expression',
    # but the operators and function calls differ.
        left = parse_factor()
        while peek().text in ['*', '/']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(
                operator_token.location,
                left,
                operator,
                right
            )
        return left

    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == 'if':
            return parse_if_expression()
        elif peek().type == 'int_literal':
            return parse_int_literal()
        elif peek().type == 'identifier':
            return parse_identifier()
        else:
            raise Exception(f'{peek().location}: expected "(", "if", an integer literal or an identifier')

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        # Recursively call the top level parsing function
        # to parse whatever is inside the parentheses.
        expr = parse_expression()
        consume(')')
        return expr

    def parse_if_expression() -> ast.Expression:
        consume('if')
        condition = parse_expression()
        consume('then')
        then_branch = parse_expression()
        
        # Check for optional else branch
        else_branch = None
        if peek().text == 'else':
            consume('else')
            else_branch = parse_expression()
        
        return ast.IfExpression(condition.location, condition, then_branch, else_branch)

    def parse_expression() -> ast.Expression:
        left = parse_term()

        # While there are more `+` or '-'...
        while peek().text in ['+', '-']:
            # Move past the '+' or '-'.
            operator_token = consume()
            operator = operator_token.text

            # Parse the operator on the right.
            right = parse_term()

            # Combine it with the stuff we've
            # accumulated on the left so far.
            left = ast.BinaryOp(
                operator_token.location,
                left,
                operator,
                right
            )
        return left


    parsed = parse_expression()
    if peek().type != 'end':
        raise Exception(f'{peek().location}: unexpected token "{peek().text}"')
    return parsed
