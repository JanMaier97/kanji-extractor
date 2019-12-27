from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo
from .forms.settings import Ui_Settings 



class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.ui = Ui_Settings()
        self._config = mw.addonManager.getConfig(__name__)
        self.ui.setupUi(self)

        self._kanji_field_cbs = [
                self.ui.cb_kanji,
                self.ui.cb_onyomi,
                self.ui.cb_kunyomi,
                self.ui.cb_meaning,
                self.ui.cb_radical,
                self.ui.cb_frequency,
                self.ui.cb_strokecount
                ]

        self._setup_ui()
        self._load_config()

    def _setup_ui(self):
        self._setup_vocab()
        self._setup_kanji()

        self.ui.apply_btn.clicked.connect(self._save_config)
        self.ui.cancel_btn.clicked.connect(self.reject)
        

    def _setup_vocab(self):
        self.ui.vocab_model.currentTextChanged.connect(self._on_vocab_model_changed)
        self.ui.vocab_model.addItems(sorted(mw.col.models.allNames()))

    def _on_vocab_model_changed(self, model_name):
        self.ui.vocab_field.clear()
        self.ui.vocab_field.addItems(mw.col.models.fieldNames(mw.col.models.byName(model_name)))

    def _on_kanji_model_changed(self, model_name):
        for cb in self._kanji_field_cbs:
            cb.activated.emit(cb.currentIndex())

    def _setup_kanji(self):
        self.ui.kanji_model.activated.connect(self._on_kanji_model_changed)
        for cb in self._kanji_field_cbs:
            cb.activated.connect(self.on_kanji_cb_activated)

        self.ui.kanji_model.addItems(sorted(mw.col.models.allNames()))
        self.ui.kanji_deck.addItems(sorted(mw.col.decks.allNames(False)))


    def _save_config(self):
        self._config['common']['vocab_mid'] = mw.col.models.byName(self.ui.vocab_model.currentText())['id']
        self._config['common']['vocab_field'] = self.ui.vocab_field.currentText()

        self._config['common']['kanji_mid'] = mw.col.models.byName(self.ui.kanji_model.currentText())['id']
        self._config['common']['deck_id'] = mw.col.decks.byName(self.ui.kanji_deck.currentText())['id']

        mw.addonManager.writeConfig(__name__, self._config)
        self.accept()

    def update_items(self, cb, requried=False):
        currentText = cb.currentText()
        cb.clear()
        fields = set(sorted(self._get_selectable_kanji_fields() + [currentText]))
        if not requried:
            fields.insert(0, '----')

        cb.addItems(fields)
        cb.setCurrentText(currentText)

    def on_kanji_cb_activated(self, index):
        for cb in self._kanji_field_cbs:
            if cb == self.ui.cb_kanji:
                self.update_items(cb, True)
            else:
                self.update_items(cb)


    def _load_config(self):
        vocab_model = mw.col.models.get(self._config['common']['vocab_mid'])
        if not vocab_model is None:
            self.ui.vocab_model.setCurrentText(vocab_model['name'])

        deck = mw.col.decks.get(self._config['common']['deck_id'], default=False)
        if not deck is None:
            self.ui.kanji_deck.setCurrentText(deck['name'])

        kanji_model = mw.col.models.get(self._config['kanjidic']['mid'])
        if not kanji_model is None:
            self.ui.kanji_model.setCurrentText(kanji_model['name'])

            if not self._config['kanjidic']['kanji']:
                self.ui.cb_kanji.addItems([self._config['kanjidic']['kanji']])
            if not self._config['kanjidic']['meaning']:
                self.ui.cb_meaning.addItems([self._config['kanjidic']['meaning']])
            if not self._config['kanjidic']['onyomi']:
                self.ui.cb_onyomi.addItems([self._config['kanjidic']['onyomi']])
            if not self._config['kanjidic']['kunyomi']:
                self.ui.cb_kunyomi.addItems([self._config['kanjidic']['kunyomi']])
            if not self._config['kanjidic']['strokecount']:
                self.ui.cb_strokecount.addItems([self._config['kanjidic']['strokecount']])
            if not self._config['kanjidic']['radical']:
                self.ui.cb_radical.addItems([self._config['kanjidic']['radical']])
            if not self._config['kanjidic']['frequency']:
                self.ui.cb_frequency.addItems([self._config['kanjidic']['frequency']])

        for cb in self._kanji_field_cbs:
            cb.activated.emit(0)

    def _get_selectable_kanji_fields(self):
        all_fields = mw.col.models.fieldNames(mw.col.models.byName(self.ui.kanji_model.currentText()))
        selected_fields = [cb.currentText() for cb in self._kanji_field_cbs]
        return [field for field in all_fields if not field in selected_fields]



class ConfigLoadError(Exception):
    def __init__(self, message):
        self.message = message

