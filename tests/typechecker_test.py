from compiler.tokenizer import tokenize
from compiler.token import Token
from compiler.token_location import Location
from compiler.typecheck import typecheck
from compiler.types import Type, FunType
from compiler.parser import parse
import compiler.ast as ast
import pytest

L = Location(1,1, True)

def test_typecheck():
    tokens = tokenize("2+3")
    parsed = parse(tokens)
    assert(typecheck(parsed) == Type('Int'))

def test_typecheck_variable_definition():
    tokens = tokenize('{ var x = 1 + 2 }')
    parsed = parse(tokens)
    assert(typecheck(parsed) == Type('Int'))

def test_typecheck_blocks():
    tokens = tokenize('{ { var x = 1 } }')
    parsed = parse(tokens)
    assert(typecheck(parsed) == Type('Int'))

def test_typecheck_and():
    tokens = tokenize('True and True')
    parsed = parse(tokens)
    assert(typecheck(parsed) == Type('Bool'))
