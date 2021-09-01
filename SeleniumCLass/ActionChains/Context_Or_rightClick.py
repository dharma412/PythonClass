#double click actions
from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://swisnl.github.io/jQuery-contextMenu/demo.html")
driver.maximize_window()

ele=driver.find_element_by_xpath("//span[contains(text(),'right click me')]")
act=ActionChains(driver)
act.context_click(ele).perform()

