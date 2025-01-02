import pytest

@pytest.fixture(scope="class")
def resource_setup():
    # Setup code: runs once before any tests in the class
    print("\n[Setup] Initializing resource")
    resource = {"data": 42}
    yield resource
    # Teardown code: runs once after all tests in the class
    print("\n[Teardown] Cleaning up resource")

class TestExample:
    def test_case1(self, resource_setup):
        assert resource_setup["data"] == 42

    def test_case2(self, resource_setup):
        assert resource_setup["data"] + 1 == 43
