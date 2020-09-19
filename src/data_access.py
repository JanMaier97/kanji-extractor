from aqt import mw

class KanjiNote():
    def __init__(self):
        self._fields = []
        self._field_values = {}
        pass


class AnkiDAO():
    def __init__(self):
        pass

    def get_deck_names(self):
        sorted(mw.col.decks.allNames(False))

    def get_model_names(self):
        return sorted(mw.col.models.allNames())

    def get_model_fields(self, model_name):
        model = mw.col.models.byName(model_name)
        if model is None:
            pass
        return mw.col.models.fieldNames(model)

    def get_missing_kanji(self):
        pass

    def get_kanji_notes(self):
        pass

    def add_notes(self, notes):
        pass

    def upsert_notes(self, notes):
        pass


class CommonConfigDAO():
    def __init__(self):
        pass


class KanjiDicConfigDAO():
    def __init__(self):
        pass

class KanjiDAO():
    def __init__(self):
        pass
