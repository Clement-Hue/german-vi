from tkinter import Tk, Button, Entry, Label, StringVar


class Window:
    def __init__(self, word, form, on_validate, on_continue):
        self._window = Tk()
        self.on_validate = on_validate
        self.on_continue = on_continue
        self.answer = StringVar()
        self.label = StringVar()
        self._window.geometry("500x300")
        self._window.title('German strong verbs')
        self.set_label(word, form)
        self._widgets()

    def _widgets(self):
        Entry(self._window,textvariable=self.answer, bg='white', bd=5).grid(row=1, column=1)
        self._validate_w = Button(self._window, text="Validate", fg='blue', command=self._on_validate)
        self._continue_w = Button(self._window, text="Continue", fg='blue', command=self._on_continue)
        self._error_w = Label(self._window, fg="red")
        Label(self._window,textvariable=self.label, font=("Helvetica", 16)).grid(row=0, columnspan=2)
        Label(self._window, text="Answer:").grid(row=1, column=0)
        self._validate_w.grid(row=2, columnspan=2)

    def _on_continue(self):
        self._continue_w.grid_forget()
        self._error_w.grid_forget()
        self.answer.set("")
        self._validate_w.grid(row=2, columnspan=2)
        self.on_continue(self)

    def _on_validate(self):
        self.on_validate(self)

    def start(self):
        self._window.mainloop()

    def show_error(self, expected_answer):
        self._validate_w.grid_forget()
        self._continue_w.grid(row=2, columnspan=2)
        self._error_w.config(text=f"WRONG, the answer was {expected_answer}")
        self._error_w.grid(row=3, columnspan=2)

    def show_result(self, success, tries):
        self._clean_window()
        Label(self._window, text=f"Result:{success} / {tries}", font=("Arial", 50)).grid(row=0)

    def _clean_window(self):
        for widget in self._window.winfo_children():
            widget.grid_forget()

    def set_label(self, word, form):
        self.label.set(f"Word: {word.infinitive} / {word.definition}\n"
                    f"{form}")
