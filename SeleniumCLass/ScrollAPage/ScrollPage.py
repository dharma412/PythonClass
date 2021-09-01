from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.countries-ofthe-world.com/flags-of-the-world.html")
driver.maximize_window()
#scroll By Pixel

driver.execute_script("window.scrollBy(0,1000)") # it will scrolldown by 1000 pixels
# scroll till you find the element

#ele=driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/table[1]/tbody/tr[86]/td[1]/img")
#driver.execute_script("arguments[0].scrollIntoView();",ele)

#
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")






