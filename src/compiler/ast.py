from dataclasses import dataclass
from .token_location import Location

@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""
    location: Location

@dataclass
class Literal(Expression):
    value: int | bool

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""
    left: Expression
    op: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    op: str
    operand: Expression

@dataclass
class IfExpression(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression | None

@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: list[Expression]