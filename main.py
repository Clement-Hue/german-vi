from ui import Window, Console
from core.game import Game
from config import ROOT_DIR

if __name__ == '__main__':
    app = Console(Game(csv_path=f"{ROOT_DIR}/data/words.csv"))
    app.run()
