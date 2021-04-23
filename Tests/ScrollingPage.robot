*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
ScrollingTest
    open browser    https://www.countries-ofthe-world.com/flags-of-the-world.html   chrome
    maximize browser window
    #execute javascript    window.scrollTo(0,1300)
    #scroll element into view    xpath://*[@id="content"]/div[2]/div[2]/table[1]/tbody/tr[44]/td[1]/img
    execute javascript    window.scrollTo(0,document.body.scrollHeight)
    sleep    2
    execute javascript    window.scrollTo(0,-document.body.scrollHeight)
    close all browsers