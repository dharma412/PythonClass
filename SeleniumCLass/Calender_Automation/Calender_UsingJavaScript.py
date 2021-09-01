from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.maximize_window()
driver.get("http://testautomationpractice.blogspot.com/")

ele=driver.find_element_by_xpath("//*[@id='datepicker']")

driver.execute_script("arguments[0].setAttribute('value','08/06/2021')",ele)