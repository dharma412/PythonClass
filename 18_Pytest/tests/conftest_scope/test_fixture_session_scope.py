import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures('driver_creation')
class TestExample:
    def test_case1(self, driver_creation):
        driver=driver_creation
        driver.get('https://www.sbicard.com/')
        print(driver.title)

    def test_case2(self, driver_creation):
        driver = driver_creation
        driver.get('https://www.sbicard.com/')
        driver.find_element(By.XPATH,'//a[contains(text(),"Corporate")]')