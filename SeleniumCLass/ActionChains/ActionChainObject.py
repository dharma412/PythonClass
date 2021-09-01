#ActionChains are implemented with the help of a action chain object which stores the actions in a queue and when perform() is called,
#performs the queued operations.






from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.find_element_by_link_text("Courses")
element3 = driver.find_element_by_class_name("gsc-input")
#element2=driver.find_element_by_link_text("Jobs")

#create actiona chain object
act=ActionChains(driver)



# on_element is argument to click on .if none ,click on current mouse position.
#act.click(on_element=element)

# on_element is argument to click on .if none ,click on current mouse position.
#  This method is used to hold down the left mouse button on the element.
#act.click_and_hold(on_element=element)

# on_element is argument to click on .if none ,click on current mouse position.
#context_click method on Action Chains in Python Selenium.
# context_click method is used to perform a context-click (right click) on an element.
#act.context_click(on_element=element)


# on_element is argument to click on .if none ,click on current mouse position.
#double_click method on Action Chains in Python Selenium. double_click method is used to double click on an element or current position.
#act.double_click(on_element=element)

#The drag and drop method on action chain in python hold down the
# left mouse button on source and then moves to the target element and release the mouse button.
# require two parameyters source and Target.
#act.drag_and_drop(element,element2)


#key_down method on Action Chains in Python Selenium.
#key_down method is used to send a key press, without releasing it.
# this method is used in case one wants to press, ctrl+c, or ctrl+v.
#For this purpose one needs to first hold the ctrl key down and then press c.
# This method automates this work. It should only be used with modifier keys (Control, Alt and Shift).
act.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()


#move_by_offset method on Action Chains in Python Selenium.
#move_by_offset method is used for moving the mouse to an offset from current mouse position.
#act.move_by_offset(50,60).perform()

#move_to_element method on Action Chains in Python Selenium.
# move_to_element method is used to move the mouse to the middle of an element.
# The argument to_element: The WebElement to move to.
#act.move_to_element(element).click().perform()

#to mov  move_to_element_with_offset method is used to move the mouse by an offset of the specified element.
#Offsets are relative to the top-left corner of the element.
#act.move_to_element_with_offset(element,10,20).perform()

#Release method is used for relasing a held mouse button on the element.

act.click(element3)
act.reset_actions()
#act.click(another_element)
act.send_keys("Arrays")
act.send_keys(Keys.ENTER)
act.perform()


#send_keys method on Action Chains in Python Selenium. send_keys method is used to send keys to current focused element.





