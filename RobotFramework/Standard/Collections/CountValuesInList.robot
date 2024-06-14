*** Settings ***
Library    Collections

*** Variables ***
@{list1}    1   2   3   4   5   8   1  1   1   python

*** Test Cases ***
CountValuesTest
    log to console    ${list1}
    ${count}=     Count Values In List    ${list1}   1
    log to console    ${count}