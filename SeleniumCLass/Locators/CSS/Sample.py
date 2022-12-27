import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import  ChromeDriverManager
#from  webdriver_manager.firefox import GeckoDriverManager
#diver=webdriver.Chrome(executable_path='E:\PythonClass\SeleniumCLass\Driver\chromedriver.exe')
#driver=webdriver.Firefox(GeckoDriverManager().install())
driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.facebook.com/login.php")
driver.maximize_window()

ele=driver.find_element(By.CSS_SELECTOR,"input#email")
ele.send_keys("chdharma412@gmail.com")
#driver.find_element(By.CSS_SELECTOR,"input.inputtext _55r1 _6luy _9npi").send_keys("8008461613")
driver.find_element(By.CSS_SELECTOR,"input[name='pass']").send_keys("8008461613")
#driver.find_element(By.NAME,"login").click()
# driver.find_element(By.LINK_TEXT,"Forgotten password?")
# driver.find_element(By.PARTIAL_LINK_TEXT,"Fogotten")
# driver.find_element(By.TAG_NAME,"input")
time.sleep(20)
driver.close()