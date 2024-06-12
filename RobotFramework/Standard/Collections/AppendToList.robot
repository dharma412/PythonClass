*** Settings ***
Library    Collections

*** Variables ***
@{list1}    1   2   3   4   5   8   class   python

*** Test Cases ***
AppendListTest
    log to console    ${list1}
    Append To List    ${list1}    85
    log to console    ${list1}