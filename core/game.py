import csv
from core.word import Word
from core.question import Question
from core.state import State


class Game:

    def __init__(self, csv_path: str):
        """
        :param csv_path: CSV must contain header with 'definition' and 'infinitive' columns,
            the other columns will be treated as tense
        """
        self.words = []
        self.forms = []
        self.state = None
        self._load_words(csv_path)

    def __bool__(self):
        """
        :return: True if the game is still on going
        """
        return self.state.answered < self.state.tries

    def start(self, tries = 1):
        self.state = State(tries=tries)

    def create_question(self):
        question = Question(words=self.words)
        question.on_answer(self._handle_answer)
        return question

    def _load_words(self, csv_path: str):
        """
        Open csv file and create forms and words attributes
        :param csv_path: path of the csv file
        """
        with open(csv_path, encoding="utf8") as csvfile:
            content = csv.DictReader(csvfile)
            columns_to_exclude = ["infinitive", "definition"]
            for col in columns_to_exclude:
                if col not in content.fieldnames:
                    raise KeyError(f"'{col}' header must be present in the CSV file")
            self.forms = [x for x in content.fieldnames if x not in columns_to_exclude ]
            for row in content:
                self.words.append(Word(infinitive=row[columns_to_exclude[0]], definition=row[columns_to_exclude[1]],
                                       forms={key: row[key] for key in self.forms}
                                   ))
    def _handle_answer(self, is_correct: bool):
        if self.state is None:
            return
        self.state.answered += 1
        if is_correct:
            self.state.success += 1
