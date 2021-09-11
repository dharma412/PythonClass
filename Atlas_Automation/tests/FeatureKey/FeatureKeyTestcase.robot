*** Settings ***
Resource              regression/regression.robot

Suite Setup           LoginToAtlas
Suite Teardown        DeleteAllocationLogoutOfAtlas
Test Setup             Execute Local Commands  

*** Variables ***
${customer_name}           ${ATLAS_CUSTOMER_DATA.customer_name}
${customer_email}          ${ATLAS_CUSTOMER_DATA.customer_email}
${sales_email}             ${ATLAS_CUSTOMER_DATA.se_email}
${sender_email}            ${ATLAS_CUSTOMER_DATA.sender_email}
${account_manager_email}   ${ATLAS_CUSTOMER_DATA.account_manager_email}
${alerts_notifications}    ${ATLAS_CUSTOMER_DATA.alerts_notifications}
@{EXPIRY_DATES}               90    60    30    15    10    5    1
@{include_expired_features}               True    False

*** Test Cases ***
Tvh1641513c
      [Documentation]
        ...  To verify that Notification email is sent to customer whose feature keys expires for (90,60,30,15,10,5,1)
        ...  feature_expiry_monitor.py script is run
        ...  feature expires Notification mails sent to customers are verified for (90,60,30,15,10,5,1) days from the current date.
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641513,1641514,1641515,1641516,1641517,1641518,1641519
      [Tags]   FeatureKey  Tvh1641513c

      Log To Console  Check License Expiry
      Log To Console  ${customer_name}
      FOR  ${attempt}  IN    @{EXPIRY_DATES}
            Check License Expiry  ${customer_name}  ${attempt}
            Log To Console   Updated End Date With Feature Expiry Interval
            Run Feature Expiry Monitor
            Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent   ${sender_email}   ${customer_name}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry
      END

Tvh1641512c
      [Documentation]
        ...  To verify that expiration interval dates are calculated properly from the current date
        ...  feature_expiry_monitor.py script is run
        ...  expire dates in feature_expiry_monitor.log are verified for (90,60,30,15,10,5,1) days from the current date
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641512
      [Tags]   FeatureKey  expiryDate

      Log To Console  ${customer_name}
      Log To Console  Run Feature Expiry Monitor Script
      Run Feature Expiry Monitor
      ${file_output}=  Read File  /data/var/log/atlas/feature_expiry_monitor.log
      ${output}=  Search Expiry Date In Log  ${file_output}
      log to console  ${file_output}
      Should Be True  ${output}

Tvh1641520c
      [Documentation]
        ...  To verify that Notification email is sent to customer, SE Emails, AM Emails id(s).
        ...  feature_expiry_monitor.py script is run
        ...  feature expires Notification mails sent to customer, SE Emails, AM Emails id(s) are verified for 1 day from the current date.
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641520(and)1641521
      [Tags]   FeatureKey  Tvh1641520c

      Log To Console  Check License Expiry
      Log To Console  ${customer_name}
      Check License Expiry  ${customer_name}   1
      Log To Console   Updated End Date With Feature Expiry Interval
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent   ${sales_email}  ${customer_name}   ${account_manager_email}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry

Tvh1641522c
      [Documentation]
        ...  Verify that Feature Expiration report is sent successfully with list of Customers & respective features expiring in configured interval days
        ...  In "feature_expiry_monitor.conf" check below config value set feature_expiration_report_interval_days=10
        ...  For two customers make sure to change the feature key expiration dates from db such that they expire 10 days from current date
        ...  feature_expiry_monitor.py script is run
        ...  feature expires Notification mails sent to customer email address configured in "feature_expiry_monitor.conf" under [global_feature_expiry_alert]
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641522
      [Tags]   FeatureKey  Tvh1641522c

      Log To Console  Check License Expiry
      Check License Expiry  ${customer_name}   10
      Log To Console   Updated End Date With Feature Expiry Interval
      Update Feature Expiry Monitor File   featureexpiry  feature_expiration_report_interval_days   10
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${global_feature_expiry_alert_mail}=    get_feature_expiry_monitor_file_values    global_feature_expiry_alert    notify
      ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${global_feature_expiry_alert_mail}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry

