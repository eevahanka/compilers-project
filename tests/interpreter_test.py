# from compiler.interpreter import interpret
# from compiler.parser import parse
# from compiler.tokenizer import tokenize
# import compiler.ast as ast
# import pytest
# from compiler.token_location import Location
# from compiler.token import Token

# def test_interpreter():
#     tokens = tokenize("2+3")
#     parsed = parse(tokens)
#     assert(interpret(parsed) == 5)

# def test_interpreter_variable_definition():
#     tokens = tokenize('{ var x = 1 + 2 }')
#     parsed = parse(tokens)
#     assert(interpret(parsed) == 3)

# def test_interpreter_blocks():
#     tokens = tokenize('{ { var x = 1 } }')
#     parsed = parse(tokens)
#     assert(interpret(parsed) == 1)

# def test_interpreter_and():
#     tokens = tokenize('True and True')
#     parsed = parse(tokens)
#     assert(interpret(parsed) == True)

# def test_interpreter_and2():
#     tokens = tokenize('True and False')
#     parsed = parse(tokens)
#     assert(interpret(parsed) == False)

# def test_interpreter_and3():
#     tokens = tokenize('False and True')
#     parsed = parse(tokens)
#     assert(interpret(parsed) == False)

# # Short-circuiting tests for 'and' operator
# def test_short_circuit_and_false_left():
#     """Test that 'and' does not evaluate right side when left is false"""
#     code = '''
#     {
#         var evaluated_right_hand_side = False;
#         False and { evaluated_right_hand_side = True; True };
#         evaluated_right_hand_side
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     print(parsed)
#     result = interpret(parsed)
#     assert result == False, "Right side should not have been evaluated"

# def test_short_circuit_and_true_left():
#     """Test that 'and' evaluates right side when left is true"""
#     code = '''
#     {
#         var evaluated_right_hand_side = False;
#         True and { evaluated_right_hand_side = True; True };
#         evaluated_right_hand_side
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == True, "Right side should have been evaluated"

# # Short-circuiting tests for 'or' operator
# def test_short_circuit_or_true_left():
#     """Test that 'or' does not evaluate right side when left is true"""
#     code = '''
#     {
#         var evaluated_right_hand_side = False;
#         True or { evaluated_right_hand_side = True; True };
#         evaluated_right_hand_side
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == False, "Right side should not have been evaluated"

# def test_short_circuit_or_false_left():
#     """Test that 'or' evaluates right side when left is false"""
#     code = '''
#     {
#         var evaluated_right_hand_side = False;
#         False or { evaluated_right_hand_side = True; True };
#         evaluated_right_hand_side
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == True, "Right side should have been evaluated"

# # Additional short-circuit tests with function calls
# def test_short_circuit_and_with_side_effects():
#     """Test that function calls in right side are not executed when left is false"""
#     code = '''
#     {
#         var call_count = 0;
#         False and { call_count = call_count + 1; True };
#         call_count
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == 0, "Function in right side should not have been called"

# def test_short_circuit_or_with_side_effects():
#     """Test that function calls in right side are not executed when left is true"""
#     code = '''
#     {
#         var call_count = 0;
#         True or { call_count = call_count + 1; True };
#         call_count
#     }
#     '''
#     tokens = tokenize(code)
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == 0, "Function in right side should not have been called"

# def test_short_circuit_and_evaluates_when_needed():
#     """Test that both sides are evaluated for 'and' when result cannot be determined from left"""
#     tokens = tokenize('True and False')
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == False

# def test_short_circuit_or_evaluates_when_needed():
#     """Test that both sides are evaluated for 'or' when result cannot be determined from left"""
#     tokens = tokenize('False or True')
#     parsed = parse(tokens)
#     result = interpret(parsed)
#     assert result == True