from datetime import date, datetime

def parse_date(value: str) -> date:
    if not value:
        raise ValueError('value is required')
    
    try:
        if 'T' in value:
            return datetime.fromisoformat(value).date()
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f'{value} is not a valid date')