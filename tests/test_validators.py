import pytest

from validators import validate_email

VALID = [
    "bob@mail.com",
    "bob.smith+tag@mail.example.com",
    "b_o-b@sub.mail.co.uk",
    "BOB@MAIL.COM",
    "a1@x1.io",
]

INVALID = [
    "bob@",
    "bob@mail",
    "@mail.com",
    "bob@@mail.com",
    "bob@mail.c",
    "bob@mail.c0m",
    "bob@.com",
    "bob@mail..com",
    "bob@-mail.com",
    "bob@mail-.com",
    "bob@mail_x.com",
    "bob..x@mail.com",
    ".bob@mail.com",
    "bob.@mail.com",
    "боб@mail.com",
    "bob@пошта.com",
    "bob@mail.com\n",
    "a" * 250 + "@mail.com",
]


@pytest.mark.parametrize("email", VALID)
def test_valid_email_is_returned_unchanged(email):
    assert validate_email(email) == email


@pytest.mark.parametrize("email", INVALID)
def test_invalid_email_is_rejected_with_example(email):
    with pytest.raises(ValueError, match="name@example.com"):
        validate_email(email)
