import pytest

from services import contains_punctuation


# write using parametrize
@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, world!", True),
        ("Hello world", False),
        ("", False),
        ("     ", False),
        ("!", True),
        ("A", False),
        (" ", False),
        ("Hello, world! How are you?", True),
        ("Hello, world! How are you", True),
        ("Hello world! How are you", True),
        ("Hello world How are you", False),
        ('4234234', False),
        ('0', False),
    ],
)
def test_contains_punctuation(text, expected):
    assert contains_punctuation(text) == expected
