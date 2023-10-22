from __future__ import annotations
import random
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Word


class Question:
    def __init__(self, words: List[Word]):
        self.word = random.choice(list(filter(lambda w: w.selected ,words)))
        self.form = random.choice(list(self.word.forms.keys()))
        self._on_answer = None

    def on_answer(self, cb):
        self._on_answer = cb

    def answer(self, answer: str):
        is_correct = self.word.forms[self.form] == answer
        if self._on_answer is not None:
            self._on_answer(is_correct)
        return is_correct

