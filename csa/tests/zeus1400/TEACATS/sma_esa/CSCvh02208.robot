*** Settings ***
Resource   selenium.txt
Resource   sma/global_sma.txt

*** Variables ***
${host_ssh}         127.0.0.1
${port_ssh}         8089
${USER_NAME1}       user1
${FULL_NAME1}       USER1
${USER_NAME2}       user2
${FULL_NAME2}       USER2
${USER_NAME3}       user3
${FULL_NAME3}       USER3
${PASSWORD1}        T@estpaswor1
${PASSWORD2}        Cisco123$
${PASSWORD3}        Ironport@123

*** Keywords ***

Login into SMA
      Set Library Search Order  SmaGuiLibrary
      Setup Selenium Environment
      Launch DUT Browser
      Log into DUT

Logout from SMA using resource file
   Set Library Search Order  SmaGuiLibrary
   Selenium Close

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1157572c
   [Documentation]  Priv escalation from guest to
   ...  root through splunk injection on SMA
   ...  http://tims.cisco.com/view-entity.cmd?ent=1157572
   [Tags]   srts  teacat  CSCvh02208  Tvh1157572c  invalid_not_applicable_for_smart_license
   [Setup]  Login into SMA
   [Teardown]  Logout from SMA using resource file

   Set Suite Variable   ${FEATUREKEY}   cloud
   Feature Key Set Key  ${FEATUREKEY}
   Users Add User  ${USER_NAME1}  ${FULL_NAME1}  ${PASSWORD1}  ${sma_user_roles.GUEST}
   Users Add User  ${USER_NAME2}  ${FULL_NAME2}  ${PASSWORD2}  ${sma_user_roles.OPERATOR}
   Users Add User  ${USER_NAME3}  ${FULL_NAME3}  ${PASSWORD3}  ${sma_user_roles.CLOUD_ADMIN}
   Commit Changes
   FOR  ${USER_NAME}  ${PASSWORD}  IN
   ...   ${USER_NAME1}  ${PASSWORD1}
   ...   ${USER_NAME2}  ${PASSWORD2}
   ...   ${USER_NAME3}  ${PASSWORD3}
      SSHLibrary.Open Connection    ${SMA}  prompt=>  timeout=30
      SSHLibrary.Login    ${USER_NAME}    ${PASSWORD}
      SSHLibrary.Write   telnet ${host_ssh} ${port_ssh}
      ${out}=  SSHLibrary.Read Until Prompt
      Set SSHLib Prompt  ${Empty}
      SSHLibrary.Close Connection
      Log  ${out}
      Should Contain  ${out}  restricted
   END
   Users Delete User  ${USER_NAME1}
   Users Delete User  ${USER_NAME2}
   Users Delete User  ${USER_NAME3}
   Commit Changes
   Feature Key Delete Key   ${FEATUREKEY}

