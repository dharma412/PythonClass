*** Settings ***
Resource            regression/regression.robot
Variables           Potestconstants.py
Library             DependencyLibrary

Suite Setup         LoginToAtlas
#Suite Teardown      LogoutofAtlas
Suite Teardown        DeleteAllocationLogoutOfAtlas

*** Variables ***
${customer_name}           ${ATLAS_CUSTOMER_DATA.customer_name}

*** Test Cases ***
Verify_PO_order_is_mandatory_for_adding_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog Text
     Should Be True     """${dialog_message}""" == """Purchase order cannot be empty"""
     Newpoorderpage.Click Ok Warning Dialog

Verify_SO_order_is_mandatory_for_adding_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog Text
     Should Be True     """${dialog_message}""" == """Sales order cannot be empty"""
     Newpoorderpage.Click Ok Warning Dialog


Verify_either_Feature_Bundle_/_Add-on_bundle_needs_to_be_set_for_PO_creation
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog Text
     Should Be True     """${dialog_message}""" == """Feature Bundle / Add-on Bundle not selected!!!"""
     Newpoorderpage.Click Ok Warning Dialog


Verify_Feature_Bundle_start_date_is_mandatory_to_add_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     ${end_date}=   Get Date From Today     20
     Newpoorderpage.Input Feature End Date  ${end_date}
     Newpoorderpage.select feature bundle by index         1
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog text
     Should Be True     """${dialog_message}""" == """Bundle start date cannot be empty"""
     Newpoorderpage.Click Ok Warning Dialog


Verify_Feature_Bundle_end_date_is_mandatory_to_add_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     ${start_date}=   Get Date From Today     -1
     Newpoorderpage.Input Feature Start Date  ${start_date}
     Newpoorderpage.select feature bundle by index         1
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog text
     Should Be True     """${dialog_message}""" == """Bundle end date cannot be empty"""
     Newpoorderpage.Click Ok Warning Dialog


Verify_Feature_cannot_be_empty_if_start_and_end_dates_are_selected_while_adding_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     ${start_date}=   Get Date From Today     -1
     ${end_date}=   Get Date From Today     20
     Newpoorderpage.Input Feature Start Date  ${start_date}
     Newpoorderpage.Input Feature End Date  ${end_date}
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Warning Dialog text
     Should Be True     """${dialog_message}""" == """Feature cannot be empty"""
     Newpoorderpage.Click Ok Warning Dialog


Verify_Dialog_message_showing_while_adding_PO
     [Tags]      Regression
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     ${start_date}=  Get Date From Today   -1
     ${end_date}=   Get Date From Today     20
     Newpoorderpage.Input Feature Start Date  ${start_date}
     Newpoorderpage.Input Feature End Date  ${end_date}
     Newpoorderpage.Select Feature Bundle By Index         1
     Newpoorderpage.Click Save PO
     ${dialog_message}=     Newpoorderpage.Get Confirm Dialog Text
     should contain    ${dialog_message}  You Agree to expire the existing Purchased Order with active Base Bundle on the mentioned start date of new Purchased Order.  Click YES to Continue?

     Newpoorderpage.Click No Confirm Dialog



Verify_new_po_can_be_added
     [Tags]      Regression

     #1.Add new po and verify status message for successfull po creation
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Newpoorderpage.Delete All Future PO Orders
     Customerpage.Click Add PO Order
     Newpoorderpage.Input Purchase Order    ${dummy_purchase_order}
     Newpoorderpage.Input Sales Order       ${dummy_sales_order}
     ${start_date}=  Get Date From Today   -1
     ${end_date}=   Get Date From Today     20
     Newpoorderpage.Input Feature Start Date   ${start_date}
     Newpoorderpage.Input Feature End Date    ${end_date}
     Newpoorderpage.Select Feature Bundle By Index         1
     Newpoorderpage.Click Save PO
     Newpoorderpage.Click Yes Confirm Dialog
     ${status_message}=  Newpoorderpage.Get Status Message
     ${expected_message}=  Catenate    New PO ${dummy_purchase_order} created successfully
     should be equal   ${status_message}  ${expected_message}


Verify_PO_in_FUTURE_state_can_be_deleted
     [Tags]      Regression

     #1.verify add PO test case is successfull as this is test case has dependency on add PO
     Depends on test  Verify_new_po_can_be_added
     Log TO Console  Dependency for future PO addition is met, hence proceeding to Delete Future PO

     #2.Delete all Future PO Orders and verify status message for deletion
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer     ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name  ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Newpoorderpage.Delete All Future PO Orders
     ${status_message}=  Newpoorderpage.Get Status Message
     ${expected_message}=  Catenate   PO order ${dummy_purchase_order} deleted successfully.
     should be equal    ${status_message}  ${expected_message}



