from compiler.parser import parse
from compiler.tokenizer import tokenize
import compiler.ast as ast
import pytest
from compiler.token_location import Location
from compiler.token import Token

L = Location(3,2,True) #dummy location

def test_parser():
    tokens = tokenize("2+3")
    parse(tokens)
    lit2 = ast.Literal(L, 2)
    lit3 = ast.Literal(L, 3)
    ast1 = ast.BinaryOp(L, lit2, '+', lit3)
    assert(parse(tokens) == ast1)

def test_parcer_incorrect_input_errors():
    tokens = tokenize('2+4f')
    with pytest.raises(Exception):
        assert(parse(tokens) ==5 )

def test_parcer_empty_input():
    tokens = tokenize('')
    assert(parse(tokens) == None)

def test_parcer_another_incorrect_input():
    tokens = tokenize('2a+4')
    with pytest.raises(Exception):
        assert(parse(tokens) ==5 )

def test_parcer_ifthenelse():
    tokens = tokenize('if a then b + c else x * y')
    expected = ast.IfExpression(
        L,
        condition=ast.Identifier(L, 'a'),
        then_branch=ast.BinaryOp(L, ast.Identifier(L, 'b'), '+', ast.Identifier(L, 'c')),
        else_branch=ast.BinaryOp(L, ast.Identifier(L, 'x'), '*', ast.Identifier(L, 'y'))
    )
    print(expected)
    print(parse(tokens))
    assert(parse(tokens) == expected)

def test_parcer_ifthen():
    tokens = tokenize('if a then b + c')
    expected = ast.IfExpression(
        L,
        condition=ast.Identifier(L, 'a'),
        then_branch=ast.BinaryOp(L, ast.Identifier(L, 'b'), '+', ast.Identifier(L, 'c')),
        else_branch=None
    )
    assert(parse(tokens) == expected)

def test_parcer_if_part_of_another_expression():
    tokens = tokenize('1 + if true then 2 else 3')
    expected = ast.BinaryOp(
        location=L,
        left=ast.Literal(L, 1),
        op='+',
        right=ast.IfExpression(
            location=L,
            condition=ast.Identifier(L, 'true'),
            then_branch=ast.Literal(L, 2),
            else_branch=ast.Literal(L, 3),
        )
    )
    assert(parse(tokens) == expected)

def test_parcer_nested_if():
    tokens = tokenize('if a then if b then 1 else 2 else 3')
    expected = ast.IfExpression(
        L,
        condition=ast.Identifier(L, 'a'),
        then_branch=ast.IfExpression(
            L,
            condition=ast.Identifier(L, 'b'),
            then_branch=ast.Literal(L, 1),
            else_branch=ast.Literal(L, 2)
        ),
        else_branch=ast.Literal(L, 3)
    )
    assert(parse(tokens) == expected)

def test_parcer_locations():
    token1 = Token('print_int', 'identifier', Location(6,1))
    token2 = Token('(', 'punctuation', Location(6,10))
    token3 = Token('123', 'int_literal', Location(6,11))
    token4 = Token(')', 'punctuation', Location(6,14))
    tokens = [token1, token2, token3, token4]
    expected = ast.FunctionCall(Location(6,1), ast.Identifier(Location(6,1), 'print_int'), [ast.Literal(Location(6,11), 123)])
    assert (parse(tokenize('/*\nMany lines\nof comment\ntext.\n*/\nprint_int(123)\n/* Another\ncomment. */')) == expected)

def test_function_call_single_arg():
    tokens = tokenize('f(x)')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[ast.Identifier(L, 'x')]
    )
    assert result == expected

def test_function_call_multiple_args():
    tokens = tokenize('f(x, y)')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[
            ast.Identifier(L, 'x'),
            ast.Identifier(L, 'y')
        ]
    )
    assert result == expected

def test_function_call_with_expression():
    tokens = tokenize('f(x, y + z)')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[
            ast.Identifier(L, 'x'),
            ast.BinaryOp(L, ast.Identifier(L, 'y'), '+', ast.Identifier(L, 'z'))
        ]
    )
    assert result == expected

