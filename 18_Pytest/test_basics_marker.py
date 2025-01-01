import pytest


@pytest.mark.santy1
@pytest.mark.sanity2
def test_test1_my():
    print("This is first testcase")

@pytest.mark.smoke
def test_test2_my():
    print("This is first testcase")

@pytest.mark.sanity
@pytest.mark.smoke

def test_test3_my():
    print("This is first testcase")

def test_quality():
    assert 10 == 10