from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.maximize_window()
driver.get("https://www.phptravels.net/home")
driver.find_element_by_xpath("//a[contains(text(),'lights')]").click()
driver.find_element_by_xpath("//*[@id='FlightsDateStart']").click()
val=driver.find_element_by_xpath("(//div[@class='datepicker--nav-title'])[1]").text