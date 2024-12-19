from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("https://www.selenium.dev/selenium/docs/api/java/index.html?overview-summary.html")
driver.maximize_window()

driver.switch_to_frame("packageListFrame")
driver.find_element_by_link_text("org.openqa.selenium").click()
driver.switch_to_default_content()
driver.switch_to_frame("packageFrame")
driver.find_element_by_link_text("WebDriver")

driver.switch_to_default_content()
driver.switch_to_frame("classFrame")
driver.find_element_by_xpath("//a[contains(text(),'Deprecated')]").click()
