from dataclasses import dataclass

@dataclass
class State:
    tries: int = 0
    answered: int = 0
    success: int = 0


