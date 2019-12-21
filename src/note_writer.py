import abc

class NoteWriter(abc.ABC):

    @abc.abstractmethod
    def write_note(self, kanji, note):
        pass

    @abc.abstractmethod
    def check_config(self):
        pass


class KanjiDicNoteWriter(NoteWriter):

    def write_note(sef, kanji, note):
        pass

    def check_config(self):
        pass


class ExampleWordNoteWriter(NoteWriter):

    def write_note(sef, kanji, note):
        pass

    def check_config(self):
        pass


class AdditionalTagNoteWriter(NoteWriter):

    def write_note(sef, kanji, note):
        pass

    def check_config(self):
        pass
