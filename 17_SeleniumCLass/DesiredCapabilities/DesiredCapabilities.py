from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

opt=Options()


opt.add_experimental_option('detach',True)  # keep open your browser event after you code is finished
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()),options=opt)
driver.get("https://www.facebook.com/login/")

driver.find_element(By.NAME,"email").send_keys("chdharma412@gmail.com")



driver.find_element(By.ID,"pass").send_keys("8008461613")

driver.find_element(By.XPATH,"//a[starts-with(text(),'Forgotten')]").send_keys("993939u")

driver.find_element(By.LINK_TEXT,"Forgotten account?")

driver.find_element(By.PARTIAL_LINK_TEXT,"Forgotten").click()

#driver.close()

# start-maximized: Opens Chrome in maximize mode
# incognito: Opens Chrome in incognito mode
# headless: Opens Chrome in headless mode
# disable-extensions: Disables existing extensions on Chrome browser
# disable-popup-blocking: Disables pop-ups displayed on Chrome browser
# make-default-browser: Makes Chrome default browser
# version: Prints chrome browser version
# disable-infobars: Prevents Chrome from displaying the notification ‘Chrome is being controlled by automated software