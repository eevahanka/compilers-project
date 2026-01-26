import re
from .token import Token
from .token_location import Location

def tokenize(source_code: str) -> list[str]:
    identifier_regrex = r'[a-zA-Z_][a-zA-Z_0-9]*'
    integer_regrex = r'[0-9]+'
    bool_literal = r'(True)|(False)'
    operator_regrex = r'==|!=|<=|>=|[+\-*/%=<>]'
    punctuation_regrex = r'[(){},;]'
    whitespace_regrex = r'\s+'
    comment_regrex = r'//[^\n]*|#[^\n]*'
    multiline_comment_regrex = r'/\*[\s\S]*?\*/'
    tokens: list = []
    i = 0
    row = 1
    column = 1
    while i < len(source_code):
        current_token = re.match(bool_literal, source_code[i:])
        if current_token:
            loc = Location(row, column)
            token = Token(current_token.group(), "bool_literal", loc)
            tokens.append(token)
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(identifier_regrex, source_code[i:])
        if current_token:
            loc = Location(row, column)
            token = Token(current_token.group(), "identifier", loc)
            tokens.append(token)
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(integer_regrex, source_code[i:])
        if current_token:
            loc = Location(row, column)
            token = Token(current_token.group(), "int_literal", loc)
            tokens.append(token)
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(multiline_comment_regrex, source_code[i:])
        if current_token:
            for char in current_token.group():
                if char == '\n':
                    row += 1
                    column = 1
                else:
                    column += 1
            i += len(current_token.group())
        current_token = re.match(comment_regrex, source_code[i:])
        if current_token:
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(operator_regrex, source_code[i:])
        if current_token:
            loc= Location(row, column)
            token= Token(current_token.group(), "operator", loc)
            tokens.append(token)
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(punctuation_regrex, source_code[i:])
        if current_token:
            loc = Location(row, column)
            token= Token(current_token.group(), "punctuation", loc)
            tokens.append(token)
            i += len(current_token.group())
            column += len(current_token.group())
            continue
        current_token = re.match(whitespace_regrex, source_code[i:])
        if current_token:
            i += len(current_token.group())
            for char in current_token.group():
                if char == '\n':
                    row += 1
                    column = 1
                else:
                    column += 1
            continue
        current_token = re.match(comment_regrex, source_code[i:])
        if current_token:
            i += len(current_token.group())
            for char in current_token.group():
                if char == '\n':
                    row += 1
            column = 1
            continue
    print("got to the end, is this suppopsed yo happen??")
    i += 1
    return tokens

    
    

"pytest path/to/test_file.py::test_function_name"