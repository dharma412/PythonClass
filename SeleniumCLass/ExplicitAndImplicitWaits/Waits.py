import time

from selenium import  webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

#create Driver objcet
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#implict wait
#An implicit wait instructs Selenium WebDriver to poll DOM for a certain amount of time, this time can be specified,
# when trying to find an element or elements that are not available immediately. The default setting is 0 seconds which means WebDriver will not wait before any operations on element.
#Once set, the implicit wait is set for the life of the WebDriver object i.e. all actions will be delayed by given time.
driver.implicitly_wait(10)
driver.find_element()
#time.sleep(12)
wait=WebDriverWait(driver,100,poll_frequency=5,ignored_exceptions=[BaseException,Exception])
driver.find_element_by_name("checkBoxOption1").click()

#explicit wait
#Explicit wait is used to specify wait condition for a particular element.
# Here we define to wait for a certain condition to occur before proceeding further in the code.
#There can be instance when a particular element takes more than usual time to load. In that case no need to set a huge time to Implicit wait, as this will make browser to wait for the same time for every element.
#To avoid that situation explicit wait is used by defining a separate wait time only on the required elemen
#There are some predefined methods provided that will help your script to wait only as long as required.
# WebDriverWait in combination with ExpectedCondition is one way this can be accomplished.




wait=WebDriverWait(driver,10)
ele=driver.find_element(By.XPATH,"//a[@data-tracking-id='men']"))
#here the driver will wait a maximum of 10 seconds untill the condition is fulfilled.
menu=wait.until(ec.element_to_be_clickable(ele))
ActionChains(driver).move_to_element(menu).perform()
# wait for Fastrack menu item to appear, then click it
fastrmenu=WebDriverWait(driver,10).until(ec.invisibility_of_element_located(By.XPATH,"//a[@data-tracking-id='0_Fastrack']" ))
fastrmenu.perform()

# here WebDriverWait by default calls the ExpectedCondition every 500 milliseconds,
# which is called poll frequency, until it returns successfully. A successful return is for ExpectedCondition type is Boolean return true or not null return value for all other ExpectedCondition types.
# Default value of poll frequency is 0.5 sec we can give 1 sec also
wait=WebDriverWait(driver,10,poll_frequency=1)
#title_is(title) title parameter is required
status=wait.until(ec.title_is("All Selenium - The Blog To Learn Selenium and Test Automation"))
print(status)

# it aslo require parameter and return true if title contains same name.
status=wait.until(ec.title_contains("Learn selenium"), "Title does not contain expected")
print(status)

#presence_of_all_elements_located(locator)

#at least shoud match one element , if all element matched return a list
# parametr is tuple of by and path
#Throws TimeoutException when there is no element located using the locator.

list_of_element=wait.until(ec.presence_of_all_elements_located(By.ID,"Hipro"))

for i in list_of_element:
    print(i.get_attribute("Style"))

#presence_of_element_located(locator)
# it return the hidden element also
#Throws TimeoutException when there is no element located using the locator.

ele=wait.until(ec.presence_of_element_located(By.ID,"Hippro"))

