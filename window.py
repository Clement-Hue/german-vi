from tkinter import Tk, Button, Entry, Label, StringVar, Checkbutton, Frame, IntVar

class WordSelection:
    def __init__(self, words, window):
        self.words = words
        self._window = window

    def show_words(self):
        checkboxes = []
        frame = Frame(self._window)
        frame.pack()
        Button(self._window, text="All", command= lambda : self._select_all(checkboxes)).pack()
        Button(self._window, text="None", command= lambda : self._unselect_all(checkboxes)).pack()
        for i in range(len(self.words)):
            word = self.words[i]
            checkbox_var = IntVar(value=1 if word.selected else 0)
            checkbox = Checkbutton(frame, text=word.infinitive, variable=checkbox_var ,font=("Arial", 15))
            checkbox.config(command=lambda w=word, c=checkbox_var: self._on_check(w, c))
            checkbox.grid(row=i//5, column=i%5)
            checkboxes.append((checkbox, word))

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

class ScreenFactory:
    def __init__(self, window, answer, on_continue, on_validate,
                 on_start):
        self._window = window
        self._on_continue = on_continue
        self._on_validate = on_validate
        self._on_start = on_start
        self._label = StringVar()
        self._answer = answer
        self._create_widgets()

    def _create_widgets(self):
        self._question_w = Label(self._window, textvariable=self._label, font=("Helvetica", 16))
        self._textfield_label_w =  Label(self._window, text="Answer:")
        self._textfield_w = Entry(self._window, textvariable=self._answer, bg='white', bd=5)
        self._textfield_w.bind("<Return>", self._on_validate)
        self._validate_w = Button(self._window, text="Validate", fg='blue', command=self._on_validate)
        self._continue_w = Button(self._window, text="Continue", fg='blue', command=self._on_continue)
        self._continue_w.bind("<Return>", self._on_continue)
        self._error_w = Label(self._window, fg="red")

    def main_screen(self):
        self._question_w.pack()
        self._textfield_label_w.pack()
        self._textfield_w.pack()
        self._textfield_w.focus_set()
        self._validate_w.pack()

    def reset_main_screen(self, label: str):
        self._label.set(label)
        self._answer.set("")
        self._textfield_w.focus_set()
        self._continue_w.pack_forget()
        self._error_w.pack_forget()
        self._validate_w.pack()

    def first_screen(self, words):
        word_selection = WordSelection(words, self._window)
        word_selection.show_words()
        start_w = Button(self._window, text="Start", fg='Green',  font=("Arial", 30),
                         command=self._on_start)
        start_w.pack()

    def score_screen(self, success, tries):
        Label(self._window, text=f"Score: {success} / {tries}", font=("Arial", 50)).pack()

    def show_error(self, expected_answer):
        self._validate_w.pack_forget()
        self._continue_w.pack()
        self._continue_w.focus_set()
        self._error_w.config(text=f"WRONG, the answer was {expected_answer}")
        self._error_w.pack()

class Window:
    def __init__(self, game):
        self._window = Tk()
        self.game = game
        self.answer = StringVar()
        self.screen_factory = ScreenFactory(self._window,  answer=self.answer,
                                            on_continue=self._new_question, on_validate=self._on_validate,
                                            on_start=self._on_start)
        self._window.geometry("700x700")
        self._window.title('German strong verbs')

    def _on_start(self):
        try:
            self._clean_window()
            self.screen_factory.main_screen()
            self._new_question()
        except IndexError:
            Label(self._window, fg="red", text="Please select at least one verb").pack()



    def run(self):
        self.screen_factory.first_screen(self.game.words)
        self._window.mainloop()


    def _clean_window(self):
        for widget in self._window.winfo_children():
            widget.pack_forget()

    def _new_question(self, e=None):
        if not self.game:
            self._clean_window()
            self.screen_factory.score_screen(self.game.success, self.game.tries)
            return
        word, form = self.game.question()
        self.screen_factory.reset_main_screen(
            f"{word.infinitive} / {word.definition}\n"
            f"{form}")

    def _on_validate(self, e=None):
        if not self.game.answer(self.answer.get()):
            self.screen_factory.show_error(self.game.expected_answer)
        else:
            self._new_question()
