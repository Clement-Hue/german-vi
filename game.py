import random, csv

class Word:
    def __init__(self, infinitive, definition, forms = None):
        self.infinitive = infinitive
        self.definition = definition
        self.forms = forms
        self.selected = True

class Game:
    words = []
    forms = ["Present tense", "Simple past", "Past participle", "Definition"]

    def __init__(self):
        self._load_words()
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
    def _load_words(self):
        with open("words.csv", encoding="utf8") as csvfile:
            content = csv.reader(csvfile)
            next(content)
            for row in content:
                self.words.append(Word(infinitive=row[0], definition=row[4],
                                       forms=dict(zip(self.forms, row[1:-1])
                                                   )))

    def question(self):
        self._count += 1
        self._word = random.choice(list(filter(lambda w: w.selected ,self.words)))
        self._form = random.choice(list(self._word.forms))
        return self._word, self._form

    def answer(self, res):
        if res == self.expected_answer:
            self.success += 1
            return True
        return False

    @property
    def expected_answer(self):
        return self._word.forms[self._form]
