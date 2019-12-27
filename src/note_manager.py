import re
import abc
from aqt import mw
from anki.utils import ids2str
from aqt.utils import showInfo
from anki.notes import Note


""" From https://stackoverflow.com/questions/19899554/unicode-range-for-japanese and
    http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
"""
KANJI_PATTERN = r'[\u3400-\u4DB5\u4E00-\uF9CB\uF900-\uFA6a]'

class NoteManager(abc.ABC):
    @abc.abstractmethod
    def handle_notes(self, nids=None):
        pass

class KanjiExtractor(NoteManager):
    def __init__(self, note_writer):
        self._note_writer = note_writer
        self._config = mw.addonManager.getConfig(__name__)['common']

    def handle_notes(self, nids = None):
        if nids is None:
            nids = mw.col.findNotes('mid:' + str(self._config['vocab_mid']) + ' is:new card:1')

        if (nids == []):
            return []

        self._check_nids(nids)

        new_kanji = self._extract_new_kanji(nids)

        if (new_kanji == []):
            return []

        new_nids = self._create_notes(new_kanji)

        self._move_cards(new_nids)
        return nids

    def _check_nids(self, nids):
        mids = mw.col.db.list("select distinct mid from notes where id in " + ids2str(nids))
        if len(mids) == 0:
            raise NoteSelectionError("No Kanji notes have been selected.")
        if len(mids) > 1:
            raise NoteSelectionError("The selected notes contain multiple note types.")
        if not str(mids[0]) == self._config['vocab_mid']:
            raise NoteSelectionError("The selected notes do not use the specified note type.")

    def _create_notes(self, kanji_characters):
        note_model = mw.col.models.get(self._config['kanji_mid'])
        nids = []

        for kanji in kanji_characters:
            note = Note(mw.col, note_model)

            self._note_writer.write_note(kanji, note)

            mw.col.addNote(note)
            nids.append(note.id)

        return nids

    def _move_cards(self, nids):
        cids = mw.col.db.list("select id from cards where nid in "+ ids2str(nids))
        mw.col.decks.setDeck(cids, self._config['deck_id'])

    def _extract_new_kanji(self, vocab_nids):
        new_kanji = set()

        for nid in vocab_nids:
            note = mw.col.getNote(nid)
            for character in self._extract_kanji(note[self._config['vocab_field']]):
                if not self._already_exists(character):
                    new_kanji.add(character)

        return new_kanji


    def _extract_kanji(self, string):
        return re.findall(KANJI_PATTERN, string) 

    def _already_exists(self, kanji):
        nids = mw.col.findNotes('mid:' + str(self._config['kanji_mid']) + ' ' + self._config['kanji_field'] + ':' + kanji)

        if len(nids) == 0:
            return False
        else:
            return True


class KanjiUpdater(NoteManager):
    def __init__(self):
        pass

    def handle_notes(self):
        pass

    def handle_notes(self, nids):
        pass


class NoteSelectionError(Exception):
    def __init__(self, message):
        self.message = message
