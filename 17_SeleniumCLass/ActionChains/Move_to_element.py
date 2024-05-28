#move_to_element
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.pavantestingtools.com/")
driver.maximize_window()

Download=driver.find_element(By.XPATH,"//a[contains(text(),'Downloads')]")

you=driver.find_element(By.XPATH,"//a[contains(text(),'YouTube Videos')]")

#self_paced=driver.find_element(By.XPATH,"//a[contains(text(),'Self-Paced')]")


act=ActionChains(driver)
time.sleep(8)

act.move_to_element(Download).perform()
time.sleep(8)
act.move_to_element(you).perform()
#act.reset_actions()

