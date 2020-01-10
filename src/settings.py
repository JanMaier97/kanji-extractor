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
        self._setup_tags()

        self.ui.apply_btn.clicked.connect(self._save_config)
        self.ui.cancel_btn.clicked.connect(self.reject)

    def _on_tag_line_edited(self):
        sender = self.sender()
        currentText = sender.text().strip()
        sender.setText(currentText if currentText == "" else mw.col.tags.split(currentText)[0])
        
    def _setup_tags(self):
        self.ui.jlpt_prefix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.jlpt_postfix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.grade_prefix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.grade_postfix_line.editingFinished.connect(self._on_tag_line_edited)

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
            if not cb is self.ui.cb_kanji:
                cb.insertItem(0, '----')

        self.ui.kanji_model.addItems(sorted(mw.col.models.allNames()))
        self.ui.kanji_deck.addItems(sorted(mw.col.decks.allNames(False)))


    def _save_config(self):
        try:
            self._check_config()
        except ConfigSaveError as e:
            showInfo(e.message + "\nPlease check your settings.")
            return

        self._config['common']['vocab_mid'] = mw.col.models.byName(self.ui.vocab_model.currentText())['id']
        self._config['common']['vocab_field'] = self.ui.vocab_field.currentText()

        self._config['common']['kanji_mid'] = mw.col.models.byName(self.ui.kanji_model.currentText())['id']
        self._config['common']['kanji'] = self.ui.cb_kanji.currentText()
        self._config['common']['deck_id'] = mw.col.decks.byName(self.ui.kanji_deck.currentText())['id']

        self._config['kanjidic']['mid'] = self._config['common']['kanji_mid']
        self._config['kanjidic']['kanji'] = self.ui.cb_kanji.currentText()
        self._config['kanjidic']['meaning'] = self.ui.cb_meaning.currentText()
        self._config['kanjidic']['onyomi'] = self.ui.cb_onyomi.currentText()
        self._config['kanjidic']['kunyomi'] = self.ui.cb_kunyomi.currentText()
        self._config['kanjidic']['strokecount'] = self.ui.cb_strokecount.currentText()
        self._config['kanjidic']['frequency'] = self.ui.cb_frequency.currentText()
        self._config['kanjidic']['radical'] = self.ui.cb_radical.currentText()

        self._config['kanjidic']['grade'] = self.ui.grade_check.checkState()
        self._config['kanjidic']['grade_prefix'] = self.ui.grade_prefix_line.text()
        self._config['kanjidic']['grade_postfix'] = self.ui.grade_postfix_line.text()

        self._config['kanjidic']['jlpt'] = self.ui.jlpt_check.checkState()
        self._config['kanjidic']['jlpt_prefix'] = self.ui.jlpt_prefix_line.text()
        self._config['kanjidic']['jlpt_postfix'] = self.ui.jlpt_postfix_line.text()

        mw.addonManager.writeConfig(__name__, self._config)
        self.accept()

    def _check_config(self):
        if self.ui.jlpt_check.checkState() and not (self.ui.jlpt_prefix_line.text() + self.ui.jlpt_postfix_line.text()):
            raise ConfigSaveError("The postfix and prefix for the JLPT tags cannot be empty.")

        if self.ui.grade_check.checkState() and not (self.ui.grade_prefix_line.text() + self.ui.grade_postfix_line.text()):
            raise ConfigSaveError("The postfix and prefix for the kanji grade tags cannot be empty.")

    def on_kanji_cb_activated(self, index):
        for cb in self._kanji_field_cbs:
            currentText = cb.currentText()
            is_optional = cb.itemText(0) == '----'

            fields = self._get_selectable_kanji_fields(currentText)

            if is_optional:
                fields = ['----'] + fields

            cb.clear()
            cb.addItems(fields)
            cb.setCurrentText(currentText)


    def _load_config(self):
        vocab_model = mw.col.models.get(self._config['common']['vocab_mid'])
        if not vocab_model is None:
            self.ui.vocab_model.setCurrentText(vocab_model['name'])

        deck = mw.col.decks.get(self._config['common']['deck_id'], default=False)
        if not deck is None:
            self.ui.kanji_deck.setCurrentText(deck['name'])

        kanji_model = mw.col.models.get(self._config['kanjidic']['mid'])
        if kanji_model is None:
            showInfo('Could not find the note type with the id "{0}" for the kanji notes.\nPlease check your configuration.'.format(self._config['kanjidic']['mid']))
        else:

            for cb in self._kanji_field_cbs:
                cb.addItems(mw.col.models.fieldNames(kanji_model))
                cb.setCurrentIndex(0)

            self.ui.kanji_model.setCurrentText(kanji_model['name'])

            if self._config['kanjidic']['kanji']:
                self._set_kanji_field(self.ui.cb_kanji, self._config['kanjidic']['kanji'])
            if self._config['kanjidic']['meaning']:
                self._set_kanji_field(self.ui.cb_meaning, self._config['kanjidic']['meaning'])
            if self._config['kanjidic']['onyomi']:
                self._set_kanji_field(self.ui.cb_onyomi, self._config['kanjidic']['onyomi'])
            if self._config['kanjidic']['kunyomi']:
                self._set_kanji_field(self.ui.cb_kunyomi, self._config['kanjidic']['kunyomi'])
            if self._config['kanjidic']['strokecount']:
                self._set_kanji_field(self.ui.cb_strokecount, self._config['kanjidic']['strokecount'])
            if self._config['kanjidic']['radical']:
                self._set_kanji_field(self.ui.cb_radical, self._config['kanjidic']['radical'])
            if self._config['kanjidic']['frequency']:
                self._set_kanji_field(self.ui.cb_frequency, self._config['kanjidic']['frequency'])
        
        self.on_kanji_cb_activated(0)


        self.ui.jlpt_check.setCheckState(self._config['kanjidic']['jlpt'])
        self.ui.jlpt_prefix_line.setText(self._config['kanjidic']['jlpt_prefix'])
        self.ui.jlpt_postfix_line.setText(self._config['kanjidic']['jlpt_postfix'])

        self.ui.grade_check.setCheckState(self._config['kanjidic']['grade'])
        self.ui.grade_prefix_line.setText(self._config['kanjidic']['grade_prefix'])
        self.ui.grade_postfix_line.setText(self._config['kanjidic']['grade_postfix'])

    def _set_kanji_field(self, kanji_cb, field_text):
        if kanji_cb.findText(field_text) == -1:
            showInfo('Could not find the field "{0}" for the note type "{1}".\nPlease update your configuration.'.format(field_text, self.ui.kanji_model.currentText()))
        else:
            kanji_cb.setCurrentText(field_text)


    def _get_selectable_kanji_fields(self, additional_item):
        all_fields = mw.col.models.fieldNames(mw.col.models.byName(self.ui.kanji_model.currentText()))
         
        selected_fields = [cb.currentText() for cb in self._kanji_field_cbs]
        selected_fields.remove(additional_item)
        return [field for field in all_fields if not field in selected_fields]


class ConfigLoadError(Exception):
    def __init__(self, message):
        self.message = message

class ConfigSaveError(Exception):
    def __init__(self, message):
        self.message = message
