from ui.window.views import MainView, SettingView, ScoreView
from tkinter import Tk
from tkinter.font import nametofont
from abc import ABC, abstractmethod


class WindowImpl(ABC):
    @abstractmethod
    def create_setting_view(self, **kwargs):
        pass

    @abstractmethod
    def create_main_view(self, **kwargs):
        pass

    @abstractmethod
    def create_score_view(self, **kwargs):
        pass

    @abstractmethod
    def loop(self):
        pass

class WindowTkinter(WindowImpl):
    def __init__(self):
        self._window = Tk()
        self._window.geometry("700x700")
        self._window.title('German strong verbs')
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=25, family="Arial")

    def create_setting_view(self, *args, **kwargs):
        return SettingView(self._window, *args, **kwargs)

    def create_main_view(self, *args, **kwargs):
        return MainView(self._window, *args, **kwargs)

    def create_score_view(self, *args, **kwargs):
        return ScoreView(self._window,*args, **kwargs)

    def loop(self):
        self._window.mainloop()
