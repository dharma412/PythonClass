*** Settings ***
Resource              regression/regression.robot

Suite Setup           LoginToAtlas
Suite Teardown        DeleteAllocationLogoutOfAtlas

*** Variables ***
${customer_name}           ${ATLAS_CUSTOMER_DATA.customer_name}
${partner_email}           ${ATLAS_CUSTOMER_DATA.partner_email}
${sales_email}             ${ATLAS_CUSTOMER_DATA.se_email}
${sender_email}            ${ATLAS_CUSTOMER_DATA.sender_email}
@{used_by_service}         interface 'Data 1'  destination controls   listener 'MailFlow'   LDAPS

*** Test Cases ***
001_Verify_SMA_Is_Accessible_After_Customer_Provisioning
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Log To Console                       Checking If SMA UI Is Accessible
      Access SMA
      Log To Console                       SMA UI Is Accessible

002_Verify_ESA_Is_Accessible_After_Customer_Provisioning
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Log To Console                       Checking If ESA UI Is Accessible
      Access ESA
      Log To Console                       ESA UI Is Accessible

003_Verify_Re-Send_SE_Notifications_Can_Be_Sent_From_Customer_Page
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Log To Console  ${partner_email}
      Log To Console  ${sender_email}
      Click On Allocation Name
      Log To Console                    Attempting To Resend SE Notification SE  ${partner_email}  ${sender_email}
      Click Verify SE Notification      ${customer_name}  ${partner_email}  ${sender_email}
      Log To Console                    Resending SE Notification Successful

004_Check_Welcome_letters_are_sent
      Log To Console     ${sales_email}
      ${status}=  Is Welcome Letter Present  ${customer_name}  ${sales_email}
      Should Be True  ${status}  Welcome Letter Isnt Sent To Customer

005_Checking_notifications_for_licenseexpiry
      Log To Console  Check License Expiry
      Log To Console  ${customer_name}
      Check License Expiry  ${customer_name}  15
      Log To Console  Updated End Date With Feature Expiry Interval
      Log To Console  Run Feature Expiry Monitor Script
      Run Feature Expiry Monitor
      ${notification}=  Is Featureexpirynotification Present  ${customer_name}
      Log To Console                      ${notification}
      Log To Console  Atlas Received Notification For Feature Expiry

006_Verify_base_bundle_and_addon_can_be_added_in_purchase_order
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Delete Existing Purchase Orders
     ${feature_name}=     Get Feature
     ${add_on_name}=  Get Add On
     Log To Console     Selected feature is ${feature_name}
     Click Add PO Order
     ${purchase_order}=   Create Feature And Add On In Same Purchase Order            ${feature_name}  ${add_on_name}  -1  30
     Log To Console    Invoking license pusher...
     Check Extended State By Running License Pusher     ${customer_name}
     Log To Console   Running license pusher is complete
     Refresh Customer Purchase Order Page
     ${status}=     Get Activation Status Of Sales Order        ${purchase_order['sales_order']}
     Log To Console    The status of purchase order is  ${status}
     Should Be Equal As Strings     ${status}   ACTIVE
     ${feature}=    get_features_for_customer
     Log To Console    The current feature in UI ${feature}
     ${features_status}=   Verify Feature Activated   ${feature}  ${feature_name}  ${purchase_order['end_date']}
     Should Be True     ${features_status}
     Click On Activations Renewals
     Search Customer Name                 ${customer_name}
     Topnav.Click On Customer Name        ${customer_name}
     Click On Allocation Name
     ${esa_ip}=  Get ESA Ip
     ${result}=   featurekey_on_appliance   ${esa_ip}
     verify_feature_activation   ${feature_name}   ${result}

007_Verify_base_bundle_can_be_added_in_purchase_order_will_activate_purchase_order_by_adding_required_keys_for_order
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Delete Existing Purchase Orders
     ${feature_name}=     Get Feature
     Log To Console     Selected feature is ${feature_name}
     Click Add PO Order
     ${purchase_order}=   Create Feature In Purchase Order     ${feature_name}  -1  30
     Log To Console    Invoking license pusher...
     Check Extended State By Running License Pusher     ${customer_name}
     Log To Console   Running license pusher is complete
     Refresh Customer Purchase Order Page
     ${status}=     Get Activation Status Of Sales Order        ${purchase_order['sales_order']}
     Log To Console    The status of purchase order is  ${status}
     Should Be Equal As Strings     ${status}   ACTIVE
     ${feature}=    get_features_for_customer
     Log To Console    The current feature in UI ${feature}
     ${features_status}=   Verify Feature Activated   ${feature}  ${feature_name}  ${purchase_order['end_date']}
     Should Be True     ${features_status}
     Click On Activations Renewals
     Search Customer Name                 ${customer_name}
     Topnav.Click On Customer Name        ${customer_name}
     Click On Allocation Name
     ${esa_ip}=  Get ESA Ip
     ${result}=   featurekey_on_appliance   ${esa_ip}
     verify_feature_activation   ${feature_name}   ${result}

