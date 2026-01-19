from compiler.parser import parse
from compiler.tokenizer import tokenize
import compiler.ast as ast
import pytest
from compiler.token_location import Location

L = Location(3,2,True) #dummy location

def test_parser():
    tokens = tokenize("2+3")
    print(parse(tokens))
    lit2 = ast.Literal(2, L)
    lit3 = ast.Literal(3, L)
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
        left=ast.Literal(1, L),
        op='+',
        right=ast.IfExpression(
            location=L,
            condition=ast.Identifier(L, 'true'),
            then_branch=ast.Literal(2, L),
            else_branch=ast.Literal(3, L),
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
            then_branch=ast.Literal(1, L),
            else_branch=ast.Literal(2, L)
        ),
        else_branch=ast.Literal(3, L)
    )
    assert(parse(tokens) == expected)
