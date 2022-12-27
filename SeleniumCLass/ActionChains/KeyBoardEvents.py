from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://extendsclass.com/text-compare.html")
driver.maximize_window()

#source
source_ele=driver.find_element(By.XPATH,"(//*[@class=' CodeMirror-line '])[1]")
#source_ele.clear()
act=ActionChains(driver)
act.key_down(Keys.CONTROL,source_ele).send_keys('a').send_keys('c').perform()


#destination to copy
destination_ele=driver.find_element(By.XPATH,"(//*[contains(text(),'Your documents remain confidential and private,')])[4]")
act.key_down(Keys.CONTROL,destination_ele).send_keys('a').send_keys('v').perform()




