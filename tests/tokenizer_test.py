from compiler.tokenizer import tokenize
from compiler.token import Token
from compiler.token_location import Location

L = Location(1,1, True)

def test_tokenizer_basics() -> None:
    token1 = Token('if', 'identifier', L)
    token2 = Token('3', 'integer', L)
    token3 = Token('while', 'identifier', L)
    assert tokenize("if  3\nwhile") == [token1, token2, token3]

def test_location():
    token1 = Token('if', 'identifier', Location(1,1))
    token2 = Token('3', 'integer', Location(1,5))
    token3 = Token('while', 'identifier', Location(2,1))
    assert tokenize("if  3\nwhile") == [token1, token2, token3]


def test_operators() -> None:
    token1 = Token('+', 'operator', L)
    token2 = Token('-', 'operator', L)
    token3 = Token('*', 'operator', L)
    token4 = Token('/', 'operator', L)
    token5 = Token('%', 'operator', L)
    token6 = Token('=', 'operator', L)
    assert tokenize("+-*/%=") == [token1, token2, token3, token4, token5, token6]


def test_multi_char_operators() -> None:
    token1 = Token('==', 'operator', L)
    token2 = Token('!=', 'operator', L)
    token3 = Token('<=', 'operator', L)
    token4 = Token('>=', 'operator', L)
    assert tokenize("==!=<=>=") == [token1, token2, token3, token4]


def test_punctuation() -> None:
    token1 = Token('(', 'punctuation', L)
    token2 = Token(')', 'punctuation', L)
    token3 = Token('{', 'punctuation', L)
    token4 = Token('}', 'punctuation', L)
    token5 = Token(',', 'punctuation', L)
    token6 = Token(';', 'punctuation', L)
    assert tokenize("(){},;") == [token1, token2, token3, token4, token5, token6]


def test_line_comment() -> None:
    token1 = Token('x', 'identifier', L)
    token2 = Token('y', 'identifier', L)
    assert tokenize("x // this is a comment\ny") == [token1, token2]


def test_hash_comment() -> None:
    token1 = Token('a', 'identifier', L)
    token2 = Token('b', 'identifier', L)
    assert tokenize("a # this is a comment\nb") == [token1, token2]


def test_mixed_tokens() -> None:
    token1 = Token('x', 'identifier', L)
    token2 = Token('=', 'operator', L)
    token3 = Token('5', 'integer', L)
    token4 = Token('+', 'operator', L)
    token5 = Token('3', 'integer', L)
    token6 = Token(';', 'punctuation', L)
    assert tokenize("x = 5 + 3;") == [token1, token2, token3, token4, token5, token6]

def test_multiline_comment() -> None:
    token1 = Token('print_int', 'identifier', Location(6,1))
    token2 = Token('(', 'punctuation', Location(6,10))
    token3 = Token('123', 'integer', Location(6,11))
    token4 = Token(')', 'punctuation', Location(6,14))
    assert tokenize('/*\nMany lines\nof comment\ntext.\n*/\nprint_int(123)\n/* Another\ncomment. */') == [token1, token2, token3, token4]

