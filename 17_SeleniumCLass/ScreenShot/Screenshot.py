# importing webdriver from selenium

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
url = "https://www.geeksforgeeks.org/"

driver.get(url)


driver.save_screenshot("image.png")
driver.get_screenshot_as_file("image.png")
driver.get_screenshot_as_png()
image = Image.open("image.png")
image.show()


if driver.title=="Alters":
    pass
else:
    driver.save_screenshot("image.png")
#driver.get_screenshot_as_png()
#driver.get_screenshot_as_base64()
# Loading the image

# failure
# each step
# Showing the image