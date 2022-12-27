
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_1():
    opts = Options()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
    driver.get(
        "https://www.vista.adp.com/vista/index.html?TARGET=-SM-https:%2F%2Fwww.vista.adp.com%2Fess4%2F&REASON=INVALIDCREDENTIALS")

    driver.get("https://www.globalsqa.com/demo-site/frames-and-windows/#iFrame")
    driver.maximize_window()

    driver.switch_to.frame("globalSqa");
    driver.find_element(By.CSS_SELECTOR,"img[alt='Selenium Online Training']").click()
    driver.switch_to.default_content()

    print("text: ",driver.find_element(By.CSS_SELECTOR,"a[title='Demo Testing Site']").text)


    time.sleep(3)
    current_handle= driver.current_window_handle
    print("current_handle: ",current_handle)

    driver.find_element(By.LINK_TEXT,"Privacy").click()
    handles= driver.window_handles
    driver.switch_to.window(handles[1])

    print("Title: ",driver.title)

    driver.switch_to.window(handles[0])

    print("Title: ", driver.title)

    driver.switch_to.new_window('window')
    driver.get("https://www.google.com")

    driver.switch_to.new_window('tab')
    driver.get("https://www.google.com")

test_1()


