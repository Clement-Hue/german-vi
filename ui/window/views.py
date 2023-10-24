from abc import abstractmethod
from tkinter import Button, Entry, Label, StringVar, Checkbutton,\
    Frame, IntVar, LEFT, RIGHT, INSERT, TOP


class WordSelectionFrame:
    def __init__(self, words, window):
        self.selected_words = []
        self._words = words
        self._window = window
        self._frame = Frame(self._window)
        self._checkboxes = self._create_checkboxes()
        self._btn_frame = Frame(self._window)
        Button(self._btn_frame, text="All", command=lambda: self._select_all(self._checkboxes)).pack(side=LEFT)
        Button(self._btn_frame, text="None", command=lambda: self._unselect_all(self._checkboxes)).pack(side=RIGHT)

    def _create_checkboxes(self):
        checkboxes = []
        for word in self._words:
            checkbox_var = IntVar(value=0)
            checkbox = Checkbutton(self._frame, text=word.infinitive, variable=checkbox_var, font=("Arial", 15))
            checkbox.config(command=lambda w=word, c=checkbox_var: self._on_check(w, c))
            checkboxes.append(checkbox)
        return checkboxes

    def show_words(self):
        self._frame.pack()
        self._btn_frame.pack()
        for i in range(len(self._words)):
            self._checkboxes[i].grid(row=i // 5, column=i % 5)

    def _on_check(self, word, checkbox: IntVar):
        if checkbox.get():
            self.selected_words.append(word)
        else:
            self.selected_words.remove(word)

    def _select_all(self, checkboxes):
        self.selected_words = self._words
        for checkbox in checkboxes:
            checkbox.select()

    def _unselect_all(self, checkboxes):
        self.selected_words = []
        for checkbox in checkboxes:
            checkbox.deselect()


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

    def show_error(self, *args, **kwargs):
        pass

class MainView(View):
    def __init__(self, window, on_validate, on_continue):
        super().__init__(window)
        self._answer = StringVar()
        self._label = StringVar()
        self._parent_frame = Frame(window)
        Label(self._parent_frame, textvariable=self._label).pack()
        self._create_answer_frame(self._parent_frame,on_validate=on_validate)
        self._validate_w = Button(self._parent_frame, text="Validate", fg='blue', command=lambda: on_validate(self._answer.get()))
        self._continue_w = Button(self._parent_frame, text="Continue", fg='blue', command=on_continue)
        self._continue_w.bind("<Return>", lambda e: on_continue())
        self._error_w = Label(self._parent_frame, fg="red")

    def _create_answer_frame(self, parent, on_validate):
        frame = Frame(parent)
        Label(frame, text="Answer:", font=("Arial", 15)).pack(side=TOP)
        self._textfield_w = Entry(frame, textvariable=self._answer, bg='white', font=("Arial", 20), bd=5)
        self._textfield_w.bind("<Return>", lambda e: on_validate(self._answer.get()))
        self._textfield_w.pack(side=LEFT)
        Button(frame, text="ß", command=self._add_eszett).pack(side=RIGHT, padx=10)
        frame.pack()

    def _add_eszett(self):
        self._answer.set(self._answer.get() + "ß")
        pos = self._textfield_w.index(INSERT)
        self._textfield_w.icursor(pos + 1)

    def _show(self, label: str):
        self._label.set(label)
        self._answer.set("")
        self._parent_frame.pack(expand=True)
        self._validate_w.pack()
        self._textfield_w.focus_set()
        self._continue_w.pack_forget()
        self._error_w.pack_forget()

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
        self._nb_question = IntVar(value=10)
        self._word_selection = WordSelectionFrame(self._words, self._window)
        self._start_btn = Button(self._window, text="Start", fg='Green',
                                 command=lambda: self._on_start(self._nb_question.get(), self._word_selection.selected_words))
        self._try_frame = Frame(self._window)
        Label(self._try_frame, text="Number of question").pack(side=LEFT)
        Entry(self._try_frame, textvariable=self._nb_question, font=("Arial", 20)).pack(side=RIGHT)
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
        self._parent_frame = Frame(window)
        self._score_label = Label(self._parent_frame, font=("Arial", 50))
        self._score_label.pack()
        Button(self._parent_frame, text="Restart", command=self._on_restart).pack()

    def _show(self, success: int, nb_question: int):
        self._score_label.config(text=f"Score: {success} / {nb_question}")
        self._parent_frame.pack(expand=True)
        self._parent_frame.focus_set()