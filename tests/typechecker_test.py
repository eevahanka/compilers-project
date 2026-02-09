from compiler.tokenizer import tokenize
from compiler.token import Token
from compiler.token_location import Location
from compiler.typecheck import typecheck
from compiler.types import Type, FunType
from compiler.parser import parse
import compiler.ast as ast
import pytest
from compiler.compiler import compile

L = Location(1,1, True)

def testtest():
    c = compile('1 - 3')
    assert c ==0

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

def test_typecheck_assigmenr():
    tokens = tokenize('{var x = 1;x = 2}')
    parsed = parse(tokens)
    assert(typecheck(parsed) == Type('Int'))