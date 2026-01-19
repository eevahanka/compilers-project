from dataclasses import dataclass
from .token_location import Location

@dataclass
class Token:
    text: str
    type: str
    location: Location