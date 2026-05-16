from pydantic import ValidationError


def normalize_validation_error(error: ValidationError) -> list[dict]:
    normalized = []
    for item in error.errors():
        normalized_item = dict(item)
        if "ctx" in normalized_item:
            normalized_item["ctx"] = {
                key: str(value) for key, value in normalized_item["ctx"].items()
            }
        normalized.append(normalized_item)
    return normalized
