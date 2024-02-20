import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.cycle import Cycle

def test_isLeap():
    cycle=Cycle(['21','21','2021'])

    assert cycle.isLeap(2000)==True
    assert cycle.isLeap(2012)==True
    assert cycle.isLeap(1900)==False