from aqt import mw
from aqt.utils import showInfo


class NoteManager():
    def __init__(self, note_writer):
        self._note_writer = note_writer
        self._config = mw.addonManager.getConfig(__name__)['common']

    def extract_kanji(self, vocab_nids):
        new_kanji = set()

        for nid in vocab_nids:
            note = mw.col.getNote(nid)

            for character in note[self._config['expression_field']]:
                if self._is_kanji(character) and not self._already_exists(character):
                    new_kanji.add(character)

        for kanji in new_kanji:
            note = mw.col.newNote()

            self._note_writer.write_note(kanji, note)
            note.flush()
            mw.col.addNote(note)
        


    """
    Returns True if the given character is a kanji.

    The check is done using the unicode ranges found here:
    https://stackoverflow.com/questions/19899554/unicode-range-for-japanese
    http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
    """
    def _is_kanji(sef, character):
        char_code = ord(character)
        return (0x3400 <= char_code <= 0x4DB5) or (0x4E00 <= char_code <= 0xF9CB) or (0xF900 <= 0xFA6a)

    def _already_exists(self, kanji):
        nids = mw.col.findNotes('mid:' + str(self._config['kanji_mid']) + ' ' + self._config['kanji_field'] + ' ' + kanji)

        if len(nids) == 0:
            return True
        else:
            return False

