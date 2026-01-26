from typing import Any
from compiler import ast
from compiler.symtab import SymTab, create_global_symtab

type Value = int | bool | None

def interpret(node: ast.Expression, symtab: SymTab | None = None) -> Value:
    if symtab is None:
        symtab = create_global_symtab()
    
    match node:
        case ast.Literal():
            return node.value

        case ast.BinaryOp():
            # Special handling for short-circuiting operators
            if node.op == "and":
                a: Any = interpret(node.left, symtab)
                if not a:
                    return False
                b: Any = interpret(node.right, symtab)
                return bool(b)
            elif node.op == "or":
                a: Any = interpret(node.left, symtab)
                if a:
                    return True
                b: Any = interpret(node.right, symtab)
                return bool(b)
            else:
                # Normal binary operators: evaluate both operands
                a: Any = interpret(node.left, symtab)
                b: Any = interpret(node.right, symtab)
                operator = symtab.lookup(node.op)
                if callable(operator):
                    return operator(a, b)
                else:
                    raise ValueError(f"Operator {node.op} is not callable")

        case ast.IfExpression():
            if interpret(node.condition, symtab):
                return interpret(node.then_branch, symtab)
            else:
                return interpret(node.else_branch, symtab)
        
        case ast.Identifier():
            value = symtab.lookup(node.name)
            return value
        
        case ast.VariableDeclaration():
            value = interpret(node.value, symtab)
            # Check if the variable already exists (is being reassigned)
            try:
                symtab.lookup(node.name)
                # Variable exists, so update it
                symtab.set(node.name, value)
            except NameError:
                # Variable doesn't exist, so define it
                symtab.define(node.name, value)
            return value
        
        case ast.Block():
            # Create a new child scope for the block
            child_symtab = symtab.create_child()
            result: Value = None
            for statement in node.statements:
                result = interpret(statement, child_symtab)
            return result
        
        case _:
            raise ValueError(f"Unknown node type: {type(node)}")