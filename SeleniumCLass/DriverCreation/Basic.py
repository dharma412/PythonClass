import time
from selenium import  webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import  ChromeDriverManager
#from  webdriver_manager.firefox import GeckoDriverManager
#diver=webdriver.Chrome(executable_path='E:\PythonClass\SeleniumCLass\Driver\chromedriver.exe')
#driver=webdriver.Firefox(GeckoDriverManager().install())
driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
ele=driver.find_element(By.XPATH,"//input[@name='radioButton']")
ele.click()
print(type(ele))

ele1=driver.find_elements(By.XPATH,"//input[@name='radioButton']")
for i in ele1:
    i.click()



# #ele=driver.find_element(By.CSS_SELECTOR,"input#email")  css with id
# ele=driver.find_element(By.CSS_SELECTOR,"input.inputtext _55r1 _6luy")
# #ele=driver.find_element(By.ID,"email")
# ele.send_keys("chdharma412@gmail.com")
# #driver.find_element(By.CSS_SELECTOR,"pass").send_keys("8008461613")
# # driver.find_element(By.NAME,"login").click()
# # driver.find_element(By.LINK_TEXT,"Forgotten password?")
# # driver.find_element(By.PARTIAL_LINK_TEXT,"Fogotten")
# # driver.find_element(By.TAG_NAME,"input")
# time.sleep(5)
# driver.close()
#
#
#
#
import time
from selenium  import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver import ActionChains, Keys
driver.get("https://www.facebook.com/login/")
driver.maximize_window()
driver.find_element(By.XPATH,"//input[@name='email']").send_keys("7989512436")
driver.find_element(By.XPATH,"//input[@type='password']").send_keys("RAja@9493")
driver.find_element(By.XPATH,"//button[@id='loginbutton']").send_keys(Keys.ENTER)
# act=ActionChains(driver)
# act.key_down(Keys.ENTER)
# time.sleep(10)
# driver.find_element(By.XPATH,"//img[@alt='Mobiles']").click()
# time.sleep(10)
# driver.find_element(By.XPATH,"//p[text()='Samsung']").click()
# time.sleep(10)
# driver.find_element(By.XPATH,"//div[text()='SAMSUNG Galaxy S21 FE 5G (Lavender, 128 GB)']").click()
# time.sleep(20)
# driver.find_element(By.XPATH,"//button[text()='Add to cart']").click()
# time.sleep(20)
#driver.close()
#
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# driver=webdriver.Chrome(ChromeDriverManager().install())
# driver.get("https://www.amazon.in/")
# driver.maximize_window()
# driver.find_element(By.XPATH,"//i[@class='hm-icon nav-sprite']").click()
# driver.find_element(By.XPATH,"//div[text()='Echo & Alexa']").click()
# driver.find_element(By.XPATH,"//a[text()='All-new Echo Dot (4th Gen)']").click()
# time.sleep(10)
# driver.find_element(By.XPATH,"//a[@aria-label='Open Menu']").click()
# time.sleep(10)
# driver.find_element(By.XPATH,"//div[text()='Echo & Alexa']").click()
# driver.find_element(By.XPATH,"//a[text()='Echo Dot (3rd Gen)']").click()
# time.sleep(10)
# driver.find_element(By.ID,"add-to-cart-button").click()
# time.sleep(10)
# driver.find_element(By.XPATH,"//span[@class='a-button a-button-base abb-intl-decline']").click()
# time.sleep(10)
# print("sucussfully added item into cart")
# driver.close()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get("https://www.google.com")