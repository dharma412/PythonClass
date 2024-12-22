import pytest


@pytest.mark.regg
def test_test1():
    print("This is first testcase")

@pytest.mark.smoke
def test_test2():
    print("This is first testcase")

@pytest.mark.sanity
@pytest.mark.smoke
def test_test3():
    print("This is first testcase")

def tes_quality():
    assert 10 == 11