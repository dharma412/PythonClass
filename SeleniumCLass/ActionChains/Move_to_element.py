#move_to_element
from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains

from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.pavantestingtools.com/")
driver.maximize_window()

traniing=driver.find_element_by_xpath("//a[contains(text(),'Training')]")

online=driver.find_element_by_xpath("//a[contains(text(),'Online')]")

self_paced=driver.find_element_by_xpath("//a[contains(text(),'Self-Paced')]")


act=ActionChains(driver)


act.move_to_element(traniing).move_to_element(online).click().perform()

