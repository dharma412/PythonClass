from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import pytest

@pytest.fixture(scope='package')
def driver_creation():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument("--incognito")
    options.add_argument("--disable-cache")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()),options=options)
    print(' I am executing')
    yield driver
    driver.close()
