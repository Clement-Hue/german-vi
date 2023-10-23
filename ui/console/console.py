from __future__ import annotations
from typing import TYPE_CHECKING
from ui.application import Application
if TYPE_CHECKING:
    from core.game import Game

colors = {
    "blue": '\033[94m',
    "reset": '\033[0m',
    "green": '\033[92m',
    "red": "\033[91m"
}

class Console(Application):
    def __init__(self, game: Game):
        self.game = game

    def run(self):
        nb_question = input("Number of questions: ")
        rnd = self.game.new_round(int(nb_question))
        while rnd:
            question = rnd.create_question()
            question.on_answer(self._handle_answer)
            answer = input(f"\n{question.word.infinitive} ({question.word.definition}) in {question.form}:\n")
            question.answer(answer)
        print(f"\nscore {rnd.state.success} / {rnd.state.answered}")

    def _handle_answer(self, is_correct: bool, correct_answer: str, *args):
        print(f"{colors['green']}Good answer{colors['reset']}") if is_correct else\
            print(f"{colors['red']}Wrong !{colors['reset']} The answer is {colors['blue']}{correct_answer}{colors['reset']}")
