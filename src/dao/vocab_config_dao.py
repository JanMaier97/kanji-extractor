from typing import List

class VocabConfigDAO():
    def __init__(self):
        self._config = mw.addonManager.getConfig(__name__)['vocab']

    def update_vocab_config(self, model_name: str, field_name: str) -> None:
        assert(model_name is not None)
        assert(field_name is not None)

        mid = _validate_model(model_name, [field_name])
        self._config['mid'] = mid
        self._config['field'] = field_name

    @property
    def vocab_model_name(self):
        model = mw.col.models.get(self._config['mid'])
        if model is None:
            return None
        return model['name']
    
    @property
    def vocab_field_name(self):
        return self._config['field']

    def save(self):
        mw.addonManager.writeConfig(__name__, {'vocab': self._config}) 

    def _validate_model(model_name: str, field_names: List[str]) -> int:
        assert(model_name is not None)
        assert(field_names is not None)

        model = mw.col.models.byName(model_name)
        if model is None:
            raise InvalidModelError(model_name)

        missing_fields = [field for field in field_names 
                          if field not in mw.col.models.fieldNames(model)
                          and field is not None]

        if len(missing_fields) > 0:
            raise MissingFieldsError(missing_fields)

        return model['id']
