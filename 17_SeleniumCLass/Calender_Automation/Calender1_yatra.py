from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.maximize_window()
driver.get("https://www.yatra.com/")
driver.maximize_window()
driver.find_element_by_name("flight_origin_date").click()
#driver.find_element_by_xpath("//*[@id='15/09/2021']")

dates=driver.find_elements_by_xpath("//*[@id='monthWrapper']//tbody//td[@class!='inActiveTD']")

for date in dates:
    if date.get_attribute("data-date") == "30/08/2021":
        date.click()
        break



