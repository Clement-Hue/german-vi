from game import Game
from window import Window


class Application:
    def __init__(self):
        tries = input("Number of try: ")
        self.game = Game(int(tries))
        word, form = self.game.question()
        self.window = Window(word, form, on_validate=self.on_validate,
                        on_continue=self.on_continue)

    def start(self):
        self.window.start()

    def on_validate(self, w: Window):
        if not self.game.answer(w.answer.get()):
            w.show_error(self.game.expected_answer)

    def on_continue(self, w: Window):
        if not self.game:
            w.show_result(self.game.success, self.game.tries)
            return
        word, form = self.game.question()
        w.set_label(word, form)
