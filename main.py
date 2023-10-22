from ui.window import Window
from core.game import Game
from config import ROOT_DIR

if __name__ == '__main__':
    app = Window(Game(csv_path=f"{ROOT_DIR}/data/words.csv"))
    app.run()
