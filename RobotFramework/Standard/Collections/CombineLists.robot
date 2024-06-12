*** Settings ***
Library    Collections

*** Variables ***
@{list1}    1   2   3   4   5   8   class   python
@{list2}    1   2   36   74   15   8   class   python

*** Test Cases ***
CombineListTest
    log to console    ${list1}
    ${newlist}=     Combine Lists    ${list1}    ${list2}
    log to console    ${newlist}