from dataclasses import dataclass


@dataclass
class Receipt:
    name: str
    total: float