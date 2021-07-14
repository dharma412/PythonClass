from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


#driver=webdriver.Chrome(executable_path=r'C:\Users\dhchaluv\Learning\RobotLearning\SeleniumCLass\Driver\chromedriver.exe')
driver.get("https://www.youtube.com/")




# open url in anybrowser


