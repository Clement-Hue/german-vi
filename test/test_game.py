import pytest
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
    rnd = game.new_round()
    question = rnd.questions[0]
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
    rnd = game.new_round()
    question = rnd.questions[0]
    question.answer("ff")
    assert rnd.state.answered == 1
    assert rnd.state.success == 0

def test_state_success(game):
    rnd = game.new_round()
    question = rnd.questions[0]
    correct_answer = question.word.forms[question.form]
    question.answer(correct_answer)
    assert rnd.state.answered == 1
    assert rnd.state.success == 1
    question.answer(correct_answer)
    assert rnd.state.answered == 1
    assert rnd.state.success == 1

def test_selected_words(game):
    rnd = game.new_round(selected_words=lambda words: [words[0]])
    assert len(rnd.words) == 1
    assert rnd.words[0] == Word(
        infinitive="befehlen", definition="to command",
        forms={
            "present": "befiehlt",
            "simple past": "befahl",
            "past participle": "hat befohlen"
        }
    )