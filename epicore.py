#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver=webdriver.Chrome(ChromeDriverManager().install())
#
# driver.get("https://www.google.co.in/")
#
# def slect_page(driver,text,page,suggestion_num):
#
#     driver.find_element(By.XPATH,'//input[@type="text"]').send_keys("epicore")
#     driver.find_element(By.NAME,'btnK')
#     driver.implicitly_wait(10)
#
#     scroll into view  //span[text()="Next"]
#     xpath=f'//a[@aria-label="Page {page}"]'
#     driver.find_element(By.XPATH,xpath).click()
#     // div[ @ id = "search"] // child::div[2]
#     (// div[@class ="MjjYud"] // a[contains( @ href, "https")])[suggestion_num]
import re

with open("file.txt", 'r') as f1:
    for line in f1:
        print(line)





