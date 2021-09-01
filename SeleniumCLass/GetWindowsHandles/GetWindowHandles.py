import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://www.cdot.in")
driver.maximize_window()
window_title = driver.execute_script("return window.document.title")
print(window_title)


