import webdriver_manager.utils
from selenium import  webdriver
from selenium.webdriver import FirefoxProfile

fp=FirefoxProfile()
fp.accept_untrusted_certs = False

fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/plain,application/pdf")
#Mine type we have specify if it is text file we have to keep text/plain , for pdf we have to mention application/pdf.
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir","C:\Downloadfiles")
fp.set_preference("browser.download.folderList",2)

driver=webdriver.Firefox(executable_path="",firefox_profile=fp)






















































