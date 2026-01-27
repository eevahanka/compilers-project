from typing import Callable, TypeVar, Generic

type Value = int | bool | None | Callable

# Type variable for generic symbol table
T = TypeVar("T")

from .types import Type

class SymTab:
    """OLD OLD OLD OLD OLD OLD Hierarchical symbol table for managing variable scopes."""
    
    def __init__(self, parent: "SymTab | None" = None):
        """Initialize a new scope, optionally with a parent scope."""
        self.parent = parent
        self.symbols: dict[str, Value] = {}
    
    def declare_variable(self, name: str, value: Value) -> None:
        """Declare a variable with a given name and value."""
        self.define(name, value)

    def define(self, name: str, value: Value) -> None:
        """Define a variable in the current scope."""
        self.symbols[name] = value
    
    def lookup(self, name: str) -> Value:
        """Look up a variable, searching in current and parent scopes."""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Value) -> None:
        """Set a variable in the scope where it's defined."""
        
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent is not None:
            try:
                self.parent.set(name, value)
            except:
                self.parent.set(name, value)

        else:
            raise NameError(f"Undefined variable: {name}")
    
    def create_child(self) -> "SymTab":
        """Create a new child scope."""
        return SymTab(parent=self)

def create_global_symtab() -> SymTab:
    """Create a global symbol table with built-in operators and functions."""
    symtab = SymTab()    

    # Built-in binary operators
    symtab.define("+", lambda a, b: a + b)
    symtab.define("-", lambda a, b: a - b)
    symtab.define("<", lambda a, b: a < b)
    symtab.define(">", lambda a, b: a > b)
    symtab.define("<=", lambda a, b: a <= b)
    symtab.define(">=", lambda a, b: a >= b)
    symtab.define("==", lambda a, b: a == b)
    symtab.define("!=", lambda a, b: a != b)
    symtab.define("-", lambda a, b: a - b)
    symtab.define("*", lambda a, b: a * b)
    symtab.define("/", lambda a, b: a / b)
    symtab.define("%", lambda a, b: a % b)
    
    return symtab


class SymTable(Generic[T]):
    """Generic hierarchical symbol table for mapping names to values of type T."""
    
    def __init__(self, parent: "SymTable[T] | None" = None):
        """Initialize a new scope, optionally with a parent scope."""
        self.parent = parent
        self.symbols: dict[str, T] = {}
    
    def declare_variable(self, name: str, value: T) -> None:
        """Declare a variable with a given name and value."""
        self.define(name, value)

    def define(self, name: str, value: T) -> None:
        """Define a variable in the current scope."""
        self.symbols[name] = value
    
    def lookup(self, name: str) -> T:
        """Look up a variable, searching in current and parent scopes."""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: T) -> None:
        """Set a variable in the scope where it's defined."""
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent is not None:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")
    
    def create_child(self) -> "SymTable[T]":
        """Create a new child scope."""
        return SymTable(parent=self)


class TypeSymTab(SymTable[Type]):
    """Hierarchical symbol table for mapping variable names to types."""
    pass
