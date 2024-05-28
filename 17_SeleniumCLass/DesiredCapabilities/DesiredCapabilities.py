from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


opt=Options()
opt.add_argument('')
opt.add_experimental_option('detach',True)  # keep open your browser event after you code is finished
driver = webdriver.Chrome(ChromeDriverManager().install(),options=opt)

# start-maximized: Opens Chrome in maximize mode
# incognito: Opens Chrome in incognito mode
# headless: Opens Chrome in headless mode
# disable-extensions: Disables existing extensions on Chrome browser
# disable-popup-blocking: Disables pop-ups displayed on Chrome browser
# make-default-browser: Makes Chrome default browser
# version: Prints chrome browser version
# disable-infobars: Prevents Chrome from displaying the notification ‘Chrome is being controlled by automated software