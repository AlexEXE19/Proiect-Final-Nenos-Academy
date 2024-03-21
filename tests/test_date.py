import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.module import is_leap

def test_is_leap():
    assert is_leap(2000) == True
    assert is_leap(2012) == True
    assert is_leap(1900) == False