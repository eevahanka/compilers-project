from dataclasses import dataclass
from .token_location import Location

@dataclass
class Type:
    type: str

@dataclass
class FunType:
    parameters: (Type)
    returntype: Type