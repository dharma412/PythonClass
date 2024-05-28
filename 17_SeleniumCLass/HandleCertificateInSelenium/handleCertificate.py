from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# we can handle the cerificate in many ways
driver=webdriver.FirefoxProfile()
driver.accept_untrusted_certs=True
driver=webdriver.Firefox(firefox_profile=driver)
driver.get('https://url')


#By using the desired capabilities in fire fox
desire_cap=webdriver.DesiredCapabilities.FIREFOX.copy()
desire_cap['acceptInsecureCerts']=True
driver=webdriver.Firefox(capabilities=desire_cap)
driver.get('https://url')


#By using the desired capabilities in Chrome
desire_cap=webdriver.DesiredCapabilities.CHROME.copy()
desire_cap['acceptInsecureCerts']=True
driver=webdriver.Chrome(capabilities=desire_cap)
driver.get('https://url')


#using the Option class
op=Options()
op.add_argument('--allow-running-insecure-content')
op.add_argument('--ignore-certificate-errors')
driver=webdriver.Chrome(chrome_options=Options)
driver.get('https://url')

#using option and Set Capcity

opt=Options()
opt.set_capability("acceptInsecureCerts",True)
driver.get('https://url')

