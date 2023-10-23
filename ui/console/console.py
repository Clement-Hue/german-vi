from __future__ import annotations
from typing import TYPE_CHECKING
from ui.application import Application
if TYPE_CHECKING:
    from core.game import Game

colors = {
    "blue": '\033[94m',
    "reset": '\033[0m',
    "green": '\033[92m'
}

class Console(Application):
    def __init__(self, game: Game):
        self.game = game

    def run(self):
        nb_question = input("Number of questions: ")
        self.game.new_round(int(nb_question))
        while self.game:
            question = self.game.create_question()
            question.on_answer(self._handle_answer)
            answer = input(f"\n{question.word.infinitive} ({question.word.definition}) in {question.form}:\n")
            question.answer(answer)
        print(f"\nscore {self.game.state.success} / {self.game.state.answered}")

    def _handle_answer(self, is_correct: bool, correct_answer: str, *args):
        print("Good answer") if is_correct else print(f"Wrong ! The answer is {colors['green']}{correct_answer}{colors['reset']}")
