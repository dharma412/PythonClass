from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("http://demo.automationtesting.in/Windows.html")
driver.maximize_window()

driver.find_element(By.XPATH,"//button[contains(text(),'    click   ')]").click()
currentwindow=(driver.current_window_handle)

handles=driver.window_handles
#driver.close()

driver.switch_to.window(currentwindow)

for i in handles:
    driver.switch_to.window(i)
    print(driver.title)
    if driver.title=="SeleniumHQ Browser Automation":
        driver.close()   # close the parent window
    else:
        print("not okay")

#driver.close() # close the current window
#driver.quit() # close the all browsers