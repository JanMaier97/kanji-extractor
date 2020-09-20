from aqt import mw
from typing import List #, Set, Dict, Tuple, Optional

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
            raise InvalidModelError(model_name)
        return mw.col.models.fieldNames(model)

    def get_missing_kanji(self):
        pass

    def get_kanji_notes(self):
        pass

    def add_notes(self, notes):
        pass

    def upsert_notes(self, notes):
        pass


class InvalidModelError(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name


class MissingFieldsError(Exception):
    def __init__(self, field_names: List[str]):
        self.field_names = field_names

class ConfigError(Exception):
    pass

class VocabConfigDAO():
    def __init__(self):
        self._config = mw.addonManager.getConfig(__name__)['vocab']

    def update_vocab_config(self, model_name: str, field_name: str) -> None:
        mid = _validate_model(model_name, [field_name])
        self._config['mid'] = mid
        self._config['field'] = field_name

    @property
    def vocab_model_name(self):
        model = mw.col.models.get(self._config['mid'])
        if model is None:
            return None
        return model['name']
    
    @property
    def vocab_field_name(self):
        return self._config['field']

    def save(self):
        mw.addonManager.writeConfig(__name__, {'vocab': self._config}) 

def _validate_model(model_name: str, field_name: str) -> int:
    model = mw.col.models.byName(model_name)
    if model is None:
        raise InvalidModelError(model_name)

    missing_fields = [field for field in field_names if field not in mw.col.models.fieldNames(model)]
    if len(missing_fields) > 0:
        raise MissingFieldsError(missing_fields)

    return model['id']


class KanjiDicConfigDAO():
    def __init__(self):
        self._config = mw.addonManager.getConfig(__name__)['kanjidic']
        self._fields = self._config['fields']

    def update_note_config(self, deck_name, model_name: str, kanji: str, meaning: str, onyomi: str, kunyomi: str, strokecount: str, frequency: str, radical: str) -> None:
        mid = _validate_model(model_name, [kanji, meaning, onyomi, kunyomi, strokecount, frequency, radical])
        self._config['mid'] = mid
        self._fields['kanji'] = kanji
        self._fields['meaning'] = meaning
        self._fields['onyomi'] = onyomi
        self._fields['kunyomi'] = kunyomi
        self._fields['strokecount'] = strokecount
        self._fields['frequency'] = frequency
        self._fields['radical'] = radical
        deck = mw.col.decks.byName(deck_name)
        if deck is None:
            raise ValueError
        self._config['did'] = deck['id']

    def update_grade_tag(self, enabled, prefix, postfix):
        self._config['grade'] = enabled
        self._config['grade_prefix'] = prefix
        self._config['grade_postfix'] = postfix

    def update_jlpt_tag(self, enabled, prefix, postfix):
        self._config['jlpt'] = enabled
        self._config['jltp_prefix'] = prefix
        self._config['jltp_postfix'] = postfix

    def save(self):
        mw.addonManager.writeConfig(__name__, {'kanjidic': self._config}) 

    @property
    def model_name(self):
        model = mw.col.models.get(self._config['mid'])
        if model is None:
            return None
        return model['name']

    @property
    def kanji(self):
        return self._fields['kanji']

    @property
    def meaning(self):
        return self._fields['meaning']

    @property
    def onyomi(self):
        return self._fields['onyomi']

    @property
    def kunyomi(self):
        return self._fields['kunyomi']

    @property
    def strokecount(self):
        return self._fields['strokecount']

    @property
    def frequency(self):
        return self._fields['frequency']

    @property
    def radical(self):
        return self._fields['radical']

    @property
    def jlpt_enabled(self):
        return self._config['jlpt']

    @property
    def jlpt_postfix(self):
        return self._config['jlpt_postfix']

    @property
    def jlpt_prefix(self):
        return self._config['jlpt_prefix']

    @property
    def grade_enabled(self):
        return self._config['grade']

    @property
    def grade_postfix(self):
        return self._config['grade_postfix']

    @property
    def grade_prefix(self):
        return self._config['grade_prefix']

    @property
    def kanji_deck_name(self):
        deck = mw.col.decks.get(self._config['did'], default=False)
        if deck is None:
            return None
        return deck['name']


class KanjiDAO():
    def __init__(self):
        pass
