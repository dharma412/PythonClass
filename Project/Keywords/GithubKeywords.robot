*** Settings ***
Library    RequestsLibrary

*** Keywords ***
Session Creation
    Create Session    endpoint    https://api.github.com