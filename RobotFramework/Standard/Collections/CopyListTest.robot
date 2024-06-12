*** Settings ***
Library    Collections

*** Variables ***
@{list1}    1   2   3   4   5   8   1  1   1   python

*** Test Cases ***
CopyLitsTest
    log to console    ${list1}
    ${new_list}=     Copy List    ${list1}
    log to console    ${new_list}