def test_function_call_no_args():
    tokens = tokenize('f()')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[]
    )
    assert result == expected

def test_function_call_complex_args():
    tokens = tokenize('f(a * b, c + d)')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[
            ast.BinaryOp(L, ast.Identifier(L, 'a'), '*', ast.Identifier(L, 'b')),
            ast.BinaryOp(L, ast.Identifier(L, 'c'), '+', ast.Identifier(L, 'd'))
        ]
    )
    assert result == expected

def test_function_call_in_expression():
    tokens = tokenize('f(x) + 2')
    result = parse(tokens)
    expected = ast.BinaryOp(
        L,
        left=ast.FunctionCall(
            L,
            function=ast.Identifier(L, 'f'),
            arguments=[ast.Identifier(L, 'x')]
        ),
        op='+',
        right=ast.Literal(L, 2)
    )
    assert result == expected

def test_nested_function_calls():
    tokens = tokenize('f(g(x))')
    result = parse(tokens)
    expected = ast.FunctionCall(
        L,
        function=ast.Identifier(L, 'f'),
        arguments=[
            ast.FunctionCall(
                L,
                function=ast.Identifier(L, 'g'),
                arguments=[ast.Identifier(L, 'x')]
            )
        ]
    )
    assert result == expected

def test_parcer_equals():
    tokens = tokenize('x=2')
    expected = ast.VariableDeclaration(L, 'x', ast.Literal(L, 2))
    assert parse(tokens) == expected

def test_parser_lt():
    tokens = tokenize('x <= 2')
    excpected = ast.BinaryOp(L, ast.Identifier(L, 'x'), '<=', ast.Literal(L, 2))
    assert parse(tokens) == excpected

def test_parser_unary():
    tokens = tokenize('-2')
    excpected = ast.UnaryOp(L, '-', ast.Literal(L, 2))
    assert parse(tokens) == excpected

def test_variable_declaration_simple():
    tokens = tokenize('{ var x = 123 }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.VariableDeclaration(L, 'x', ast.Literal(L, 123))
        ]
    )
    assert result == expected

def test_variable_declaration_with_expression():
    tokens = tokenize('{ var x = 1 + 2 }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.VariableDeclaration(
                L,
                'x',
                ast.BinaryOp(L, ast.Literal(L, 1), '+', ast.Literal(L, 2))
            )
        ]
    )
    assert result == expected

def test_multiple_variable_declarations():
    tokens = tokenize('{ var x = 1; var y = 2 }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.VariableDeclaration(L, 'x', ast.Literal(L, 1)),
            ast.VariableDeclaration(L, 'y', ast.Literal(L, 2))
        ]
    )
    assert result == expected

def test_block_with_expressions():
    tokens = tokenize('{ 1 + 2; x }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.BinaryOp(L, ast.Literal(L, 1), '+', ast.Literal(L, 2)),
            ast.Identifier(L, 'x')
        ]
    )
    assert result == expected

def test_variable_declaration_and_expression():
    tokens = tokenize('{ var x = 5; x + 1 }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.VariableDeclaration(L, 'x', ast.Literal(L, 5)),
            ast.BinaryOp(L, ast.Identifier(L, 'x'), '+', ast.Literal(L, 1))
        ]
    )
    assert result == expected

def test_block_as_expression_in_binary_op():
    tokens = tokenize('{ var x = 1 } + 2')
    result = parse(tokens)
    expected = ast.BinaryOp(
        L,
        left=ast.Block(
            L,
            statements=[
                ast.VariableDeclaration(L, 'x', ast.Literal(L, 1))
            ]
        ),
        op='+',
        right=ast.Literal(L, 2)
    )
    assert result == expected

def test_nested_blocks():
    tokens = tokenize('{ { var x = 1 } }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.Block(
                L,
                statements=[
                    ast.VariableDeclaration(L, 'x', ast.Literal(L, 1))
                ]
            )
        ]
    )
    assert result == expected

