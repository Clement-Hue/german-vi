from typing import Iterator

from ui.window.views_manager import ViewsManager
from ui.window.window_impl import WindowTkinter
from core.question import Question
from core.round import Round
from ui.application import Application

class WindowState:
    round: Round
    question_iter: Iterator[Question]
    question: Question

class Window(Application):
    def __init__(self, game):
        self.game = game
        self._state = WindowState()
        self._window_impl = WindowTkinter()
        self._view_manager = ViewsManager(
            setting=self._window_impl.create_setting_view(words=self.game.words, on_start=self._handle_start),
            main=self._window_impl.create_main_view(on_validate=self._handle_validate),
            score=self._window_impl.create_score_view(on_restart=self._handle_restart)
        )

    def run(self):
        self._view_manager.show("setting")
        self._window_impl.loop()
    def _handle_start(self, nb_question, selected_words):
        try:
            self._state.round = self.game.new_round(nb_question, selected_words=lambda _: selected_words)
            self._state.question_iter = iter(self._state.round.questions)
            self._show_next_question()
        except IndexError:
            self._view_manager.show_error("Please select at least one verb")

    def _handle_restart(self):
        self._view_manager.show("setting")

    def _show_next_question(self):
        self._state.question = next(self._state.question_iter, None)
        if self._state.question is None:
            self._view_manager.show("score",success=self._state.round.state.success, nb_question=self._state.round.nb_question)
            return
        self._state.question.on_answer(self._handle_answer)
        self._view_manager.show("main",
            f"{self._state.question.word.infinitive} / {self._state.question.word.definition}\n"
            f"{self._state.question.form}")

    def _handle_answer(self, is_correct: bool, correct_answer: str, *args, **kwargs):
        if not is_correct:
            self._view_manager.show_error(f"WRONG, the answer was {correct_answer}")
            return
        self._show_next_question()
    def _handle_validate(self, answer):
        self._state.question.answer(answer)
