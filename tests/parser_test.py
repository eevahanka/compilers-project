from compiler.parser import parse
from compiler.tokenizer import tokenize
import compiler.ast as ast
import pytest


def test_parser():
    tokens = tokenize("2+3")
    print(parse(tokens))
    lit2 = ast.Literal(2)
    lit3 = ast.Literal(3)
    ast1 = ast.BinaryOp(lit2,'+',lit3)
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
    assert(parse(tokens) == None)

def test_parcer_ifthen():
    tokens = tokenize('if a then b + c')
    assert(parse(tokens) == None)

def test_parcer_if_part_of_another_expression():
    tokens = tokenize('1 + if true then 2 else 3')
    assert(parse(tokens) == None)
