from dataclasses import dataclass

@dataclass
class VocabConfig():
    model_id: int
    expressionField: str
    meaningField: str


