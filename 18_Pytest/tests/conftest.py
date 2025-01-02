import pytest

@pytest.fixture(scope='module')
def input_value():
   input = 36
   return input
