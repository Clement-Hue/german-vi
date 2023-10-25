from abc import abstractmethod
import tkinter as tk


class WordSelectionFrame:
    def __init__(self, words, window):
        self.selected_words = []
        self._words = words
        self._window = window
        self._frame = tk.Frame(self._window)
        self._checkboxes = self._create_checkboxes()
        self._btn_frame = tk.Frame(self._window)
        tk.Button(self._btn_frame, text="All", command=lambda: self._select_all(self._checkboxes)).pack(side=tk.LEFT)
        tk.Button(self._btn_frame, text="None", command=lambda: self._unselect_all(self._checkboxes)).pack(side=tk.RIGHT)

    def _create_checkboxes(self):
        checkboxes = []
        for word in self._words:
            checkbox_var = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(self._frame, text=word.infinitive, variable=checkbox_var, font=("Arial", 15))
            checkbox.config(command=lambda w=word, c=checkbox_var: self._on_check(w, c))
            checkboxes.append(checkbox)
        return checkboxes

    def show_words(self):
        self._frame.pack()
        self._btn_frame.pack()
        for i in range(len(self._words)):
            self._checkboxes[i].grid(row=i // 5, column=i % 5)

    def _on_check(self, word, checkbox: tk.IntVar):
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
        self._label_w = tk.Label(self._view_frame)
        self._answer_frame = self._create_answer_frame(self._view_frame, on_validate=on_validate)
        self._validate_w = tk.Button(self._view_frame, text="Validate", fg='blue', command=lambda: on_validate(self._textfield_w.get()))
        self._error_w = tk.Label(self._view_frame, fg="red")
        self._packing()

    def _packing(self):
        self._label_w.pack()
        self._answer_frame.pack()
        self._validate_w.pack()
        self._error_w.pack()

    def _create_answer_frame(self, parent, on_validate):
        frame = tk.Frame(parent)
        tk.Label(frame, text="Answer:", font=("Arial", 15)).pack(side=tk.TOP)
        self._textfield_w = tk.Entry(frame, bg='white', font=("Arial", 20), bd=5)
        self._textfield_w.bind("<Return>", lambda e: on_validate(self._textfield_w.get()))
        self._textfield_w.bind("<Alt-s>", lambda e: self._insert_letter_eszett())
        self._textfield_w.pack(side=tk.LEFT)
        tk.Button(frame, text="ß", command=self._insert_letter_eszett).pack(side=tk.RIGHT, padx=10)
        return frame

    def _insert_letter_eszett(self):
        current_position = self._textfield_w.index(tk.INSERT)
        self._textfield_w.insert(current_position, "ß")

    def _show(self, label: str):
        self._error_w.config(text="")
        self._label_w.config(text=label)
        self._textfield_w.delete(0, tk.END)
        self._view_frame.pack(expand=True)
        self._textfield_w.focus_set()

    def show_error(self, message: str):
        self._error_w.config(text=message)


class SettingView(View):
    def __init__(self, window, words, on_start):
        super().__init__(window)
        self._words = words
        self._on_start = on_start
        self._nb_question = tk.IntVar(value=10)
        self._word_selection = WordSelectionFrame(self._words, self._window)
        self._start_btn = tk.Button(self._window, text="Start", fg='Green',
                                 command=lambda: self._on_start(self._nb_question.get(), self._word_selection.selected_words))
        self._try_frame = tk.Frame(self._window)
        tk.Label(self._try_frame, text="Number of question").pack(side=tk.LEFT)
        tk.Entry(self._try_frame, textvariable=self._nb_question, font=("Arial", 20)).pack(side=tk.RIGHT)
        self._error_label = tk.Label(self._window, fg="red")

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
        self._parent_frame = tk.Frame(window)
        self._score_label = tk.Label(self._parent_frame, font=("Arial", 50))
        self._score_label.pack()
        tk.Button(self._parent_frame, text="Restart", command=self._on_restart).pack()

    def _show(self, success: int, nb_question: int):
        self._score_label.config(text=f"Score: {success} / {nb_question}")
        self._parent_frame.pack(expand=True)
        self._parent_frame.focus_set()