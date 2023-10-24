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
            self._window_impl.create_setting_view(words=self.game.words, on_start=self._handle_start),
            self._window_impl.create_main_view(on_validate=self._handle_validate, on_continue=self._handle_continue),
            self._window_impl.create_score_view(on_restart=self._handle_restart)
        )

    def _handle_start(self, nb_question, selected_words):
        try:
            self._state.round = self.game.new_round(nb_question, selected_words=lambda _: selected_words)
            self._state.question_iter = iter(self._state.round.questions)
            self._handle_continue()
        except IndexError:
            self._view_manager.show_error("Please select at least one verb")

    def run(self):
        self._view_manager.show("Setting")
        self._window_impl.loop()

    def _handle_restart(self):
        self._view_manager.show("Setting")

    def _handle_continue(self):
        self._state.question = next(self._state.question_iter, None)
        if self._state.question is None:
            self._view_manager.show("Score",success=self._state.round.state.success, nb_question=self._state.round.nb_question)
            return
        self._state.question.on_answer(self._handle_answer)
        self._view_manager.show("Main",
            f"{self._state.question.word.infinitive} / {self._state.question.word.definition}\n"
            f"{self._state.question.form}")

    def _handle_answer(self, is_correct: bool, correct_answer: str, answer: str):
        if not is_correct:
            self._view_manager.show_error(correct_answer)
            return
        self._handle_continue()
    def _handle_validate(self, answer):
        self._state.question.answer(answer)
