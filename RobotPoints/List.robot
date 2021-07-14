*** Settings ***
Library    Collections
*** Variables ***
@{list1} =   a  b   c   d
*** Test Cases ***
ListTestcase
    #create list using the create list    keyword
    @{list2}=    create list    1   2    3    4    5    6
    FOR    ${atm1}    IN    @{list2}
        log to console     ${atm1}

    END
    # iterating through the list which is created without create list keyword.
    FOR    ${atm}    IN    @{list1}
        log to console    ${atm}
    END
    # insert value at given index
    insert into list    ${list2}    5    567
    log to console    ${list2}

    #get the value from the given index
    ${value}=    get from list    ${list2}    5
    log to console   ${value}

    #append the values to 2
    append to list    ${list2}    412    413
    log to console    ${list2}

    #combine list
    ${list3} =    combine lists    ${list1}    ${list2}
    log to console    ${list3}

    # conver to list
    # used to convert any item to list object
    ${list4} =    convert to list    abcdefdsa
    log to console    ${list4}

    # copy list
    #if argumet deepcopy=True it will return deep copy of the list else shallow copy
    ${list5} =    copy list    ${list4}
    log to console    ${list5}

    #count values in list
    ${count} =    count values in list    a   0
    log to console    ${count}