Tvh1641523c
      [Documentation]
        ...  Verify that if "include_expired_features=False" or  "include_expired_features=True"   in feature_expiry_monitor.conf file
        ...  then expired keys should not or shoud  be included in Feature Expiration report.
        ...  feature_expiry_monitor.py script is run
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641523(and)1641524
      [Tags]   FeatureKey  Tvh1641523c

      FOR  ${value}    IN    @{include_expired_features}
          Log To Console  Check License Expiry
          Check License Expiry  ${customer_name}   10
          Log To Console   Updated End Date With Feature Expiry Interval
          Update Feature Expiry Monitor File   /usr/local/ironport/atlas/etc/feature_expiry_monitor.conf    include_expired_features   ${value}
          Update Feature Expiry Monitor File   /usr/local/ironport/atlas/etc/feature_expiry_monitor.conf    feature_expiration_report_interval_days   10
          Run Feature Expiry Monitor
          Log To Console  Running Feature Expiry Monitor Script
          ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${customer_name}
          Should Be True    ${email_sent_status}    Email notification is not sent or received .
          Log To Console  Users Received Notification Mail For Feature Expiry
      END

Tvh1641525c
      [Documentation]
        ...  Verify that Notification email contains only feature keys which match expiry interval condition
        ...  For a Customer change some of the feature  keys expiration dates from db such that they expire 1 days from current date for
        ...  following features ('ASYNC','CLOUD','CT','CR','BV','CM');
        ...  feature_expiry_monitor.py script is run
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641525
      [Tags]   FeatureKey  Tvh1641525c

      Log To Console  Check License Expiry
      Check License Expiry With Featurename  ${customer_name}   1    'ASYNC','CLOUD','CT','CR','BV','CM'
      Log To Console   Updated End Date With Feature Expiry Interval
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${customer_name}    ASYNC,CLOUD,CT,CR,BV,CM
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry

Tvh1641526c
      [Documentation]
        ...  Verify that Feature Expiry Notification is not sent to customer if PO with Future order with base bundle is placed
        ...  feature_expiry_monitor.py script is run
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641526
      [Tags]   FeatureKey  Tvh1641526c

      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Log To Console  Check License Expiry
      Check License Expiry  ${customer_name}   1
      Log To Console   Updated End Date With Feature Expiry Interval
      ${number_of_bundles} =    Verify Future Order
      should be equal    ${numofmxrecords}  1    Alredy Bundles are added to Customer
      Addnewpo Feature    NewFeatureBundle    111     L-CES-ESI-LIC
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${alerts_notifications}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry

Tvh1641527c
      [Documentation]
        ...  Verify that Feature Expiry Notification is sent to customer if PO with Future order with only ADDON bundle is placed.
        ...  feature_expiry_monitor.py script is run
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641527
      [Tags]   FeatureKey  Tvh1641527c

      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Log To Console  Check License Expiry
      Log To Console  ${customer_name}
      ${number_of_bundles} =    Verify Future Order
      should be equal    ${numofmxrecords}  1    Alredy Bundles are added to Customer
      Addnewpo Addon Feature    NewFeatureBundle    111     L-CES-ESI-LIC
      Check License Expiry  ${customer_name}   1
      Log To Console   Updated End Date With Feature Expiry Interval
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${alerts_notifications}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry

Tvh1641528c
      [Documentation]
        ...  Verify that Customer email is picked from "Alerts & Notifications Email:" to send feature Expiry notification email.
        ...  feature_expiry_monitor.py script is run
        ...  https://tims.cisco.com/view-entity.cmd?ent=1641528
      [Tags]   FeatureKey  Tvh1641528c

      Log To Console  Check License Expiry
      Log To Console  ${customer_name}
      Check License Expiry  ${customer_name}   1
      Log To Console   Updated End Date With Feature Expiry Interval
      Run Feature Expiry Monitor
      Log To Console  Running Feature Expiry Monitor Script
      ${email_sent_status}=  Is Featureexpirynotification Mailsent    ${alerts_notifications}
      Should Be True    ${email_sent_status}    Email notification is not sent or received .
      Log To Console  Users Received Notification Mail For Feature Expiry