*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections

*** Variables ***
${URL}  https://demo.nopcommerce.com/
${browser}  chrome
*** Keywords ***



*** Test Cases ***
LoginTest
    [Documentation]    Login Test
    [Tags]    regression
    open browser    ${URL}  ${browser}
    click link    xpath:/html/body/div[6]/div[1]/div[1]/div[2]/div[1]/ul/li[2]/a
    #sleep    5
    #execute javascript    window.scrollBy(0,170)
    input text    id:Email    chdharma412@gmail.com
    input text    id:Password   Ustglobal@412
    click element    xpath://button[contains(text(),'Log in')]
    #close browser



