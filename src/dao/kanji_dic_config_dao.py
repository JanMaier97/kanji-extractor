from ..model.kanji_config import KanjiConfig

class KanjiDicConfigDAO():
    def __init__(self):
        self._config = mw.addonManager.getConfig(__name__)['kanjidic']
        self._fields = self._config['fields']
        showInfo(f"{self._config}")

    def update_note_config(self,
                           deck_name: str, 
                           model_name: str,
                           kanji: str,
                           meaning: str,
                           onyomi: str,
                           kunyomi: str,
                           strokecount: str,
                           frequency: str,
                           radical: str) -> None:

        assert(deck_name is not None)
        assert(model_name is not None)
        assert(kanji is not None)

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
        showInfo(f"{self._config}")
        mw.addonManager.writeConfig(__name__, {'kanjidic': self._config}) 

    @property
    def model_name(self):
        model = mw.col.models.get(self._config['mid'])
        if model is None:
            return None
        return model['name']


    @property
    def kanji_deck_name(self):
        deck = mw.col.decks.get(self._config['did'], default=False)
        if deck is None:
            return None
        return deck['name']
