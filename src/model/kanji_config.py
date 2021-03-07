from dataclasses import dataclass

@dataclass
class KanjiFieldConfig():
    kanji: str
    meaning: str
    onyomi: str
    kunyomi: str
    strokecount: str
    frequency: str
    radical: str

@dataclass
class TagConfig():
    enabled: bool
    prefix: str
    postfix: str

@dataclass
class KanjiConfig():
    deck_id: int
    model_id: int
    fieldMapping: KanjiFieldConfig
    gradeTag: TagConfig
    jlptTag: TagConfig



