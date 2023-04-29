import pytest
def test_001():
    x=input('Press Enter if CLAMP15 is OFF: ')
    assert x == "", "Test Failed check CLAMP15" 
    y=input('Press Enter if CLAMP15 is ON: ')
    assert y == "", "Test Failed check CLAMP15"