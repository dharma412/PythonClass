import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
options = Options()
options.add_argument("user-data-dir=C:/Users/Lenovo/AppData/Local/Google/Chrome/User Data")
options.add_argument("start-maximized")
options.add_argument("headless")
prefs = {"download.default_directory" : PATH}
options.add_experimental_option("pref",)




driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
#
# mywait=WebDriverWait(driver,10,ignored_exceptions=Exception)

driver.implicitly_wait(10)
driver.get("https://login.salesforce.com/?eco=1&ec=20037")
driver.maximize_window()
driver.find_element(By.XPATH,"//input[@id='username']").send_keys("tejach412-cnc8@force.com")
driver.find_element(By.XPATH,"//input[@id='password']").send_keys("Ericsson@412")
driver.find_element(By.XPATH,"//input[@id='Login']").click()
ele=driver.find_element(By.XPATH,"//span[@class='slds-truncate'][normalize-space()='Leads']")
driver.execute_script("arguments[0].click();", ele )
# mywait.until(EC.presence_of_all_elements_located(ele))
# mywait.click()
driver.find_element(By.XPATH,"//div[@title='New']").click()
lead_status=driver.find_element(By.XPATH,"//button[@id='combobox-button-360']").click()
sel=Select(lead_status)
sel.select_by_visible_text("Working")
time.sleep(10)
driver.quit()