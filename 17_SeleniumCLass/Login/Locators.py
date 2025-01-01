from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("http://www.google.com")
driver.maximize_window()


# driver.find_element_by_name(name='q').send_keys("naveen automation")
#
# wait=WebDriverWait(driver,200,ignored_exceptions=["elmenet not intracyable exception","No Such a Element Exception"],poll_frequency=4)
#
# wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH,"//input[@type='name']")))
#
#
# optionsList = driver.find_elements(By.XPATH, '//span[contains(text(),"naveen automation")]//child::b')
#
# print(len(optionsList))
#
# for ele in optionsList:
#     print(ele.text)
#
# driver.get("https://www.youtube.com/")
# driver.maximize_window()
# #time.sleep(15)
# driver.implicitly_wait(15)
#
# driver.find_element(By.XPATH,"//input[@id='search']").send_keys("Python videos")
#
# driver.find_element_by_xpath("//input[@id='search']").send_keys("Python videos")
#
# driver.find_element_by_xpath("//button[@id='search-icon-legacy']").click()
#
# driver.find_element(By.CSS_SELECTOR,'div.content')
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# driver.implicitly_wait(50)
# time.sleep(10)
#
# #//*[@id="value"]