*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
MouseActions
    #right click or context menu
    open browser    https://swisnl.github.io/jQuery-contextMenu/demo.html   chrome
    maximize browser window
    open context menu    xpath://span[@class='context-menu-one btn btn-neutral']
    sleep    5
    # double CLick action
    go to    http://testautomationpractice.blogspot.com/
    maximize browser window
    double click element    xpath://button[contains(text(),'Copy Text')]


    # drag and drop actions
    go to    http://www.dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html
    drag and drop    id:box6    id:box106


