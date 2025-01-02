import pytest


def test_first(input_value_to_sub):
    print(input_value_to_sub)
    print("I am first sub test")

def test_second(input_value_to_sub):
    print(input_value_to_sub*2)
    print("I am second sub test")

def test_third(input_value_to_sub):
    print(input_value_to_sub*3)
    print("I am Third sub Testcase")

def test_fourth(input_value):
    print(input_value*4)
    print("I am 4th sub testcase")