from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.maximize_window()
driver.get("https://jqueryui.com/slider/#colorpicker")

#ele=driver.find_element_by_xpath("//*[@id='datepicker']")
#driver.execute_script("arguments[0].setAttribute('value','07/06/2021')",ele)

#ele1=driver.find_element_by_xpath("//*[@id='content'']/iframe")
driver.switch_to.frame("demo-frame")
ele=driver.find_element(By.XPATH,"//*[@id='red']/span")

act=ActionChains(driver)
act.drag_and_drop_by_offset(ele,100,400).perform()
#driver.close()


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import Select
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://www.seiyria.com/bootstrap-slider")
slider = driver.find_element(By.CSS_SELECTOR,"div#example-1 div.slider-handle.min-slider-handle.round")

move = ActionChains(driver)
move.drag_and_drop_by_offset(slider,40, 0).perform()
