
from selenium.common.exceptions import E

#NoSuchElementException extends NotFoundException” and “NotFoundException extends WebDriverException“.

#NotFoundExceotions -parent
        #NoSuchElementException,
            #1.element could not be find in DOM or
        #NoSuchFrameException,
        #NoSuchWindowException,
        #NoAlertPresentException
        #NoSuchAttributeException

#InvalidElementState-parent
    #1.ElementNotVisibleException
    #2.ElementNotSelectableException
    #3.ElementClickInterceptedException





















#1.ElementNotVisibleException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("http://omayo.blogspot.com/")
driver.maximize_window()
driver.find_elements_by_xpath("//*[@id='hbutton']")

try:
    webElement = driver.find_element_by_id("privacy-policy")
    webElement.click()
except NoSuchElementException as exception:
    print ("Element not found and test failed")

#common exceptions