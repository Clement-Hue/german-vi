from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
from dataclasses import dataclass
from core.question import Question
if TYPE_CHECKING:
    from core.word import Word

@dataclass
class State:
    answered: int = 0
    success: int = 0

class Round:
    def __init__(self, words: List[Word], nb_question: int = 1,
                 selected_forms: Callable[[List[str]], List[str]]  = None
                 ):
        self.nb_question = nb_question
        self.selected_forms = selected_forms
        self.state = State()
        self.words = words
        self.questions = [self._create_question() for _ in range(nb_question)]

    def _create_question(self):
        question = Question(words=self.words, selected_forms=self.selected_forms)
        question.on_answer(self._handle_answer)
        return question

    def _handle_answer(self, is_correct: bool, is_answered: bool, *args, **kwargs):
        if is_answered:
            return
        self.state.answered += 1
        if is_correct:
            self.state.success += 1

