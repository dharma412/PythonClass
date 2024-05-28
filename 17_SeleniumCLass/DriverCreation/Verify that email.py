from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
teja = webdriver.Chrome(ChromeDriverManager().install())
teja.get("http://demo.guru99.com/test/login.html")
teja.maximize_window()
assert teja.title=="DriverCreation Page"
teja.close()


