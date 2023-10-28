from __future__ import annotations
from typing import Callable
from dataclasses import dataclass
from core.question import Question

@dataclass
class State:
    answered: int = 0
    success: int = 0

class Round:
    def __init__(self, question_factory: Callable[[], Question],
                 nb_question: int = 1,
                 ):
        self.state = State()
        self._question_factory = question_factory
        self.questions = [self._create_question() for _ in range(nb_question)]

    def _create_question(self):
        question = self._question_factory()
        question.on_answer(self._handle_answer)
        return question

    def _handle_answer(self, is_correct: bool, is_answered: bool, *args, **kwargs):
        if is_answered:
            return
        self.state.answered += 1
        if is_correct:
            self.state.success += 1

