'''
Use id of the element for css selector css=#email

'''

from selenium import webdriver


driver = webdriver.Chrome(executable_path="./Driver/chromedriver.exe")
driver.get("https://stackoverflow.com/")
driver.maximize_window()
driver.find_element_by_link_text("Log in").click()

driver.find_element_by_css_selector("#email").send_keys("chdharma412@gmail.com")