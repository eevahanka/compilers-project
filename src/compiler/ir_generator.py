from compiler import ast, ir
from compiler.symtab import SymTable
from compiler.types import Bool, Int, Unit
from compiler.ir import IRVar
import compiler.ir


def generate_ir(
    # 'reserved_names' should contain all global names
    # like 'print_int' and '+'. You can get them from
    # the global symbol table of your interpreter or type checker.
    reserved_names: set[str],
    root_expr: ast.Expression
) -> list[ir.Instruction]:
    # 'var_unit' is used when an expression's type is 'Unit'.
    var_unit = IRVar('unit')

    def new_var() -> IRVar:
        # Create a new unique IR variable
        # Keep a counter and a set of used names (including reserved ones)
        if not hasattr(new_var, "_counter"):
            new_var._counter = 0  # type: ignore[attr-defined]
            # copy reserved names so we don't mutate caller's set
            new_var._used = set(reserved_names)  # type: ignore[attr-defined]
            new_var._used.add('unit')  # the unit variable name is reserved

        while True:
            new_var._counter += 1  # type: ignore[attr-defined]
            name = f"x{new_var._counter}"
            if name not in new_var._used:  # type: ignore[attr-defined]
                new_var._used.add(name)  # type: ignore[attr-defined]
                return IRVar(name)

    # We collect the IR instructions that we generate
    # into this list.
    ins: list[ir.Instruction] = []

    # This function visits an AST node,
    # appends IR instructions to 'ins',
    # and returns the IR variable where
    # the emitted IR instructions put the result.
    #
    # It uses a symbol table to map local variables
    # (which may be shadowed) to unique IR variables.
    # The symbol table will be updated in the same way as
    # in the interpreter and type checker.
    def visit(st: SymTable[IRVar], expr: ast.Expression) -> IRVar:
        loc = expr.location

        match expr:
            case ast.Literal():
                # Create an IR variable to hold the value,
                # and emit the correct instruction to
                # load the constant value.
                match expr.value:
                    case bool():
                        var = new_var()
                        ins.append(ir.LoadBoolConst(
                            loc, expr.value, var))
                    case int():
                        var = new_var()
                        ins.append(ir.LoadIntConst(
                            loc, expr.value, var))
                    case None:
                        var = var_unit
                    case _:
                        raise Exception(f"{loc}: unsupported literal: {type(expr.value)}")

                # Return the variable that holds
                # the loaded value.
                return var

            case ast.Identifier():
                # Look up the IR variable that corresponds to
                # the source code variable.
                return st.require(expr.name)

            case ast.BinaryOp():
                # Ask the symbol table to return the variable that refers
                # to the operator to call.
                var_op = st.require(expr.op)
                # Recursively emit instructions to calculate the operands.
                var_left = visit(st, expr.left)
                var_right = visit(st, expr.right)
                # Generate variable to hold the result.
                var_result = new_var()
                # Emit a Call instruction that writes to that variable.
                ins.append(ir.Call(
                    loc, var_op, [var_left, var_right], var_result))
                return var_result

            #... # Other AST node cases (see below)

    # We start with a SymTab that maps all available global names
    # like 'print_int' to IR variables of the same name.
    # In the Assembly generator stage, we will give
    # actual implementations for these globals. For now,
    # they just need to exist so the variable lookups work,
    # and clashing variable names can be avoided.
    root_symtab = SymTable[IRVar](parent=None)
    for name in reserved_names:
        root_symtab.add_local(name, IRVar(name))

    # Start visiting the AST from the root.
    var_final_result = visit(root_symtab, root_expr)

    # Add IR code to print the result, based on the type assigned earlier
    # by the type checker.
    if root_expr.type == Int:
        ... # Emit a call to 'print_int'
    elif root_expr.type == Bool:
        ... # Emit a call to 'print_bool'

    return ins
