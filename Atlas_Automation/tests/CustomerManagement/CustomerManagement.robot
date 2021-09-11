*** Settings ***
Resource        regression/regression.robot

*** Variables ***
${customer_name}           ${ATLAS_CUSTOMER_DATA.customer_name}

*** Test Cases ***
Tvh1642649c
    [Documentation]
    ...   Provisioning a O365 Customer on Atlas
    [Tags]    CustomerManagement
    Atlasloginpage.Login To Atlas
    Log To Console         Logged Into Atlas UI
    Click On Activations Renewals
    Click On New Order
    Create Default Customer     feature=1
    ${provisionedStatus}=  Is Customer Provisioned  ${customer_name}
    Should Be True  ${provisionedStatus}  Customer Provisioning Has Failed
    Log To Console       Customer Got Provisioned

Tvh1642642c
    [Documentation]
    ...   Verifying the number of Mail eXchange records of provisioned customer
    [Tags]    CustomerManagement
    Atlasloginpage.Login To Atlas
    Log To Console         Logged Into Atlas UI
    Click On Activations Renewals
    Search Customer Name                 ${customer_name}
    Topnav.Click On Customer Name        ${customer_name}
    ${allocation_name} =   Activationsrenewalspage.get_allocation_name
    Click On Allocation Name
    expand mail exchange
    ${numofmxrecords} =    Mx Records Generate  ${allocation_name}
    should be equal    ${numofmxrecords}  3    Theree Mail eXchange record are not created
    ${provisionedStatus}=  Is Customer Provisioned  ${customer_name}
    Should Be True  ${provisionedStatus}  Customer Provisioning Has Failed
    Log To Console       Customer Got Provisioned
