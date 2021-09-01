from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(r'C:\Users\dhchaluv\Learning\PythonLearnings\SeleniumCLass\Assignmenet\Files\index.html')

driver.maximize_window()

driver.find_element_by_xpath("(//button[@type='button'])[2]'").click()
driver.find_element_by_xpath('//*[@id="name"]').send_keys('chaitanya')
driver.find_element_by_xpath('//*[@id="city"]').send_keys('Hyderabad')
driver.find_element_by_xpath('//*[contains(text(),"Enter Data")]').click()
