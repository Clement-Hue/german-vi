from dataclasses import dataclass

@dataclass
class State:
    nb_question: int = 0
    answered: int = 0
    success: int = 0


