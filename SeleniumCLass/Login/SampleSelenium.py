from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome(executable_path='chromedriver.exe')

driver.get("https://www.facebook.com/login/")

driver.find_element(By.NAME,"email").send_keys("chdharma412@gmail.com")

driver.find_element(By.ID,"pass").send_keys("8008461613")

driver.find_element(By.XPATH,"//a[starts-with(text(),'Forgotten')]").send_keys("993939u")

driver.find_element(By.LINK_TEXT,"Forgotten account?")

driver.find_element(By.PARTIAL_LINK_TEXT,"Forgotten").click()


# xpath-- /html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div/div[3]/button
# relative xpath-

#//tag[@attribute="value"]
#//input[@type="text"]
#//*[@*="text"]
#//input[@type="text" or @name="email1"]
# text() , contains(input,desired),
# //a[starts-with(text(),"Forgotten")]
# //input[@id="email"]

#child
#parent
#ancestor
#following

# Preceding
#Following - sibling:
#Descendant

# id, name, classname,xpath,css selectors,link text,partial link text.










