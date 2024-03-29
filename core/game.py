import csv
from typing import Callable, List
from core.word import Word
from core.question import Question
from core.round import Round


class Game:

    def __init__(self, csv_path: str):
        """
        :param csv_path: CSV must contain header with 'definition' and 'infinitive' columns,
            the other columns will be treated as tense
        """
        self.words = []
        self.tenses = []
        self._load_words(csv_path)

    def new_round(self, nb_question: int = 1, selected_words: Callable[[List[Word]], List[Word]] = None,
                  selected_tenses: Callable[[List[str]], List[str]]  = None):
        """
        Initialise the game with the number of questions
        :param selected_words: callback which return a subarray of the word list
        :param selected_tenses: callback which return a subarray of the tense list
        :param nb_question: number of questions ask during the game
        """
        return Round(question_factory= lambda : Question(
               words=selected_words(self.words) if selected_words else self.words, selected_tenses=selected_tenses
        ), nb_question=nb_question)

    def _load_words(self, csv_path: str):
        """
        Open csv file and create tenses and words attributes
        :param csv_path: path of the csv file
        """
        with open(csv_path, encoding="utf8") as csvfile:
            content = csv.DictReader(csvfile)
            columns_to_exclude = ["infinitive", "definition"]
            for col in columns_to_exclude:
                if col not in content.fieldnames:
                    raise KeyError(f"'{col}' header must be present in the CSV file")
            self.tenses = [x for x in content.fieldnames if x not in columns_to_exclude ]
            for row in content:
                self.words.append(Word(infinitive=row[columns_to_exclude[0]], definition=row[columns_to_exclude[1]],
                                       tenses={key: row[key] for key in self.tenses}
                                   ))

