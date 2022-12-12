from tkinter import Tk, Button, Entry, Label, StringVar, Checkbutton, Frame, LEFT, IntVar


class Window:
    def __init__(self, words, on_validate, on_next):
        self._window = Tk()
        self.words = words
        self.on_validate = on_validate
        self.on_next = on_next
        self.answer = StringVar()
        self.label = StringVar()
        self._window.geometry("700x700")
        self._window.title('German strong verbs')
        self._first_screen()

    def _on_check(self, word, checkbox: IntVar):
        word.selected = bool(checkbox.get())
    def _show_words(self, checkboxes):
        frame = Frame(self._window)
        frame.pack()
        for i in range(len(self.words)):
            word = self.words[i]
            checkbox_var = IntVar(value=1 if word.selected else 0)
            checkbox = Checkbutton(frame, text=word.infinitive, variable=checkbox_var ,font=("Arial", 15))
            checkbox.config(command=lambda w=word, c=checkbox_var: self._on_check(w, c))
            checkbox.grid(row=i//5, column=i%5)
            checkboxes.append((checkbox, word))

    def _select_all(self, checkboxes):
        for checkbox in checkboxes:
            checkbox[0].select()
            checkbox[1].selected = True

    def _unselect_all(self, checkboxes):
        for checkbox in checkboxes:
            checkbox[0].deselect()
            checkbox[1].selected = False

    def _first_screen(self):
        checkboxes = []
        self._show_words(checkboxes)
        Button(self._window, text="All", command= lambda : self._select_all(checkboxes)).pack()
        Button(self._window, text="None", command= lambda : self._unselect_all(checkboxes)).pack()
        self._start_w = Button(self._window, text="Start", fg='Green',  font=("Arial", 30),
                               command=self._on_start)
        self._start_w.pack()

    def _on_start(self):
        try:
            self.on_next(self)
            self._clean_window()
            Label(self._window,textvariable=self.label, font=("Helvetica", 16)).pack()
            Label(self._window, text="Answer:").pack()
            self._textfield_w = Entry(self._window, textvariable=self.answer, bg='white', bd=5)
            self._textfield_w.pack()
            self._textfield_w.focus_set()
            self._textfield_w.bind("<Return>", self._on_validate)
            self._validate_w = Button(self._window, text="Validate", fg='blue', command=self._on_validate)
            self._continue_w = Button(self._window, text="Continue", fg='blue', command=self.next)
            self._continue_w.bind("<Return>", self.next)
            self._error_w = Label(self._window, fg="red")
            self._validate_w.pack()
        except IndexError:
            Label(self._window, fg="red", text="Please select at least one verb").pack()


    def next(self, e=None):
        self._textfield_w.focus_set()
        self._continue_w.pack_forget()
        self._error_w.pack_forget()
        self.answer.set("")
        self._validate_w.pack()
        self.on_next(self)

    def _on_validate(self, e=None):
        self.on_validate(self)

    def run(self):
        self._window.mainloop()

    def show_error(self, expected_answer):
        self._validate_w.pack_forget()
        self._continue_w.pack()
        self._continue_w.focus_set()
        self._error_w.config(text=f"WRONG, the answer was {expected_answer}")
        self._error_w.pack()

    def show_result(self, success, tries):
        self._clean_window()
        Label(self._window, text=f"Result:{success} / {tries}", font=("Arial", 50)).pack()

    def _clean_window(self):
        for widget in self._window.winfo_children():
            widget.pack_forget()

    def set_label(self, word, form):
        self.label.set(f"{word.infinitive} / {word.definition}\n"
                    f"{form}")
