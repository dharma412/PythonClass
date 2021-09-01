from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver=webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
driver.get("https://www.geeksforgeeks.org/")
driver.maximize_window()
#Step 1: We are inspecting and fetching the element by one of its property ‘name’
# (Also id and class properties can be used) using javascript.

#Step 2: Declare perform click action on an element using javascript.

javaScript = "document.getElementsByName('username')[0].click();"
driver.execute_script(javaScript)

#Executing JavaScript at element level:
#In this case we capture the element that we want to work with using webdriver, then we declare some actions on it using javascript and execute this javascript using WebDriver
#by passing web element as an argument to the javascript. Is it confusing? Lets break down

userName = driver.find_element_by_xpath("//button[@name='username']")
driver.execute_script("arguments[0].click();", userName)
# we can have more than one javascript actions in your statement
userName = driver.find_element_by_xpath("//button[@name='username']")
password = driver.find_element_by_xpath("//button[@name='password']")
driver.execute_script("arguments[0].click();arguments[1].click();", userName, password)


# we can scroll down in Java Script
driver.execute_script("window.scrollTo(0,document.body.scrollHieght);")
driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_quantity_input[index])
driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_showall_button[0])

#Other important aspect of javascript executor is, it can be used to fetch values
#from web element; That means execute_script() method can return values.

driver.execute_script('return document.readyState') == 'complete'
driver.execute_script('return jQuery.active') == 0