# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_web_httpmeth_2.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${http_legacy_307_response}              .*307.*Temporary Redirect.*
${http_legacy_200_response}              .*HTTP.*1.0.*200.*
${http_legacy_unsupported_response}      .*501.*Unsupported method.*
${http_ngui_200_response}                .*200.*OK.*
${http_ngui_400_response}                .*404.*Not Found.*
${http_ngui_unsupported_response}        .*501.*Not Implemented.*

*** Keywords ***
Verify supported legacy HTTP method response
    [Arguments]  ${supported_http_command}
    ${http_command_output}=  Send Curl request and return output  ${supported_http_command}
    ${http_200_status}=  Run keyword and return status  Should match regexp  ${http_command_output}   ${http_legacy_200_response}
    Run keyword if  '${http_200_status}'=='False'  Should match regexp  ${http_command_output}  ${http_legacy_307_response}

Verify unsupported HTTP method response
    [Arguments]  ${unsupported_http_command}  ${http_unsupported_response}
    ${http_unsupported_command_output}=  Send Curl request and return output  ${unsupported_http_command}
    Should match regexp  ${http_unsupported_command_output}  ${http_unsupported_response}

Send Curl request and return output
    [Arguments]  ${http_command}
    ${curl_command}=  Catenate  curl -I -vv -k -X ${http_command}
    ${curl_command_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}    ${curl_command}
    [Return]  ${curl_command_output}

Verify supported ngui HTTP method response
    [Arguments]  ${supported_ngui_http_command}
    ${ngui_supported_curl_command}=  Catenate  curl -I -k -v -u ${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD} -X ${supported_ngui_http_command}
    ${ngui_http_command_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}   ${ngui_supported_curl_command}
    ${ngui_http_200_status}=  Run keyword and return status  Should match regexp  ${ngui_http_command_output}  ${http_ngui_200_response}
    Run keyword if  '${ngui_http_200_status}'=='False'  Should match regexp  ${ngui_http_command_output}  ${http_ngui_400_response}

*** Test Cases ***
Tvh1341276c
    [Documentation]  Tvh1341276c- Disable Unused HTTP Methods
        ...  FLOW DETAILS
        ...  HTTPIE installed in Client
        ...  Trigger commands from client for Legacy and NG UI
        ...  For Legacy SMA UI
        ...  Trigger HTTP commands to check supported methods- GET,POST,HEAD
        ...  Check 200OK or 307 Redirect output
        ...  Check Unsupported commands output for unsupported commands
        ...  For NG UI
        ...  Trigger HTTP commands to check upported methods- GET,POST,PUT,DELETE,OPTIONS
        ...  Check 200OK or 307 Redirect output or valid HTTP output
        ...  Check Unsupported commands output for unsupported commands

    [Tags]  cli  Tvh1341276c
    [Setup]  Trailblazer config enable

    #1. Verify legacy SMA UI GET method
    Verify supported legacy HTTP method response  GET https://${SMA}/javascript?language=en-us

    #2. Verify legacy SMA UI POST method
    Verify supported legacy HTTP method response  POST ${SMA}

    #3. Verify legacy SMA UI HEAD method
    Verify supported legacy HTTP method response  HEAD ${SMA}

    #4. Verify legacy SMA UI unsupported method
    Verify unsupported HTTP method response  PROPFIND ${SMA}  ${http_legacy_unsupported_response}

    #5. Verify NGUI SMA UI GET method
    Verify supported ngui HTTP method response  GET https://${SMA}:4431/sma/api/v2.0/config/appliances?device_type=sma

    #6. Verify NGUI SMA UI PUT method
    Verify supported ngui HTTP method response  PUT https://${SMA}:4431/sma/api/v2.0/config/local_quarantines/Outbreak?device_type=sma {quarantine_automatic_action:true,quarantine_custom_roles:[],quarantine_groups:[],quarantine_normal_actions:'{"quarantine_action":"delete"}',quarantine_type:"OUTBREAK" ,quarantine_users:[]}

    #7. Verify NGUI SMA UI POST method
    Verify supported ngui HTTP method response  POST https://${SMA}:4431/sma/api/v2.0/config/local_quarantines/Outbreak?device_type=sma {quarantine_automatic_action:true,quarantine_custom_roles:[],quarantine_groups:[],quarantine_normal_actions:'{"quarantine_action":"delete"}',quarantine_type:"OUTBREAK" ,quarantine_users:[]}

    #8. Verify NGUI SMA UI DELETE method
    Verify supported ngui HTTP method response  DELETE https://${SMA}:4431/sma/api/v2.0/config/local_quarantines/sample?device_type=sma

    #9. Verify NGUI SMA UI OPTIONS method
    Verify supported ngui HTTP method response  OPTIONS https://${SMA}:4431/sma/api/v2.0/config/local_quarantines/Outbreak?device_type=sma

    #10. Verify NGUI SMA UI unsupported method
    Verify unsupported HTTP method response  PROPFIND https://${SMA}:4431/sma/api/v2.0/config/appliances?device_type=sma  ${http_ngui_unsupported_response}