from aqt import mw
from aqt.qt import QMenu, QAction
from anki.hooks import addHook
from .note_manager import KanjiExtractor
from .settings import SettingsDialog
from aqt.utils import showInfo


def setup_menu():
    menu = QMenu('Kanji Exctractor', mw)
    mw.form.menuTools.addAction(menu.menuAction())
    # mw.form.menuLookup = menu

    create_action = QAction('Create Kanji Notes', mw)
    create_action.triggered.connect(create_kanji_notes)
    menu.addAction(create_action)

    settings_action = QAction('Update Kanji Notes', mw)
    settings_action.triggered.connect(open_settings)
    menu.addAction(settings_action)

    settings_action = QAction('Settings', mw)
    settings_action.triggered.connect(open_settings)
    menu.addAction(settings_action)

def setup_browser_menu(browser):
    menu = QMenu('Kanji Extractor', browser)
    browser.form.menuEdit.addAction(menu.menuAction())

    create_action = QAction("Extract Kanji", browser)
    create_action.triggered.connect(lambda: create_kanji_notes_browser(browser))
    menu.addAction(create_action)

    update_action = QAction("Update Kanji Notes", browser)
    update_action.triggered.connect(lambda: update_kanji_notes_browser(browser))
    menu.addAction(update_action)

def create_kanji_notes():
    kanjiExtractor = KanjiExtractor(None)
    kanjiExtractor.handle_notes()
    mw.reset()

def create_kanji_notes_browser(browser):
    kanji_extractor = KanjiExtractor(None)
    nids = kanji_extractor.handle_notes(browser.selectedNotes())
    mw.reset()

def update_kanji_notes():
    pass

def update_kanji_notes_browser(browser):
    pass

def open_settings():
    dialog = SettingsDialog()
    dialog.exec()

setup_menu()
addHook("browser.setupMenus", setup_browser_menu)

