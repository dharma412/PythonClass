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

# we can pass URL and browser values from the commondline Ex;
#robot -d results -v URL:https://www.youtube.com/watch?v=BxM_IBtT8K8 -v browser:firefox Robot\TestFile.robot
# we can use --variable insted of -v