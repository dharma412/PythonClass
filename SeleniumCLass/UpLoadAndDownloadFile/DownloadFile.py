
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chromeOptions=Options()
chromeOptions.ad
list1=[]
list1.__

chromeOptions.add_argument("--start-maximized")

chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-useAutomationExtension")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument()
chromeOptions.add_experimental_option("prefs",{"download.default_directory": "C:/Users/dhchaluv/Downloads"})
driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chromeOptions)

driver.get("http://demo.automationtesting.in/FileDownload.html")
driver.maximize_window()
 # switch frame by ID
textfield=driver.find_element_by_xpath("//*[@id='textbox']").send_keys("This is download file")
Genratefile=driver.find_element_by_xpath("//button[@id='createTxt']").click()
donwloadButton=driver.find_element_by_xpath("(//a[contains(text(),'Download')])[3]").click()


#donwload PDF file

