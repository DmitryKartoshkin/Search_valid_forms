import re
from datetime import datetime


async def validate_date_format(string: str):
    try:
        datetime.strptime(string, "%d.%m.%Y")
        return True
    except ValueError:
        try:
            datetime.strptime(string, "%Y-%m-%d")
            return True
        except ValueError:
            return False


async def validate_email_format(string: str):
    return re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', string)


async def validate_phone_format(string: str):
    return re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', string)


async def get_type(value: str) -> str:
    if await validate_email_format(value):
        return "email"
    elif await validate_phone_format(value):
        return "phone"
    elif await validate_date_format(value):
        return "date"
    else:
        return "text"
