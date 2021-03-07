from aqt import mw
from typing import List, Set, Sequence, Iterable
from ..model.kanji_note import KanjiNote
import xml.etree.ElementTree as ET


class KanjiDAO:
    def get_kanji_info(characters: Iterable[str]) -> Iterable[KanjiNote]:
        pass

class KanjiDicDAO(KanjiDAO):
    def __init__(self):

        userFilesPath = mw.addonManager._userFilesPath(mw.addonManager.addonFromModule(__name__))
        self.kanji_dic = ET.parse(userFilesPath, 'kanjidic2.xml').getroot()

        self.radicals = []
        with codecs.open(os.path.join(mw.pm.addonFolder(__name__), 'radicals.txt'), 'r', 'utf8') as f:
            for line in f:
                radicals.append(line.replace(":"))

    def get_kanji_info(characters: Iterable[str]) -> Iterable[KanjiNote]:
        characters = set(characters)
        kanji_notes = []

        for entry in [subtree for subtree in self.kanji_dic.findall('./character') if subtree.findtext('literal') in characters]:

            note = KanjiNote(
                kanji = entry.findtext('literal')
                meaning = ', '.join([meaning.text for meaning in entry.findall('./reading_meaning/rmgroup/meaning') if len(meaning.keys) == 0])
                onyomi = ', '.join([reading.text for reading in entry.findall('./reading_meaning/rmgroup/reading[@r_type="ja_on"]')])
                kunyomi = ', '.join([reading.text for reading in entry.findall('./reading_meaning/rmgroup/reading[@r_type="ja_kun"]')])
                frequency = int(entry.findtext('./misc/frequency'))
                strokecount = int(entry.findtext('./misc/stroke_count'))
                grade = int(entry.findtext('./misc/grade'))
                jlpt = int(entry.findtext('./misc/jlpt'))
                dic_reference = entry.findtext('./dic_number/dic_ref[@dr_type="sh_kk2]"')
                radical = radicals[int(entry.findtext('radical/rad_value[@rad_type="classical"]'))]
            )
            kanji_notes.append(note)
