from aqt import mw as col
from typing import List, Set, Sequence, Iterable
from ..model.kanji_note import KanjiNote
from ..exceptions import InvalidModelError
from ..model.kanji_config import KanjiConfig
from ..model.vocab_config import VocabConfig
from ..model.kanji_note import KanjiNote

class AnkiDAO():
    def __init__(self, kanji_config: KanjiConfig, vocab_config: VocabConfig):
        self._kanji_config = kanji_config
        self._vocab_config = vocab_config

    def get_deck_names(self) -> List[str]:
        return sorted(mw.col.decks.allNames(False))

    def get_model_names(self) -> List[str]:
        return sorted(mw.col.models.allNames())

    def get_model_fields(self, model_name: str) -> List[str]:
        model = mw.col.models.byName(model_name)
        if model is None:
            raise InvalidModelError(model_name)
        return mw.col.models.fieldNames(model)

    def get_missing_kanji(self) -> Iterable[str]:
        return [kanji for kanji in _get_kanji_from_vocab() - _get_existing_kanji()]

    def _get_kanji_from_vocab(self) -> Set[str]:
        query = f'mid:{self._vocab_config.model_id} {self._vocab_config.fieldMapping.expression}:_*'
        return set(expression.split() for expression in col.find_notes(query))

    def _get_existing_kanji(self) -> Set[str]:
        query = f'mid:{self._kanji_config.mid} {self._kanji_config.fieldMapping.kanji}:_*'
        notes = [col.getNote(nid) for nid in self.find_notes(query)]
        return set(note[kanji_config.fieldMapping.kanji] for note in notes)

    def find_example_words(self, character: str) -> Iterable[VocabNote]:
        query = f'mid:{self._vocab_config.model_id} {self._kanji_config.expressionField}:*{character}*'
        anki_notes = [col.getNote(nid) for nid in self.find_notes(query)]

        return [VocabNote(id = note.id,
                expression =  note[self._vocab_config.expressionField],
                meaning = note[meaningField])
                for note in anki_notes]

        vocab_notes.append(
                VocabNote(
                    id: note


    def add_notes(self, notes: Iterable[KanjiNote]) -> Iterable[int]:
        model = col.models.get(self._kanji_config.model_id)
        note_ids = []

        for kanji_note in notes:
            note = Note(col, model)

            if self._kanji_config.fieldMapping.kanji:
                note[self._kanji_config.fieldMapping.kanji] = kanji_note.kanji

            if self._kanji_config.fieldMapping.meaning:
                note[self._kanji_config.fieldMapping.meaning] = kanji_note.meaning

            if self._kanji_config.fieldMapping.kunyomi:
                note[self._kanji_config.fieldMapping.kunyomi] = kanji_note.kunyomi

            if self._kanji_config.fieldMapping.onyomi:
                note[self._kanji_config.fieldMapping.onyomi] = kanji_note.onyomi

            if self._kanji_config.fieldMapping.frequency:
                note[self._kanji_config.fieldMapping.frequency] = kanji_note.frequency

            if self._kanji_config.fieldMapping.strokecount:
                note[self._kanji_config.fieldMapping.strokecount] = kanji_note.strokecount

            if self._kanji_config.fieldMapping.radical:
                note[self._kanji_config.fieldMapping.radical] = kanji_note.radical

            col.add_note(note, self._kanji_config.deck_id)
            note_ids.append(note.id)

        return note_ids
