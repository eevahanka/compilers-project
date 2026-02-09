from dataclasses import dataclass
from .token_location import Location

@dataclass
class Type:
    type: str

@dataclass
class FunType:
    parameters: (Type)
    returntype: Type
    
    def __repr__(self) -> str:
        return "Unit"


# Primitive type singletons
Bool = Type('Bool')
Int = Type('Int')
Unit = Type('Unit')
