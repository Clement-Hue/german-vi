from game import Game
from window import Window


class Application:
    def __init__(self):
        tries = input("Number of try: ")
        self.game = Game(int(tries))
        self.window = Window(self.game)

    def run(self):
        self.window.run()