008_Verify_add_on_can_be_added_in_purchase_order_will_activate_purchase_order_by_adding_required_keys_for_order
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Delete Existing Purchase Orders
     Log To Console    Invoking license pusher...
     Run License Pusher
     Log To Console   Running license pusher is complete
     ${add_on_name}=  Get Add On
     Log To Console     Selected add on is ${add_on_name}
     Click Add PO Order
     ${purchase_order}=  Create Add On In Purchase_order        ${add_on_name}  -1  30
     Log To Console   Running license pusher...
     Check Extended State By Running License Pusher     ${customer_name}
     Log To Console   Running license pusher is complete
     Refresh Customer Purchase Order Page
     ${status}=     Get Activation Status Of Sales Order        ${purchase_order['sales_order']}
     Log To Console    The status of purchase order is  ${status}
     Should Be Equal As Strings     ${status}   ACTIVE
     ${feature}=    get_features_for_customer
     Log To Console    The current feature in UI ${feature}
     ${features_status}=   Verify Feature Activated   ${feature}  ${add_on_name}  ${purchase_order['end_date']}
     Should Be True     ${features_status}
     Click On Activations Renewals
     Search Customer Name                 ${customer_name}
     Topnav.Click On Customer Name        ${customer_name}
     Click On Allocation Name
     ${esa_ip}=  Get ESA Ip
     ${result}=   featurekey_on_appliance   ${esa_ip}
     verify_feature_activation   ${add_on_name}   ${result}

009_Verify_existing_features_can_be_renewed_using_extend_features_option
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Log To Console  Extending features...
     ${before_renewal}=    get_features_for_customer
     ${end_date}=   Renew Features   30
     ${after_renewal}=    get_features_for_customer
     ${features_renewal_status}=   Compare Feature After Renewal    ${before_renewal}  ${after_renewal}  ${end_date}
     Log To Console   The status of feature renewal ${features_renewal_status}
     Should Be True     ${features_renewal_status}

010_Verify_purchase_order_will_expire_on_if_end_date_crosses_current_date
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Delete Existing Purchase Orders
     ${feature_name}=     Get Feature
     Log To Console     Selected feature is ${feature_name}
     Click Add PO Order
     ${purchase_order}=   Create Feature In Purchase Order     ${feature_name}  0  30
     Log To Console    Invoking license pusher ${purchase_order}
     Run License Pusher
     Update End Dates To Expire Purchase Order     -1   ${purchase_order['sales_order']}
     Log To Console    Invoking license pusher...
     Run License Pusher
     Log To Console   Running license pusher is complete
     Refresh Customer Purchase Order Page
     ${status}=     Get Activation Status Of Sales Order        ${purchase_order['sales_order']}
     Log To Console    The status of purchase order is  ${status}
     Should Be Equal As Strings     ${status}   EXPIRE

011_Verify_purchase_order_will_not_activate_and_will_be_in_FUTURE_if_start_date_of_PO_more_than_current_date
     Topnav.Click On Activations Renewals
     Activationsrenewalspage.Input Customer    ${customer_name}
     Activationsrenewalspage.Click On Customer Search
     Activationsrenewalspage.Click On Customer Name     ${customer_name}
     Activationsrenewalspage.Click On Allocation Name
     Delete Existing Purchase Orders
     ${feature_name}=     Get Feature
     Log To Console     Selected feature is ${feature_name}
     Click Add PO Order
     ${purchase_order}=   Create Feature In Purchase Order     ${feature_name}  2  30
     Log To Console    Invoking license pusher...
     Run License Pusher
     Log To Console   Running license pusher is complete
     Refresh Customer Purchase Order Page
     ${status}=     Get Activation Status Of Sales Order        ${purchase_order['sales_order']}
     Log To Console    The status of purchase order is  ${status}
     Should Be Equal As Strings     ${status}   FUTURE


Tvh1642641c
       [Documentation]
        ...  To verify addition of secondary interface from Atlas UI
        ...  Customer name is searched , clicked on allocation name  and secondary interface is added to the customer
        [Tags]   addSecondaryInterface  searchCustomer
        ...  https://tims.cisco.com/view-entity.cmd?ent=1642641


     #1.Get Free Ip count for Data center 1
     ${free_ip_count_dc1}=  Get Free IP Address Count  1
     ${free_ip_dc1}  Convert To Boolean  ${free_ip_count_dc1}
     Should Be True  ${free_ip_dc1}  No Free Ips Available for DC1

     #2.Get Free Ip count for Data center 2
     ${free_ip_count_dc2}=  Get Free IP Address Count  2
     ${free_ip_dc2}  Convert To Boolean  ${free_ip_count_dc2}
     Should Be True  ${free_ip_dc2}  No Free Ips Available for DC2

     #3.Search for Customer
     Log To Console    ${customer_name}
     Search Customer Name                 ${customer_name}

     #4.Click on Customer name and Allocation name links
     Topnav.Click On Customer Name        ${customer_name}
     Click On Allocation Name

     #5.Click on Add Secondary Interface button
     click On Add Secondary Interface Btn
     Sleep  20
     log to console   clicked secondary interface

     #6.verifies secondary interface ip from Atlas UI matches with ip form appliance for all esa
     @{ip_match} =  verify data2 interface ip matches in ui and appliance
     log to console  Secondary Ips are
     FOR  ${ip}  IN  @{ip_match}
            Log to Console    ${ip}
     END
     should not contain  @{ip_match}  False  ESA ips are not matching

