import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def validate_email(email: str) -> str:
    if not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email. Example: name@example.com")
    return email
