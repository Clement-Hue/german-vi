from __future__ import annotations
from typing import TYPE_CHECKING, List
from dataclasses import dataclass
from core.question import Question
if TYPE_CHECKING:
    from core.word import Word

@dataclass
class State:
    nb_question: int = 0
    answered: int = 0
    success: int = 0

class Round:
    def __init__(self,words: List[Word], nb_question: int = 1):
        self.state = State(nb_question)
        self.words = words

    def __bool__(self):
        """
        :return: True if the round is still on going
        """
        return self.state.answered < self.state.nb_question
    def create_question(self):
        question = Question(words=self.words)
        question.on_answer(self._handle_answer)
        return question

    def _handle_answer(self, is_correct: bool, *args):
        self.state.answered += 1
        if is_correct:
            self.state.success += 1
