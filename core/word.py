from typing import Dict

class Word:
    def __init__(self, infinitive: str, definition: str, tenses: Dict[str, str] = None):
        self.infinitive = infinitive
        self.definition = definition
        self.tenses = tenses

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.infinitive == other.infinitive and \
            self.definition == other.definition and self.tenses == other.tenses
        return False
