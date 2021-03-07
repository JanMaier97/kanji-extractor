from dataclasses import dataclass

@dataclass
class KanjiNote:
    id: int = None
    kanji:  str = None
    meaning: str = None
    onyomi: str = None
    kunyomi: str = None
    frequency: int = None
    strokecount: int = None
    radical: str = None
    dictionary_ref: str = None
    grade: int = None
    jlpt: int = None


