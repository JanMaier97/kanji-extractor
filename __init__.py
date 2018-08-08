from aqt import mw
from aqt.qt import QMenu, QAction


def create_menu():

    menu = QMenu('Kanji Exctractor', mw)
    mw.form.menuTools.addAction(menu.menuAction())
    # mw.form.menuLookup = menu

    create_action = QAction('Create Kanji Notes', mw)
    create_action.triggered.connect(create_kanji_notes)
    menu.addAction(create_action)

    settings_action = QAction('Settings', mw)
    menu.addAction(settings_action)
    create_action.triggered.connect(open_settings)


def create_kanji_notes():
    pass


def open_settings():
    pass


create_menu()
