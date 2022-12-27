from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


opt=Options()
opt.add_argument('')
opt.add_experimental_option('detach',True)  # keep open your browser event after you code is finished
driver = webdriver.Chrome(ChromeDriverManager().install(),options=opt)