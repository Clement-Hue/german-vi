import random, csv
from typing import List
from core.word import Word


class Game:
    words = []

    def __init__(self, csv_path: str):
        self._load_words(csv_path)
        self.tries = 0
        self._count = 0
        self.success = 0
        self._word, self._form = None, None

    def __bool__(self):
        return self._count < self.tries

    def start(self, tries):
        self._count = 0
        self.success = 0
        self.tries = tries

    def _load_words(self, csv_path: str):
        with open(csv_path, encoding="utf8") as csvfile:
            content = csv.DictReader(csvfile)
            for row in content:
                self.words.append(Word(infinitive=row["infinitive"], definition=row["definition"],
                                       forms={key: row[key] for key in row if key not in ["infinitive", "definition"]}
                                   ))

    def question(self):
        self._count += 1
        self._word = random.choice(list(filter(lambda w: w.selected ,self.words)))
        self._form = random.choice(list(self._word.headers))
        return self._word, self._form

    def answer(self, res):
        if res == self.expected_answer:
            self.success += 1
            return True
        return False

    @property
    def expected_answer(self):
        return self._word.headers[self._form]
