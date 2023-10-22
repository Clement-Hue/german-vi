import pytest
from core.state import State
from core.game import Game
from core.word import Word
from core.question import Question

@pytest.fixture
def game():
    return Game("test_data.csv")

def test_load_words(game):
    assert game.words[0] == Word(
        infinitive="befehlen", definition="to command",
        forms={
            "present": "befiehlt",
            "simple past": "befahl",
            "past participle": "hat befohlen",
        }
    )
    assert game.words[1] == Word(
        infinitive="beginnen", definition="to begin",
        forms={
            "present": "beginnt",
            "simple past": "begann",
            "past participle": "hat begonnen",
        }
    )


def test_load_forms(game):
    assert game.forms == ["present", "simple past", "past participle"]

def test_generate_question(game):
    question = game.create_question()
    assert question.word in game.words
    assert question.form in game.forms

def test_answer_question():
    forms = {
        "present": "beginnt",
        "simple past": "begann",
        "past participle": "hat begonnen",
    }
    question = Question(words=[
     Word(
        infinitive="beginnen", definition="to begin",
        forms=forms
        )
    ])
    correct_answer = forms[question.form]
    assert question.answer("fff") is False
    assert question.answer(correct_answer) is True

def test_state_answered(game):
    game.init()
    question = game.create_question()
    question.answer("ff")
    assert game.state.answered == 1
    assert game.state.success == 0

def test_state_success(game):
    game.init()
    question = game.create_question()
    correct_answer = question.word.forms[question.form]
    question.answer(correct_answer)
    assert game.state.answered == 1
    assert game.state.success == 1

def test_start_state(game):
    game.init(10)
    assert game.state.tries == 10
    game.state.answered = 2
    game.state.success = 1
    game.init(2)
    assert game.state == State(tries=2)
