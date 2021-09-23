*** Settings ***
Resource     sma/sma_esa_ngui.txt
Suite Setup  Smaesa Suite Setup
Suite Teardown  Smaesa Suite Teardown

*** Variables ***

*** Keywords ***

Check Email Status
    [Arguments]  ${status}
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Page Should Contain  ${status}

*** Test Cases ***

CSCvv63856
    [Documentation]  Gui fails to display tracking details, with no errors
    ...  Legacy part is covered in SDR Tvh1214961c
    [Tags]   CSCvv63856  teacat  srts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Run Keywords
    ...  Sma Ngui Teardown
    ...  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Sma Ngui Login
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${CLIENT}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${CLEAN}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .*

    Set Appliance Under Test to SMA
    Wait Until Keyword Succeeds
    ...  6m  1m
    ...  Check Email Status  Delivered

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  delivered=${True}
    SMANGGuiLibrary.Page Should Contain  Delivered
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}  more_details=${True}
    LogMany    ${details}
    ${details}=  Get From Dictionary  ${details}  ${mid}
    Should Not Be Empty  ${details['More Details']}
    Should Match  ${details['Sender']}  ${TEST_ID}@${CLIENT}
    Should Match  ${details['Recipient']}  user5@${CLIENT}
