#Iframes An iframe is used to embed HTML documents in other HTML documents.
# And iframe content can be changed without requiring the user to reload the surrounding page.
#The iframe HTML element is often used to insert content from same/another source, such as an advertisement, into a Web page.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
ele=driver.find_element(By.ID,"courses-iframe")
if ele:
    driver.switch_to.frame("courses-iframe")
    print("I have switched to frame")
else:
    print("No Frame exist")
#driver.close()
driver.implicitly_wait(10)
iframe_list =  driver.find_element(By.TAG_NAME,"iframe")
print(iframe_list)


#switch to frame by index
driver.switch_to.frame(0)
driver.switch_to.frame(1)

#switch to frame by name or ID

driver.switch_to.frame('Dynamic table')
driver.switch_to.frame('book-Table')

#Now we can switch to an iFrame by simply passing the iFrame WebElement to the driver.switchTo().frame() command.

element=driver.find_element(By.NAME,"Teja")
driver.switch_to.frame(element)

# once all operation are done we have to get back to main Page
driver.switch_to.default_content() # to come to main page
driver.switch_to.parent_frame()# to navigate back to parent frame if it is embedded in nested frames

#NoSuchFrameException
# The above exception will thrown if frame mentioned is not found in the page.
