from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo
from .forms.settings import Ui_Settings 
from .dao.anki_dao import AnkiDAO
from .dao.kanji_dic_config_dao import KanjiDicConfigDAO
from .dao.vocab_config_dao import VocabConfigDAO


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self._UNSELECTED_FIELD_TEXT = "---"
        self._anki_dao = AnkiDAO()
        self._vocab_config = VocabConfigDAO()
        self._kanji_config = KanjiDicConfigDAO()

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
        sender.setText(self._anki_dao.strip_tag(sender.text()))
        
    def _setup_tags(self):
        self.ui.jlpt_prefix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.jlpt_postfix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.grade_prefix_line.editingFinished.connect(self._on_tag_line_edited)
        self.ui.grade_postfix_line.editingFinished.connect(self._on_tag_line_edited)

    def _setup_vocab(self):
        self.ui.vocab_model.currentTextChanged.connect(self._on_vocab_model_changed)
        self.ui.vocab_model.addItems(self._anki_dao.get_model_names())

    def _on_vocab_model_changed(self, model_name):
        self.ui.vocab_field.clear()
        self.ui.vocab_field.addItems(self._anki_dao.get_model_fields(model_name))

    def _on_kanji_model_changed(self, model_name):
        for cb in self._kanji_field_cbs:
            cb.activated.emit(cb.currentIndex())

    def _setup_kanji(self):
        self.ui.kanji_model.activated.connect(self._on_kanji_model_changed)
        for cb in self._kanji_field_cbs:
            cb.activated.connect(self.on_kanji_cb_activated)
            if not cb is self.ui.cb_kanji:
                cb.insertItem(0, self._UNSELECTED_FIELD_TEXT)

        self.ui.kanji_model.addItems(self._anki_dao.get_model_names())
        self.ui.kanji_deck.addItems(self._anki_dao.get_deck_names())


    def _save_config(self):
        try:
            self._check_config()
        except ConfigSaveError as e:
            showInfo(e.message + "\nPlease check your settings.")
            return

        self._vocab_config.update_vocab_config(self._get_selected_field(self.ui.vocab_model),
                                               self._get_selected_field(self.ui.vocab_field))

        self._kanji_config.update_note_config(self._get_selected_field(self.ui.kanji_deck),
                                              self._get_selected_field(self.ui.kanji_model),
                                              self._get_selected_field(self.ui.cb_kanji),
                                              self._get_selected_field(self.ui.cb_meaning),
                                              self._get_selected_field(self.ui.cb_onyomi),
                                              self._get_selected_field(self.ui.cb_kunyomi),
                                              self._get_selected_field(self.ui.cb_strokecount),
                                              self._get_selected_field(self.ui.cb_frequency),
                                              self._get_selected_field(self.ui.cb_radical))

        self._kanji_config.update_grade_tag(self.ui.grade_check.checkState() ,
                                            self.ui.grade_prefix_line.text(),
                                            self.ui.grade_postfix_line.text())

        self._kanji_config.update_jlpt_tag(self.ui.jlpt_check.checkState(),
                                           self.ui.jlpt_prefix_line.text(),
                                           self.ui.jlpt_postfix_line.text())

        self._vocab_config.save()
        self._kanji_config.save()

        self.accept()

    def _check_config(self):
        if self.ui.jlpt_check.checkState() and not (self.ui.jlpt_prefix_line.text() + self.ui.jlpt_postfix_line.text()):
            raise ConfigSaveError("The postfix and prefix for the JLPT tags cannot be empty.")

        if self.ui.grade_check.checkState() and not (self.ui.grade_prefix_line.text() + self.ui.grade_postfix_line.text()):
            raise ConfigSaveError("The postfix and prefix for the kanji grade tags cannot be empty.")

    def on_kanji_cb_activated(self, index):
        for cb in self._kanji_field_cbs:
            currentText = cb.currentText()
            is_optional = cb.itemText(0) == self._UNSELECTED_FIELD_TEXT

            fields = self._get_selectable_kanji_fields(currentText)

            if is_optional:
                fields = [self._UNSELECTED_FIELD_TEXT] + fields

            cb.clear()
            cb.addItems(fields)
            cb.setCurrentText(currentText)


    def _load_config(self):
        vocab_model_name = self._vocab_config.vocab_model_name
        if not vocab_model_name is None:
            self.ui.vocab_model.setCurrentText(vocab_model_name)

        deck_name = self._kanji_config.kanji_deck_name
        if not deck_name is None:
            self.ui.kanji_deck.setCurrentText(deck_name)

        kanji_model_name = self._kanji_config.model_name
        if kanji_model_name is None:
            showInfo('Could not find the note type for the kanji notes.\nPlease check your configuration.')
        else:
            for cb in self._kanji_field_cbs:
                cb.addItems(_anki_dao.get_model_fields(kanji_model_name))
                cb.setCurrentIndex(0)

            self.ui.kanji_model.setCurrentText(kanji_model_name)

            if self._kanji_config.kanji:
                self._set_kanji_field(self.ui.cb_kanji, self._kanji_config.kanji)

            if self._kanji_config.meaning:
                self._set_kanji_field(self.ui.cb_meaning, self._kanji_config.meaning)

            if self._kanji_config.onyomi:
                self._set_kanji_field(self.ui.cb_onyomi, self._kanji_config.onyomi)

            if self._kanji_config.kunyomi:
                self._set_kanji_field(self.ui.cb_kunyomi, self._kanji_config.kunyomi)

            if self._kanji_config.strokecount:
                self._set_kanji_field(self.ui.cb_strokecount, self._kanji_config.strokecount)

            if self._kanji_config.radical:
                self._set_kanji_field(self.ui.cb_radical, self._kanji_config.radical)

            if self._kanji_config.frequency:
                self._set_kanji_field(self.ui.cb_frequency, self._kanji_config.frequency)
        
        self.on_kanji_cb_activated(0)

        self.ui.jlpt_check.setCheckState(self._kanji_config.jlpt_enabled)
        self.ui.jlpt_prefix_line.setText(self._kanji_config.jlpt_prefix)
        self.ui.jlpt_postfix_line.setText(self._kanji_config.jlpt_postfix)

        self.ui.grade_check.setCheckState(self._kanji_config.grade_enabled)
        self.ui.grade_prefix_line.setText(self._kanji_config.grade_prefix)
        self.ui.grade_postfix_line.setText(self._kanji_config.grade_postfix)

    def _set_kanji_field(self, kanji_cb, field_text):
        if kanji_cb.findText(field_text) == -1:
            showInfo('Could not find the field "{0}" for the note type "{1}".\nPlease update your configuration.'.format(field_text, self.ui.kanji_model.currentText()))
        else:
            kanji_cb.setCurrentText(field_text)


    def _get_selectable_kanji_fields(self, additional_item):
        all_fields = self._anki_dao.get_model_fields(self.ui.kanji_model.currentText())
         
        selected_fields = [cb.currentText() for cb in self._kanji_field_cbs]
        selected_fields.remove(additional_item)
        return [field for field in all_fields if not field in selected_fields]

    def _get_selected_field(self, combo_box):
        field = combo_box.currentText()
        if field == self._UNSELECTED_FIELD_TEXT:
            return None
        return field

class ConfigLoadError(Exception):
    def __init__(self, message):
        self.message = message

class ConfigSaveError(Exception):
    def __init__(self, message):
        self.message = message
