import compiler.ast as ast
from compiler.types import Type
from compiler.symtab import TypeSymTab, create_global_symtab

# Define built-in types
Bool = Type('Bool')
Int = Type('Int')
Unit = Type('Unit')

def is_integer(num):
    return isinstance(num, int)

def is_boolean(a):
    return isinstance(a, bool)

def create_global_type_symtab() -> TypeSymTab:
    """Create a global symbol table with built-in types for operators."""
    symtab = TypeSymTab()
    return symtab

def typecheck(node: ast.Expression, symtab: TypeSymTab | None = None) -> Type:
    """Typecheck an AST node and return its type."""
    if symtab is None:
        symtab = create_global_type_symtab()
    print(node)
    match node:
        case ast.BinaryOp():
            t1 = typecheck(node.left, symtab) 
            t2 = typecheck(node.right, symtab)
            print(t1)
            print(t2)
            if node.op in ['+', '-', '*', '/', '%']:
                if t1 is not Int or t2 is not Int:
                    raise Exception(f'{node.location}: {node.op} expected Integers, instead got {t1} and {t2} ')
                return Int
            elif node.op in ['<', '>', '<=', '>=']:
                if t1 is not Int or t2 is not Int:
                    raise Exception(f'{node.location}: {node.op} expected Integers, instead got {t1.type} and {t2.type} ')
                return Bool
            elif node.op in ['==', '!=']:
                if t1 != t2:
                    raise Exception(f'{node.location}: {node.op} expected same types, instead got {t1.type} and {t2.type} ')
                return Bool
            elif node.op in ['and', 'or']:
                if t1 is not Bool or t2 is not Bool:
                    raise Exception(f'{node.location}: {node.op} expected Booleans, instead got {t1.type} and {t2.type} ')
                return Bool
            else:
                raise Exception(f'{node.location}: unknown op {node.op}')
        
        case ast.Identifier():
            # Look up variable type in the symbol table
            try:
                return symtab.lookup(node.name)
            except NameError:
                raise Exception(f'{node.location}: undefined variable {node.name}')
            
        case ast.Literal():
            value = node.value
            if not is_integer(value):
                raise Exception(f'{node.location}: {node} expected Integer or bool, got {type(value)}')
            elif is_boolean(value):
                return Bool
            elif is_integer(value):
                print(value)
                return Int
        
        case ast.IfExpression():
            t1 = typecheck(node.condition, symtab)
            if t1 != Bool:
                raise Exception(f'{node.location}: if condition must be Bool, got {t1.type}')
            
            t2 = typecheck(node.then_branch, symtab)
            t3 = typecheck(node.else_branch, symtab) if node.else_branch else Unit
            
            if t2 != t3:
                raise Exception(f'{node.location}: then and else branches have different types: {t2.type} vs {t3.type}')
            return t2
        
        case ast.VariableDeclaration():
            # vast untyped declaration
            value_type = typecheck(node.value, symtab)
            symtab.define(node.name, value_type)
            return value_type
        
        case ast.Block():
            # Create a new child scope for the block
            child_symtab = symtab.create_child()
            result_type: Type = Unit
            for statement in node.statements:
                result_type = typecheck(statement, child_symtab)
            return result_type
        
        case ast.UnaryOp():
            t1 = typecheck(node.operand)
            if node.op not in ['-', 'not']:
                raise Exception(f'{node.location}: unknown unary operator: {node.op}')
            elif node.op == '-':
                #int int
                if t1 != Int:
                    raise Exception(f'{node.location}: the operand needs to be Int: {t1}')
                return Int
            elif node.op == 'not':
                if t1 != Bool:
                    raise Exception(f'{node.location}: the operand needs to be Bool: {t1}')
                return Bool 
        
        case ast.FunctionCall():
            ...

        case ast.Assignment():
            value = node.value
            variable_type = typecheck(node.name, symtab)
            value_type = typecheck(node.value, symtab)
            if variable_type != value_type:
                raise Exception(f'{node.location}: the assigned value ({value_type}) must have the same type as the variable ({variable_type}) ')
            return variable_type

        case _:
            raise Exception(f'{node.location}: unknown node type: {type(node)}')

