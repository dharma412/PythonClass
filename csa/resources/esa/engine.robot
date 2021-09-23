*** Settings ***
Resource   esa/process.robot

*** Variables ***

*** Keywords ***
Get Policy Antispam State
    [Arguments]  ${policy_type}  ${policy_name}
    ${antispam_record_re}=  Set Variable  Anti-Spam:.*
    ${antispam_state_re}=  Set Variable  Anti-Spam:
    ${settings}=  Policyconfig Print  ${policy_type}  ${policy_name}
    ${settings}=  Get Lines Matching Regexp  ${settings}  ${antispam_record_re}
    ${antispam_state}=  Replace String Using Regexp  ${settings}  ${antispam_state_re}  ${EMPTY}
    ${antispam_state}=  Evaluate  '''${antispam_state}'''.strip()
    [Return]  ${antispam_state}

Disable Antispam Default Policy Cli
    Policyconfig Edit Antispam Disable
    ...  Incoming
    ...  DEFAULT
    Commit

Check And Enable AntiSpam
    ${is_enabled}=  AntiSpam Is Enabled  Ironport
    Run Keyword If  not ${is_enabled}
    ...  Antispam Config Case Setup  use_case=yes
    Commit

Check And Disable AntiSpam
    ${is_enabled}=  AntiSpam Is Enabled  Ironport
    Run Keyword If  ${is_enabled}
    ...  AntiSpam Disable  IronPort
    Commit Changes

Generate API Key
    Scp  from_host=${CLIENT_IP}  from_location=${TG_REGISTRATION_SCRIPT}
    ...  to_host=${DUT_IP}  to_location=/data/fire_amp/db/preserve

    ${output}=  Run On DUT  ls -l /data/fire_amp/db/preserve/analysis.key

    Run Keyword If  """analysis.key""" not in """${output}"""
    ...  Get File Analysis Client ID And Generate Analysis Key

Enable Policyconfig AntiSpam
    Policyconfig Edit Antispam Enable  Incoming  DEFAULT
    Policyconfig Edit Antispam Enable  Outgoing  DEFAULT
    Commit

Configure Default Mail Policy Antispam
    [Arguments]  ${settings}
    Mail Policies Edit Antispam  incoming  default  ${settings}
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    Commit Changes

Check And Enable Url Filtering
    ${is_enabled}=  Url Filtering Is Enabled
    Run Keyword If  not ${is_enabled}
    ...  Websecurity Config  url_enable=YES
    Commit

Check And Disable Url Filtering
    ${is_enabled}=  Url Filtering Is Enabled
    Run Keyword If  ${is_enabled}
    ...  Websecurity Config  url_disable=YES
    Commit
