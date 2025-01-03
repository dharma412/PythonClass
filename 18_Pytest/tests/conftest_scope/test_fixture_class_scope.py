import pytest
from selenium.webdriver.common.by import By



@pytest.mark.usefixtures('driver_creation')
class Test_Example:

    def setup_method(self,method,driver_creation):
        self.driver=driver_creation
        print(type(self.driver))

    def test_case1(self):
        #driver=driver_creation
        self.driver.get('https://www.sbicard.com/')
        print(self.driver.title)

    def test_case2(self):
        self.driver.get('https://www.sbicard.com/')
        self.driver.find_element(By.XPATH,'//a[contains(text(),"Corporate")]')
