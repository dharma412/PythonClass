from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

#value=driver.find_element_by_xpath("(//*[@id='product']/tbody)[1]/tr[4]/td[2]").text
rowLen=len(driver.find_elements(By.XPATH,"(//*[@id='product'])[1]/tbody/tr"))

columnLen=len(driver.find_elements(By.XPATH,"(//*[@id='product'])[1]/tbody/tr[1]/th"))

for r in range(2,rowLen+1):
    print(r)
    value=driver.find_element(By.XPATH,"(//*[@id='product']/tbody)[1]/tr["+str(r)+"]/td[2]").text
    print(value,end=',')


#print(rowLen)
#print(columnLen)

# for r in range(2,rowLen+1):
#     for c in range(1,columnLen+1):
#         value=driver.find_element(By.XPATH,"(//*[@id='product'])[1]/tbody/tr["+str(r)+"]/td["+str(c)+"]").text
#         print(value, end='    ')
#     print()

