# importing webdriver from selenium

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Here Chrome will be used
driver = webdriver.Chrome(ChromeDriverManager().install())
# URL of website
url = "https://www.geeksforgeeks.org/"

driver.get(url)

#driver.save_screenshot("image.png")
driver.get_screenshot_as_file("image.png")
image = Image.open("image.png")
image.show()
#driver.get_screenshot_as_png()
#driver.get_screenshot_as_base64()
# Loading the image


# Showing the image

