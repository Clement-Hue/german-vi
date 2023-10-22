from tkinter import Tk
from tkinter.font import nametofont

from ui.application import Application
from ui.window.views import MainView, SettingView, ScoreView

class Window(Application):
    def __init__(self, game):
        self.game = game
        self._window = Tk()
        self._window.geometry("700x700")
        self._window.title('German strong verbs')
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=25, family="Arial")
        self._setting_view = SettingView(self._window, self.game.words,
                                         on_start=self._on_start)
        self._main_view = MainView(self._window, on_validate=self._on_validate, on_continue=self._new_question)
        self._score_view = ScoreView(self._window, on_restart=self._on_restart)

    def _on_start(self, tries):
        try:
            self.game.init(tries)
            self._new_question()
        except IndexError:
            self._setting_view.show_error("Please select at least a verb")

    def run(self):
        self._setting_view()
        self._window.mainloop()

    def _on_restart(self):
        self._setting_view()

    def _new_question(self):
        if not self.game:
            self._score_view(success=self.game.success, tries=self.game.tries)
            return
        word, form = self.game.create_question()
        self._main_view(
            f"{word.infinitive} / {word.definition}\n"
            f"{form}")

    def _on_validate(self, answer):
        if not self.game.answer(answer):
            self._main_view.show_error(self.game.expected_answer)
        else:
            self._new_question()
