import unittest

from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#class Test(unittest.TestCase):
    #def testName(self):
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://demo.automationtesting.in/Alerts.html")
pageTitle=driver.title

#assert "Alerts12" in pageTitle

try:
    assert "Alerts123" in pageTitle
    print("Title is same")
except:
    print("Title is not same")




#if __name__=="__main__":
    #unittest.main()