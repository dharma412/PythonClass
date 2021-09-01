import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
teja = webdriver.Chrome(ChromeDriverManager().install())
teja.get("http://demo.guru99.com/test/login.html")
teja.maximize_window()
assert teja.title=="Login Page"
teja.close()


teja.find_element_by_partial_link_text("Project").click()

#driver.find_element_by_link_text("Forgotten password?").click()
#driver.find_element_by_xpath("//a[contains(text(),'Forgotten password')]").click()
#driver.find_element_by_class_name("inputtext _55r1 _6luy").send_keys('80084616132')
#driver.find_element_by_id("email").send_keys("8008461613")
#driver.find_element_by_id("pass").send_keys("Ustglial")
#driver.find_element_by_name("login").click()

#id
#name
#classname
#linketxt
#partiallinktext
#tagname
#css
#xpath






# open url in anybrowser


