from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo
from .forms.settings import Ui_Settings 


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = Ui_Settings()

        self.ui.setupUi(self)
        self._setup_ui()
        self._config = mw.addonManager.getConfig(__name__)
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
        pass

    def _setup_kanji(self):
        self.ui.kanji_model.currentTextChanged.connect(self._on_kanji_model_changed)
        self.ui.kanji_model.addItems(sorted(mw.col.models.allNames()))
        self.ui.kanji_deck.addItems(sorted(mw.col.decks.allNames(False)))


    def _save_config(self):
        self._config['common']['vocab_mid'] = mw.col.models.byName(self.ui.vocab_model.currentText())['id']
        self._config['common']['vocab_field'] = self.ui.vocab_field.currentText()

        self._config['common']['kanji_mid'] = mw.col.models.byName(self.ui.kanji_model.currentText())['id']
        self._config['common']['deck_id'] = mw.col.decks.byName(self.ui.kanji_deck.currentText())['id']

        mw.addonManager.writeConfig(__name__, self._config)
        self.accept()


    def _load_config(self):
        vocab_model = mw.col.models.get(self._config['common']['vocab_mid'])
        if not vocab_model is None:
            self.ui.vocab_model.setCurrentText(vocab_model['name'])

        kanji_model = mw.col.models.get(self._config['common']['kanji_mid'])
        if not kanji_model is None:
            self.ui.kanji_model.setCurrentText(kanji_model['name'])

        deck = mw.col.decks.get(self._config['common']['deck_id'], default=False)
        if not deck is None:
            self.ui.kanji_deck.setCurrentText(deck['name'])



class ConfigLoadError(Exception):
    def __init__(self, message):
        self.message = message

