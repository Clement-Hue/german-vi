from abc import abstractmethod
from tkinter import Tk, Button, Entry, Label, StringVar, Checkbutton, Frame, IntVar, LEFT, RIGHT

from game import Game


class WordSelectionFrame:
    def __init__(self, words, window):
        self.words = words
        self._window = window
        self._frame = Frame(self._window)
        self._checkboxes = self._create_checkboxes()
        self._btn_frame = Frame(self._window)
        Button(self._btn_frame, text="All", command=lambda: self._select_all(self._checkboxes)).pack(side=LEFT)
        Button(self._btn_frame, text="None", command=lambda: self._unselect_all(self._checkboxes)).pack(side=RIGHT)

    def _create_checkboxes(self):
        checkboxes = []
        for i in range(len(self.words)):
            word = self.words[i]
            checkbox_var = IntVar(value=1 if word.selected else 0)
            checkbox = Checkbutton(self._frame, text=word.infinitive, variable=checkbox_var, font=("Arial", 15))
            checkbox.config(command=lambda w=word, c=checkbox_var: self._on_check(w, c))
            checkboxes.append((checkbox, word))
        return checkboxes

    def show_words(self):
        self._frame.pack()
        self._btn_frame.pack()
        for i in range(len(self.words)):
            self._checkboxes[i][0].grid(row=i // 5, column=i % 5)

    def _on_check(self, word, checkbox: IntVar):
        word.selected = bool(checkbox.get())

    def _select_all(self, checkboxes):
        for checkbox in checkboxes:
            checkbox[0].select()
            checkbox[1].selected = True

    def _unselect_all(self, checkboxes):
        for checkbox in checkboxes:
            checkbox[0].deselect()
            checkbox[1].selected = False


class View:
    def __init__(self, window):
        self._window = window

    @abstractmethod
    def _show(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        for widget in self._window.winfo_children():
            widget.pack_forget()
        self._show(*args, **kwargs)


class MainView(View):
    def __init__(self, window, on_validate, on_continue):
        super().__init__(window)
        self._answer = StringVar()
        self._label = StringVar()
        self._question_w = Label(window, textvariable=self._label, font=("Helvetica", 16))
        self._textfield_label_w = Label(window, text="Answer:")
        self._textfield_w = Entry(window, textvariable=self._answer, bg='white', bd=5)
        self._textfield_w.bind("<Return>", lambda e: on_validate(self._answer.get()))
        self._validate_w = Button(window, text="Validate", fg='blue', command=lambda: on_validate(self._answer.get()))
        self._continue_w = Button(window, text="Continue", fg='blue', command=on_continue)
        self._continue_w.bind("<Return>", lambda e: on_continue())
        self._error_w = Label(window, fg="red")

    def _show(self, label: str):
        self._label.set(label)
        self._answer.set("")
        self._question_w.pack()
        self._textfield_label_w.pack()
        self._textfield_w.pack()
        self._textfield_w.focus_set()
        self._validate_w.pack()

    def show_error(self, expected_answer):
        self._validate_w.pack_forget()
        self._continue_w.pack()
        self._continue_w.focus_set()
        self._error_w.config(text=f"WRONG, the answer was {expected_answer}")
        self._error_w.pack()


class SettingView(View):
    def __init__(self, window, words, on_start):
        super().__init__(window)
        self._words = words
        self._on_start = on_start
        self._tries = IntVar()
        self._start_btn = Button(self._window, text="Start", fg='Green', font=("Arial", 30),
                                 command=lambda: self._on_start(self._tries.get()))
        self._word_selection = WordSelectionFrame(self._words, self._window)
        self._try_frame = Frame(self._window)
        Label(self._try_frame, text="Number of try").pack(side=LEFT)
        Entry(self._try_frame, textvariable=self._tries).pack(side=RIGHT)
        self._error_label = Label(self._window, fg="red")

    def _show(self):
        self._word_selection.show_words()
        self._try_frame.pack()
        self._start_btn.pack()

    def show_error(self, error: str):
        self._error_label.config(text=error)
        self._error_label.pack()

class ScoreView(View):
    def __init__(self, window, on_restart):
        super().__init__(window)
        self._on_restart = on_restart
        self._score_label = Label(self._window, font=("Arial", 50))
        self._restart_btn = Button(self._window, text="Restart", command=self._on_restart)

    def _show(self, success, tries):
        self._score_label.config(text=f"Score: {success} / {tries}")
        self._score_label.pack()
        self._restart_btn.pack()


class Window:
    def __init__(self):
        self._window = Tk()
        self.game = Game()
        self._window.geometry("700x700")
        self._window.title('German strong verbs')
        self._setting_view = SettingView(self._window, self.game.words,
                                         on_start=self._on_start)
        self._main_view = MainView(self._window, on_validate=self._on_validate, on_continue=self._new_question)
        self._score_view = ScoreView(self._window, on_restart=self._on_restart)

    def _on_start(self, tries):
        try:
            self.game.start(tries)
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
        word, form = self.game.question()
        self._main_view(
            f"{word.infinitive} / {word.definition}\n"
            f"{form}")

    def _on_validate(self, answer):
        if not self.game.answer(answer):
            self._main_view.show_error(self.game.expected_answer)
        else:
            self._new_question()
