# it is used to locate notes relative to the main node in that tree.

#parent Tag
#//tagname[@Attribute='Value']//parent::tagname

#child Tag
#//tagname[@Attribute='Value']//child::tagname

#Self Node
#//tagname[@Attribute='Value']//self::tagname

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image
# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
driver.maximize_window()
driver.get("https://developer.salesforce.com/signup")