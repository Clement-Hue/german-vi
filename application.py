from game import Game
from window import Window


class Application:
    def __init__(self):
        self.game = Game()
        self.window = Window(self.game)

    def run(self):
        self.window.run()

