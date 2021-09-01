'''
Use id of the element for css selector css=#email
css=tag#id here remember id is always preceded by has sign ex: css=input#email(id value)
'''
'''
USe class of the element css=.classname
Use tag with Element css=input.classname it is also similar to the with id except the dot(.) symbol
'''
'''
Locating by css selector - tag and attribute
sybtax= css=tag[attrubute=value]
css=input[name=lastname]
'''
'''
Locating by CSS Selector - tag, class, and attribute
css=tag.class[attribute=value]

'''
'''
CSS Selector - inner text
css=tag.contains("inner text")
css=font:contains("Password:")
'''

from selenium import webdriver


driver = webdriver.Chrome(executable_path="../Driver/chromedriver.exe")
driver.get("https://stackoverflow.com/")
driver.maximize_window()
driver.find_element_by_link_text("Log in").click()

driver.find_element_by_css_selector("#email").send_keys("chdharma412@gmail.com")