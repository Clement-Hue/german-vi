from __future__ import annotations
import random
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Word


class Question:
    def __init__(self, words: List[Word]):
        self.word = random.choice(words)
        self.form = random.choice(list(self.word.forms.keys()))
        self._on_answer = []
        self.is_answered = False

    def on_answer(self, cb):
        self._on_answer.append(cb)

    def answer(self, answer: str):
        correct_answer = self.word.forms[self.form]
        is_correct = correct_answer == answer
        for on_answer in self._on_answer:
            on_answer(is_correct=is_correct, correct_answer=correct_answer, answer=answer, is_answered=self.is_answered)
        self.is_answered = True
        return is_correct

