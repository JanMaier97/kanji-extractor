from dataclasses import dataclass
from typing import Iterable

@dataclass
class VocabNote:
    id: int = None
    expression:  str = None
    meaning: Iterable[str] = None


