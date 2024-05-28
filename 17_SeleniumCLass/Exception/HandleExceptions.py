#1)#these all comes under NotFoundException Class
#NoSuchElementException

#his happens when tester writes incorrect element locator in the findElement(By, by) method.
        #InvalidSelectorException
        #This subclass of NoSuchElementException class occurs when a selector is incorrect or syntactically invalid.
        # This exception occurs commonly when XPATH locator is used.

#2)This is thrown when WebDriver tries to switch to an invalid window.
#The below code can throw org.openqa.selenium.NoSuchWindowException if the window handle doesn’t exist or is not available to switch.
#driver.switchTo().window(handle_1);

#3)When WebDriver is trying to switch to an invalid frame, NoSuchFrameException under NotFoundException class is thrown.
#The below code can throw org.openqa.selenium.NoSuchFrameException if a frame “frame_11” doesn’t exist or is not available.
#driver.switchTo().frame(“frame_11”);

#4)NoAlertPresentException under NotFoundException is thrown when WebDriver tries to switch to an alert, which is not available.

#org.openqa.selenium.NoAlertPresentException will be thrown If below automation code calls accept() operation on Alert() class when an alert is not yet on the screen.

#driver.switchTo().alert().accept();