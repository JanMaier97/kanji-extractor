from typing import List


class InvalidModelError(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name


class MissingFieldsError(Exception):
    def __init__(self, field_names: List[str]):
        self.field_names = field_names


class ConfigError(Exception):
    pass


class KanjiDAO():
    def __init__(self):
        pass
