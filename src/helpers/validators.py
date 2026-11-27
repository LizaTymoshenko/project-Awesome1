import re

# ASCII only: \w would also accept Cyrillic and other Unicode letters.
# fullmatch, not match: "$" lets a trailing newline through.
LOCAL_PART = r"[A-Za-z0-9]+(?:[._+-][A-Za-z0-9]+)*"
DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
EMAIL_PATTERN = re.compile(rf"{LOCAL_PART}@(?:{DOMAIN_LABEL}\.)+[A-Za-z]{{2,}}")
MAX_EMAIL_LENGTH = 254


def validate_email(email: str) -> str:
    if len(email) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email. Example: name@example.com")
    return email
