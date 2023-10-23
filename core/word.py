from typing import Dict

class Word:
    def __init__(self, infinitive: str, definition: str, forms: Dict[str, str] = None):
        self.infinitive = infinitive
        self.definition = definition
        self.forms = forms

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.infinitive == other.infinitive and \
            self.definition == other.definition and self.forms == other.forms
        return False