def test_empty_block():
    tokens = tokenize('{ }')
    result = parse(tokens)
    expected = ast.Block(L, statements=[])
    assert result == expected

def test_consecutive_blocks_allowed():
    """{ { a } { b } } should be allowed"""
    tokens = tokenize('{ { a } { b } }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.Block(L, statements=[ast.Identifier(L, 'a')]),
            ast.Block(L, statements=[ast.Identifier(L, 'b')])
        ]
    )
    assert result == expected

def test_consecutive_simple_expressions_not_allowed():
    """{ a b } should NOT be allowed"""
    tokens = tokenize('{ a b }')
    with pytest.raises(Exception, match='expected ";"'):
        parse(tokens)

def test_if_then_block_with_expression_allowed():
    """{ if true then { a } b } should be allowed"""
    tokens = tokenize('{ if true then { a } b }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.IfExpression(
                L,
                condition=ast.Identifier(L, 'true'),
                then_branch=ast.Block(L, statements=[ast.Identifier(L, 'a')]),
                else_branch=None
            ),
            ast.Identifier(L, 'b')
        ]
    )
    assert result == expected

def test_if_then_block_with_expression_and_semicolon_allowed():
    """{ if true then { a }; b } should be allowed"""
    tokens = tokenize('{ if true then { a }; b }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.IfExpression(
                L,
                condition=ast.Identifier(L, 'true'),
                then_branch=ast.Block(L, statements=[ast.Identifier(L, 'a')]),
                else_branch=None
            ),
            ast.Identifier(L, 'b')
        ]
    )
    assert result == expected

def test_if_then_two_expressions_not_allowed():
    """{ if true then { a } b c } should NOT be allowed"""
    tokens = tokenize('{ if true then { a } b c }')
    with pytest.raises(Exception, match='expected ";"'):
        parse(tokens)

def test_if_then_expression_semicolon_expression_allowed():
    """{ if true then { a } b; c } should be allowed"""
    tokens = tokenize('{ if true then { a } b; c }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.IfExpression(
                L,
                condition=ast.Identifier(L, 'true'),
                then_branch=ast.Block(L, statements=[ast.Identifier(L, 'a')]),
                else_branch=None
            ),
            ast.Identifier(L, 'b'),
            ast.Identifier(L, 'c')
        ]
    )
    assert result == expected

def test_if_then_else_block_with_expression_allowed():
    """{ if true then { a } else { b } c } should be allowed"""
    tokens = tokenize('{ if true then { a } else { b } c }')
    result = parse(tokens)
    expected = ast.Block(
        L,
        statements=[
            ast.IfExpression(
                L,
                condition=ast.Identifier(L, 'true'),
                then_branch=ast.Block(L, statements=[ast.Identifier(L, 'a')]),
                else_branch=ast.Block(L, statements=[ast.Identifier(L, 'b')])
            ),
            ast.Identifier(L, 'c')
        ]
    )
    assert result == expected

def test_assignment_with_consecutive_blocks_allowed():
    """x = { { f(a) } { b } } should be allowed"""
    tokens = tokenize('x = { { f(a) } { b } }')
    result = parse(tokens)
    expected = ast.VariableDeclaration(
        L,
        'x',
        ast.Block(
            L,
            statements=[
                ast.Block(
                    L,
                    statements=[
                        ast.FunctionCall(
                            L,
                            function=ast.Identifier(L, 'f'),
                            arguments=[ast.Identifier(L, 'a')]
                        )
                    ]
                ),
                ast.Block(L, statements=[ast.Identifier(L, 'b')])
            ]
        )
    )
    assert result == expected

def test_parser_true():
    tokens = tokenize('True')
    assert(parse(tokens) == ast.Literal(L, True))

def test_parser_false():
    tokens = tokenize('False')
    assert(parse(tokens) == ast.Literal(L, False))    
