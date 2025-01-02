import pytest

@pytest.fixture
def input_value_to_sub():
   input = 35
   yield input

   print("I sent object , I am closing testcase")