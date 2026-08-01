import pytest
from model.utils import is_allowed_file, generate_unique_filename

def test_is_allowed_file():
    assert is_allowed_file("sample.jpg") is True
    assert is_allowed_file("cell.PNG") is True
    assert is_allowed_file("blood.jpeg") is True
    assert is_allowed_file("report.pdf") is False
    assert is_allowed_file("script.py") is False
    assert is_allowed_file("no_extension") is False

def test_generate_unique_filename():
    name1 = generate_unique_filename("test.jpg")
    name2 = generate_unique_filename("test.jpg")
    assert name1 != name2
    assert name1.endswith("test.jpg")
