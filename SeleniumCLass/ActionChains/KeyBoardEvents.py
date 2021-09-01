from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://extendsclass.com/text-compare.html")
driver.maximize_window()

#source
source_ele=driver.find_element_by_xpath("(//*[@class=' CodeMirror-line '])[1]")
act=ActionChains(driver)
act.key_down(Keys.CONTROL,source_ele).send_keys('a').send_keys('c').perform()


#destination to copy
destination_ele=driver.find_element_by_xpath("(//*[contains(text(),'Your documents remain confidential and private,')])[4]")
act.key_down(Keys.CONTROL,destination_ele).send_keys('a').send_keys('v').perform()




