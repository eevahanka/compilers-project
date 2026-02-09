from compiler.tokenizer import tokenize
from compiler.token import Token
from compiler.token_location import Location
from compiler.typecheck import typecheck
from compiler.types import Type, FunType
from compiler.parser import parse
import compiler.ast as ast
from compiler.ir_generator import generate_ir
from compiler.symtab import create_global_symtab


def compile(code):
    tokens = tokenize(code)
    parsed = parse(tokens)
    typecheck(parsed)
    # Provide the IR generator with known global names (operators, builtins)
    global_sym = create_global_symtab()
    reserved = set(global_sym.symbols.keys())
    # also reserve printing helpers
    reserved.update({'print_int', 'print_bool'})
    ir = generate_ir(reserved, parsed)
    print(ir)
    return ir