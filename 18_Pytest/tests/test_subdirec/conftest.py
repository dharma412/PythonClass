import pytest

@pytest.fixture(scope="module")
def input_value_to_sub():
   input = 35
   yield input
   print("I sent object , I am closing testcase")