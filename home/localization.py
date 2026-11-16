from copy import deepcopy


def localized_copy(source, translations):
    result = deepcopy(source)
    return _merge(result, translations)


def _merge(target, translations):
    if isinstance(target, dict):
        if not isinstance(translations, dict):
            raise TypeError("Translation structure does not match the source.")
        for key, value in translations.items():
            if key not in target:
                raise KeyError(f"Unknown translation key: {key}")
            target[key] = _merge(target[key], value)
        return target

    if isinstance(target, list):
        if not isinstance(translations, list) or len(target) != len(translations):
            raise ValueError("Translation list does not match the source structure.")
        return [
            _merge(source_item, translated_item)
            for source_item, translated_item in zip(target, translations)
        ]

    return translations