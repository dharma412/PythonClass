from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://demo.automationtesting.in/Windows.html")
driver.maximize_window()

driver.find_element_by_xpath("//button[contains(text(),'    click   ')]").click()
currentwindow=(driver.current_window_handle)

handles=driver.window_handles
driver.close()

driver.switch_to_window(currentwindow)

for i in handles:
    driver.switch_to_window(i)
    print(driver.title)
    if driver.title=="SeleniumHQ Browser Automation":
        driver.close()   # close the parent window

#driver.close() # close the current window
#driver.quit() # close the all browsers