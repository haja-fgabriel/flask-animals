from dataclasses import dataclass

@dataclass
class ImageDTO:
    data: bytes
    hash: bytes 

@dataclass
class AnimalDTO:
    name: str
    kind: str
    user: str