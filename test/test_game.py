import pytest
from core.game import Game
from core.word import Word

@pytest.fixture
def game():
    return Game("test_data.csv")

def test_game(game):
    print(game.words[0].forms)
    assert game.words[0] == Word(
        infinitive="befehlen", definition="to command",
        forms={
            "present": "befiehlt",
            "simple past": "befahl",
            "past participle": "hat befohlen",
        }
    )