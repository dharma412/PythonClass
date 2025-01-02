import pytest
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        print(1 / 0)