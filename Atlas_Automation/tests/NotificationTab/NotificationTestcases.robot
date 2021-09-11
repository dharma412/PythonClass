*** Settings ***
Resource        regression/regression.robot

Suite Setup           LoginToAtlas
Suite Teardown        DeleteAllocationLogoutOfAtlas

*** Variables ***
${customer_name}           ${ATLAS_CUSTOMER_DATA.customer_name}
${sales_email}             ${ATLAS_CUSTOMER_DATA.se_email}
${default_email}           ces-atlas-automation@cisco.com
${configuration_notification}           *encrypt* [Atlas - AUTOMATION] Configuration complete for
${allocation_complete_notification}     Allocation complete for
${allocation_failed_notification}       Allocation failed for
${cluster_delte_notification}           Deleted cluster

*** Test Cases ***
Tvh297864c
      [Documentation]
      ...  Verify Auto configuration notification
      ...  https://tims.cisco.com/view-entity.cmd?ent=297864
      [Tags]    Tvh297864c      configurationNotification

      ${status}=   IS Notification Present    ${customer_name}    ${sales_email}    ${configuration_notification}
      Should Be True  ${status}  Configuration Notification Isnt Sent To Customers

Tvh297858c
      [Documentation]
      ...  Verify Allocation done notification
      ...  https://tims.cisco.com/view-entity.cmd?ent=297858
      [Tags]    Tvh297858c      allocationCompleteNotification

      ${status}=  IS Notification Present    ${customer_name}    ${default_email}    ${allocation_complete_notification}
      Should Be True  ${status}  Allocation Complete Notification Isnt Sent To Customer

Tvh297859c
      [Documentation]
      ...  Verify Allocation failed notification
      ...  https://tims.cisco.com/view-entity.cmd?ent=297859
      [Tags]    Tvh297859c      allocationFailedNotification

      ${status}=  IS Notification Present    ${customer_name}    ${default_email}    ${allocation_failed_notification}
      Should Be True  ${status}  Allocation Failed Notification Isnt Sent To Customer

Tvh297860c
      [Documentation]
      ...  Verify Cluster deletion notification
      ...  https://tims.cisco.com/view-entity.cmd?ent=297860
      [Tags]    Tvh297860c      clusterDeletionNotification

      ${status}=  IS Notification Present    hc    ${default_email}    ${cluster_delte_notification}
      Should Be True  ${status}  Allocation cluster deletion Notification Isnt Sent To Customer