012_Verify_ESA_server_can_be_added_to_existing_cluster
      ${esa_count_dc1}=  Get Unassigned Server Count In Dc  ${esa_model}  ${data_center1}
      ${dc1_count}  Convert To Boolean  ${esa_count_dc1}
      Should Be True  ${dc1_count}  No Server Available In Datacenter1
      ${esa_count_dc2}=  Get Unassigned Server Count In Dc  ${esa_model}  ${data_center2}
      ${dc2_count}  Convert To Boolean  ${esa_count_dc2}
      Should Be True  ${dc2_count}   No Server Available In Datacenter2
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Click On Add Server With Config Btn
      Select Datacenter         1
      Select Quantity           1
      Add Server
      Log To Console  Check For Provisioning
      ${provisionedStatus}=  Is Customer Provisioned  ${customer_name}
      Should Be True  ${provisionedStatus}  Customer Provisioning Has Failed
      Log To Console  Customer Got Provisioned with New ESA Server Added.

Tvh1227063c
        [Documentation]
        ...  Verify to get data when user clicks Search button in Activation&Renewals Page
        ...  Customer name is searched and  Allocation details page title is verified on clicking Customer name and Allocation name
        ...  https://tims.cisco.com/view-entity.cmd?ent=1227063
        [Tags]    Tvh1227063c  inventory  searchCustomer

      Log To Console    ${customer_name}

      # 1.Search for Customer in Activaiton & Renewals Page
      Click On Activations Renewals
      Activationsrenewalspage.Input Customer    ${customer_name}
      Sleep  2
      Activationsrenewalspage.Click On Customer Search

      #2.Verify Customer Name in search result
      Log To Console  Searching For Customer Name In Atlas UI
      ${search_result_customer_name}=  Activationsrenewalspage.Get Customer Name From Search Result
      Should Be Equal  ${search_result_customer_name}    ${customer_name}    Customer Name Is Not Found In Search Result

      #3.Verify customer name and allocation name are clickable
      Activationsrenewalspage.Click On Customer Name     ${customer_name}
      Log To Console  Clicked on Customer Name Link
      Sleep  2
      Activationsrenewalspage.Click On Allocation Name
      Log To Console  Customer Allocation Verified
      Sleep  2

      #4.Verify page title contains Allocation Details
      ${allocation_details_page_title}=  Customerpage.Get Allocation Page Title
      Log To Console    ${allocation_details_page_title}
      Should Be Equal    ${allocation_details_page_title}   ATLAS - Allocation Details    Allocation Page Title Does Not Match

Tvh1642644c
        [Documentation]
        ...  To verify generation of SSL certificate in allocation history
        ...  Customer name is searched and in allocation history message for ssl certificate generation is checked
        ...  https://tims.cisco.com/view-entity.cmd?ent=1642644
        [Tags]   SSLgeneration  searchCustomer

      Log To Console    ${customer_name}

      #1.Search for Customer
      Search Customer Name                 ${customer_name}

      #2.Click on Customer name and Allocation name links
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name

      #3.Expand Allocaton History and verify SSL certificate generation
      Expand Allocation History
      ${output}=  Verify SSL Certificate Generation Message
      Should Be True  ${output}  SSL ceritificate is not generated

Tvh1642643c
        [Documentation]
        ...  To verify  SSL certificate are generated for allocation
        ...  ssh login to esa appliance , execute command to get list of certificates
        ...  ciscossl_ cerificate status is checked from list of certificates and it is verified whether used by all services
        ...  https://tims.cisco.com/view-entity.cmd?ent=1642643
        [Tags]   SSLCertificate  searchCustomer

     #1.Click on Activation Renewals, search for customer name and click customer name
     Click On Activations Renewals
     Search Customer Name                 ${customer_name}
     Topnav.Click On Customer Name        ${customer_name}

     #2.click allocation name and in cluster page,esa ip is collected
     Click On Allocation Name
     ${esa_ip}=  Get ESA Ip

     #3.login to esa appliance , execute commands to get certificate details ,verify ciscossl_ certificate is active and it is used by all services
     ${cert_output}=  Verify Certificate Is Availabe And Used By All Services  ${esa_ip}  ciscossl_  ${used_by_service}
     log to console   ${cert_output}
     Should Be True  ${cert_output}  Certificate is not available

013_Remove_Server_from_existing_cluster
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Remove_Server        3
      Log To Console  Server is Removed From Index Input




