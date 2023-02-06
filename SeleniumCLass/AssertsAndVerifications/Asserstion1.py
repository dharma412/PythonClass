import unittest

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#class Test(unittest.TestCase):
    #def testName(self):
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://demo.automationtesting.in/Alerts.html")
pageTitle=driver.title
print(pageTitle)
assert  "Alerts1"==pageTitle,"Not name is not cottct"
driver.find_element(By.XPATH,"//button[@class='btn btn-danger']").click()

status=driver.find_element().is_selected()
assert 25>98
#assert "Alerts12" in pageTitle


# 1.open urllib
# 2. check tab pageTitle it should be Alerts
# 3. click on alterbutton.  expectation result should be disply