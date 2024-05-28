import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
<<<<<<< HEAD
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
=======
driver = webdriver.Chrome(ChromeDriverManager().install())
>>>>>>> 6c4a2aacb6a4d51b30fc808c15c3240350bd8d85
driver.implicitly_wait(0.5)
driver.get("https://www.rahulshettyacademy.com/AutomationPractice//")
# identify dropdown with Select class
time.sleep(5)
driver.maximize_window()


drop_ele=driver.find_element(By.XPATH,'//select[@name="dropdown-class-example"]')

sel=Select(drop_ele)

sel.select_by_visible_text("Option2")
sel.select_by_index(3)
sel.select_by_value("option2")