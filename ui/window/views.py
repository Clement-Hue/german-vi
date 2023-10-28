from abc import abstractmethod
from typing import Callable, TypeVar, Generic
import tkinter as tk

T = TypeVar("T")

class CheckboxesFrame(Generic[T]):
    def __init__(self, values: T, parent, title: str, checkbox_label: Callable[[T], str]):
        self.selected = []
        self._checkbox_label = checkbox_label
        self._values = values
        self._main_frame = tk.LabelFrame(parent, text=title)
        self._checkboxes_frame = self._create_checkboxes_frame(self._main_frame)
        self._btn_frame = self._create_btn_frame(self._main_frame)
        self._packing()

    def pack(self, *args, **kwargs):
        self._main_frame.pack(*args, **kwargs)
    def _packing(self):
        self._checkboxes_frame.pack()
        self._btn_frame.pack()
    def _create_btn_frame(self, parent):
        frame = tk.Frame(parent)
        tk.Button(frame, text="All", command=lambda: self._handle_select_all(self._checkboxes_frame.winfo_children())).pack(side=tk.LEFT)
        tk.Button(frame, text="None", command=lambda: self._handle_unselect_all(self._checkboxes_frame.winfo_children())).pack(side=tk.RIGHT)
        return frame
    def _create_checkboxes_frame(self, parent):
        checkbox_per_row = 8
        frame = tk.Frame(parent)
        for i,value in enumerate(self._values):
            checkbox_var = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(frame, text=self._checkbox_label(value), variable=checkbox_var, font=("Arial", 15),
                                      command=lambda v=value, c=checkbox_var: self._handle_check(v, c))
            checkbox.grid(row=i // checkbox_per_row, column=i % checkbox_per_row)
        return frame

    def _handle_check(self, value, checkbox: tk.IntVar):
        if checkbox.get():
            self.selected.append(value)
        else:
            self.selected.remove(value)

    def _handle_select_all(self, checkboxes):
        self.selected = self._values
        for checkbox in checkboxes:
            checkbox.select()

    def _handle_unselect_all(self, checkboxes):
        self.selected = []
        for checkbox in checkboxes:
            checkbox.deselect()


class View:
    def __init__(self, window):
        self._window = window

    @abstractmethod
    def _show(self, *args, **kwargs):
        pass

    def _remove_widget(self, widget):
        widget.grid_forget()
        widget.pack_forget()
        widget.place_forget()
    def _remove_all_widgets(self):
        for widget in self._window.winfo_children():
            self._remove_widget(widget)
    def __call__(self, *args, **kwargs):
        self._remove_all_widgets()
        self._show(*args, **kwargs)

    def show_error(self, *args, **kwargs):
        pass

class MainView(View):
    def __init__(self, window, on_validate):
        super().__init__(window)
        self._view_frame = tk.Frame(window)
        self._counter_label_w = tk.Label(self._view_frame)
        self._question_label_w = tk.Label(self._view_frame)
        self._answer_frame = self._create_answer_frame(self._view_frame, on_validate=on_validate)
        self._validate_w = tk.Button(self._view_frame, text="Validate", fg='blue', command=lambda: on_validate(self._textfield_w.get()))
        self._error_label_w = tk.Label(self._view_frame, fg="red")
        self._packing()

    def _packing(self):
        self._counter_label_w.pack(pady=(0,50))
        self._question_label_w.pack()
        self._answer_frame.pack()
        self._validate_w.pack()
        self._error_label_w.pack()

    def _create_answer_frame(self, parent, on_validate):
        frame = tk.Frame(parent)
        self._textfield_w = tk.Entry(frame, bg='white', font=("Arial", 20), bd=5)
        self._textfield_w.bind("<Return>", lambda e: on_validate(self._textfield_w.get()))
        self._textfield_w.bind("<Alt-s>", lambda e: self._insert_letter_eszett())
        self._textfield_w.pack(side=tk.LEFT)
        tk.Button(frame, text="ß", command=self._insert_letter_eszett).pack(side=tk.RIGHT, padx=10)
        return frame

    def _insert_letter_eszett(self):
        current_position = self._textfield_w.index(tk.INSERT)
        self._textfield_w.insert(current_position, "ß")

    def _show(self, infinitive: str, definition: str, form: str, current: int, nb_question: int):
        self._error_label_w.config(text="")
        self._question_label_w.config(text=f"{infinitive} / {definition}\n{form}")
        self._counter_label_w.config(text=f"{current} / {nb_question}")
        self._textfield_w.delete(0, tk.END)
        self._view_frame.pack(expand=True)
        self._textfield_w.focus_set()

    def show_error(self, message: str):
        self._error_label_w.config(text=message)


class SettingView(View):
    def __init__(self, window, words, forms, on_start):
        super().__init__(window)
        self._view_frame = tk.Frame()
        self._nb_question = tk.IntVar(value=10)
        self._word_selection_frame = CheckboxesFrame(words, self._view_frame, title="Word list", checkbox_label=lambda v: v.infinitive)
        self._form_selection_frame = CheckboxesFrame(forms, self._view_frame, title="Form list", checkbox_label=lambda f: f)
        self._start_btn_w = tk.Button(self._view_frame, text="Start", fg='Green',
                                      command=lambda: on_start(self._nb_question.get(), self._word_selection_frame.selected,
                                                               self._form_selection_frame.selected))
        self._nb_question_frame = self._create_question_frame(self._view_frame)
        self._error_label_w = tk.Label(self._view_frame, fg="red")
        self._packing()

    def _packing(self):
        self._word_selection_frame.pack(pady=20)
        self._form_selection_frame.pack(pady=20)
        self._nb_question_frame.pack()
        self._start_btn_w.pack()
        self._error_label_w.pack()
    def _create_question_frame(self, parent):
        frame = tk.Frame(parent)
        tk.Label(frame, text="Number of question").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self._nb_question, font=("Arial", 20)).pack(side=tk.RIGHT)
        return frame
    def _show(self):
        self._view_frame.pack()

    def show_error(self, error: str):
        self._error_label_w.config(text=error)

class ScoreView(View):
    def __init__(self, window, on_restart):
        super().__init__(window)
        self._on_restart = on_restart
        self._view_frame = tk.Frame(window)
        self._score_label = tk.Label(self._view_frame, font=("Arial", 50))
        self._score_label.pack()
        tk.Button(self._view_frame, text="Restart", command=self._on_restart).pack()

    def _show(self, success: int, nb_question: int):
        self._score_label.config(text=f"Score: {success} / {nb_question}")
        self._view_frame.pack(expand=True)
        self._view_frame.focus_set()