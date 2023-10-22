
class Word:
    def __init__(self, infinitive, definition, forms = None):
        self.infinitive = infinitive
        self.definition = definition
        self.forms = forms
        self.selected = True

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.infinitive == other.infinitive and \
            self.definition == other.definition and self.forms == other.forms
        return False
