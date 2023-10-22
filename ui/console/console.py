from __future__ import annotations
from typing import TYPE_CHECKING
from ui.application import Application
if TYPE_CHECKING:
    from core.game import Game

class Console(Application):
    def __init__(self, game: Game):
        self.game = game

    def run(self):
        tries = input("Number of try: ")
        self.game.init(int(tries))
        while self.game:
            question = self.game.create_question()
            question.on_answer(self._handle_answer)
            answer = input(f"\n{question.word.infinitive} ({question.word.definition}) in {question.form}:\n")
            question.answer(answer)
        print(f"\nscore {self.game.state.success} / {self.game.state.answered}")

    def _handle_answer(self, is_correct: bool, correct_answer: str, *args):
        if is_correct:
            print("Good answer")
        else:
            print(f"Wrong ! The answer is {correct_answer}")
