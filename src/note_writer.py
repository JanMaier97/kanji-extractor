from os import path
import abc
import xml.etree.ElementTree as ET
from aqt.utils import showInfo
from aqt import mw

KANJIDIC2_PATH = path.join(path.dirname(path.abspath(__file__)), "user_files", "kanjidic2.xml")
RADICALS_PATH = path.join(path.dirname(path.abspath(__file__)), "classical_radicals.txt")


class NoteWriter(abc.ABC):

    @abc.abstractmethod
    def write_note(self, kanji, note):
        pass

    @abc.abstractmethod
    def check_config(self):
        pass


class KanjiDicNoteWriter(NoteWriter):
    def __init__(self):
        tree = ET.parse(KANJIDIC2_PATH)
        self._root = tree.getroot()
        self._config = mw.addonManager.getConfig(__name__)['kanjidic']

        with open(RADICALS_PATH, mode='r', encoding='utf-8') as f:
            self._radicals = [line.rstrip('\n') for line in f]

    def write_note(self, kanji, note):
        literal_tree = self._get_subtree(kanji)
        note[self._config['kanji']] = kanji
        
        if self._config['meaning']:
            note[self._config['meaning']] = self._get_meaning(literal_tree)

        if self._config['onyomi']:
            note[self._config['onyomi']] = self._get_onyomi(literal_tree)

        if self._config['kunyomi']:
            note[self._config['kunyomi']] = self._get_kunyomi(literal_tree)

        if self._config['strokecount']:
            note[self._config['strokecount']] = self._get_strokecount(literal_tree)

        if self._config['frequency']:
            note[self._config['frequency']] = self._get_frequency(literal_tree)

        if self._config['radical']:
            note[self._config['radical']] = self._get_radical(literal_tree)

        if self._config['grade']:
            note.addTag(self._get_grade_tag(literal_tree))
    
        if self._config['jlpt']:
            note.addTag(self._get_jlpt_tag(literal_tree))


    def check_config(self):
        pass

    def _get_subtree(self, kanji):
        character_trees = self._root.findall("./character[literal='{0}']".format(kanji))
        if len(character_trees) == 0:
            raise KanjiParseError("Could not find the literal '{0}'".format(kanji))
        if len(character_trees) > 1:
            raise KanjiParseError("Found multiple entries for the literal '{0}".format(kanji))
        return character_trees[0]

    def _get_radical(self, subtree):
        rad_index = int(self._get_tag_content(subtree, "./radical/rad_value[@rad_type='classical']")[0]) - 1
        return self._radicals[rad_index]

    def _get_jlpt_tag(self, subtree):
        content = self._get_tag_content(subtree, "./misc/jlpt") 
        if content == []:
            return ""
        return self._config['jlpt_prefix'] + content[0] + self._config('jlpt_postfix')

    def _get_grade_tag(self, subtree):
        content = self._get_tag_content(subtree, "./misc/grade")
        if content == []:
            return ""
        return self._config['grade_prefix'] + content[0] + self._config['grade_postfix']

    def _get_frequency(self, subtree):
        content = self._get_tag_content(subtree, "./misc/freq")
        if content == []:
            return ""
        return content[0]

    def _get_tag_content(self, subtree, xpath):
        tags = subtree.findall(xpath)
        return [tag.text for tag in tags]

    def _get_onyomi(self, subtree):
        content = self._get_tag_content(subtree, "./reading_meaning/rmgroup/reading[@r_type='ja_on']")
        if content == []:
            return ""
        return " ,".join(content)

    def _get_kunyomi(self, subtree):
        content = self._get_tag_content(subtree, "./reading_meaning/rmgroup/reading[@r_type='ja_kun']")
        if content == []:
            return ""
        return ", ".join(content)

    def _get_meaning(self, subtree):
        tags = subtree.findall("./reading_meaning/rmgroup/meaning")
        meanings = [tag.text for tag in tags if len(tag.attrib) == 0]
        if meanings == []:
            return ""
        return ", ".join(meanings)

    def _get_strokecount(self, subtree):
        return self._get_tag_content(subtree, "./misc/stroke_count")[0]


class NoteWriterDecorator(NoteWriter):
    def __init__(self, decorated_note_writer):
        self.decorated_note_writer = decorated_note_writer

    def write_note(self, kanji, note):
        self.decorated_note_writer.write_note(kanji, note)

    def check_config(self):
        self.decorated_note_writer.check_config()

class ExampleWordNoteWriter(NoteWriterDecorator):
    def __init__(self, decorated_note_writer):
        super(ExampleWordNoteWriter, self).__init__(decorated_note_writer)

    def write_note(sef, kanji, note):
        pass

    def check_config(self):
        pass


class AdditionalTagNoteWriter(NoteWriterDecorator):

    def write_note(sef, kanji, note):
        pass

    def check_config(self):
        pass


class KanjiParseError(Exception):
    def __init__(self, message):
        self.message = message
