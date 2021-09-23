*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     regression.txt
Force Tags   csdl

Suite Setup     Do Suite Setup
Suite Teardown  Do Suite Teardown
Test Template   Verify Strict-Transport-Security availability in Response Header

*** Variables ***

${user_agent_ff}  Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0
${user_agent_ie}  Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)
${user_agent_chrome}  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36

*** Keywords ***

Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    DefaultRegressionSuiteSetup
    Set Appliance Under Test to SMA
    Run Keyword And Ignore Error  Log Out of DUT
    Log Into DUT
    Spam Quarantine Enable
    Pvo Quarantines Enable
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Centralized Web Reporting Enable
    Centralized Web Configuration Manager Enable
    Centralized Upgrade Manager Enable
    Commit Changes

Do Suite Teardown
    Start Cli Session If Not Open
    Interface Config Edit  Management  http_enable=yes
    ...  https_enable=yes  http_redirection=yes
    Commit
    DefaultRegressionSuiteTeardown

Verify Strict-Transport-Security availability in Response Header
    [Arguments]  ${url}  ${https_disable}  ${tims_link}

    Log  TIMS Link for ${TEST NAME} - ${tims_link}
    Run Keyword If  '${https_disable}'=='no'
    ...  Verify the existence of Strict-Transport-Security  ${url}
    Run Keyword If  '${https_disable}'=='yes'
    ...  Verify the absence of Strict-Transport-Security  ${url}

Verify the existence of Strict-Transport-Security
    [Arguments]  ${url}

    @{user_agents}=  Create List  ${user_agent_ff}  ${user_agent_ie}  ${user_agent_chrome}
    FOR  ${user_agent}  IN  ${user_agents}
      ${response}=  Get Header Response  ${url}  ${user_agent}
      ${output}=  Get From Dictionary  ${response}  Strict-Transport-Security
      Should Be Equal  ${output}  max-age=63072000; includeSubDomains; preload
    END

Verify the absence of Strict-Transport-Security
    [Arguments]  ${url}

    Start Cli Session If Not Open
    Interface Config Edit  Management  http_enable=yes
    ...  https_enable=yes  http_redirection=no
    Commit
    @{user_agents}=  Create List  ${user_agent_ff}  ${user_agent_ie}  ${user_agent_chrome}
    FOR  ${user_agent}  IN  ${user_agents}
      ${response}=  Get Header Response  ${url}  ${user_agent}
      Should Not Contain  ${response}  Strict-Transport-Security
    END

*** Test Cases ***   URL                                                                          https_disable   tims_link
Tvh1303365c           https://${DUT}/services/centralized_configuration/centralized_web_upgrades       no         http://tims.cisco.com/view-entity.cmd?ent=1303365
Tvh1303368c           https://${DUT}/network/dns                                                       no         http://tims.cisco.com/view-entity.cmd?ent=1303368
Tvh1303366c           https://${DUT}/network/ip_interfaces                                             no         http://tims.cisco.com/view-entity.cmd?ent=1303366
Tvh1303369c           https://${DUT}/network/routing                                                   no         http://tims.cisco.com/view-entity.cmd?ent=1303369
Tvh1303367c           https://${DUT}/network/smtp_routes                                               no         http://tims.cisco.com/view-entity.cmd?ent=1303367
Tvh1303292c           https://${DUT}/monitor_email/user_report                                         no         http://tims.cisco.com/view-entity.cmd?ent=1303292
Tvh1303293c           https://${DUT}/monitor_email/mail_reports/overview                               no         http://tims.cisco.com/view-entity.cmd?ent=1303293
Tvh1303294c           https://${DUT}/monitor_email/mail_reports/incoming_mail                          no         http://tims.cisco.com/view-entity.cmd?ent=1303294
Tvh1303295c           https://${DUT}/monitor_email/mail_reports/sender_groups                          no         http://tims.cisco.com/view-entity.cmd?ent=1303295
Tvh1303296c           https://${DUT}/monitor_email/mail_reports/sender_domain_reputation               no         http://tims.cisco.com/view-entity.cmd?ent=1303296
Tvh1303297c           https://${DUT}/monitor_email/mail_reports/hat_connection                         no         http://tims.cisco.com/view-entity.cmd?ent=1303297
Tvh1303298c           https://${DUT}/monitor_email/mail_reports/destination_domains                    no         http://tims.cisco.com/view-entity.cmd?ent=1303298
Tvh1303299c           https://${DUT}/monitor_email/mail_reports/internal_senders                       no         http://tims.cisco.com/view-entity.cmd?ent=1303299
Tvh1303300c           https://${DUT}/monitor_email/mail_reports/internal_users                         no         http://tims.cisco.com/view-entity.cmd?ent=1303300
Tvh1303301c           https://${DUT}/monitor_email/mail_reports/dlp_incident_summary                   no         http://tims.cisco.com/view-entity.cmd?ent=1303301
Tvh1303303c           https://${DUT}/monitor_email/mail_reports/message_filters                        no         http://tims.cisco.com/view-entity.cmd?ent=1303303
Tvh1303304c           https://${DUT}/monitor_email/mail_reports/hvm                                    no         http://tims.cisco.com/view-entity.cmd?ent=1303304
Tvh1303305c           https://${DUT}/monitor_email/mail_reports/content_filters                        no         http://tims.cisco.com/view-entity.cmd?ent=1303305
Tvh1303306c           https://${DUT}/monitor_email/mail_reports/macro_detection                        no         http://tims.cisco.com/view-entity.cmd?ent=1303306
Tvh1303307c           https://${DUT}/monitor_email/mail_reports/threatfeeds                            no         http://tims.cisco.com/view-entity.cmd?ent=1303307
Tvh1303308c           https://${DUT}/monitor_email/mail_reports/dmarc                                  no         http://tims.cisco.com/view-entity.cmd?ent=1303308
Tvh1303309c           https://${DUT}/monitor_email/security_reports/virus_types                        no         http://tims.cisco.com/view-entity.cmd?ent=1303309
Tvh1303310c           https://${DUT}/monitor_email/security_reports/url_filtering                      no         http://tims.cisco.com/view-entity.cmd?ent=1303310
Tvh1303311c           https://${DUT}/monitor_email/security_reports/web_interaction_tracking           no         http://tims.cisco.com/view-entity.cmd?ent=1303311
Tvh1303312c           https://${DUT}/monitor_email/security_reports/fed_protection                     no         http://tims.cisco.com/view-entity.cmd?ent=1303312
Tvh1303313c           https://${DUT}/monitor_email/security_reports/advanced_malware_protection        no         http://tims.cisco.com/view-entity.cmd?ent=1303313
Tvh1303314c           https://${DUT}/monitor_email/security_reports/amp_file_analysis                  no         http://tims.cisco.com/view-entity.cmd?ent=1303314
Tvh1303315c           https://${DUT}/monitor_email/security_reports/amp_verdict_updates                no         http://tims.cisco.com/view-entity.cmd?ent=1303315
Tvh1303316c           https://${DUT}/monitor_email/security_reports/mailbox_auto_remediation           no         http://tims.cisco.com/view-entity.cmd?ent=1303316
Tvh1303317c           https://${DUT}/monitor_email/security_reports/outbreak_filters                   no         http://tims.cisco.com/view-entity.cmd?ent=1303317
Tvh1303318c           https://${DUT}/monitor_email/mail_flow_reports/tls_connections                   no         http://tims.cisco.com/view-entity.cmd?ent=1303318
Tvh1303319c           https://${DUT}/monitor_email/mail_flow_reports/inbound_smtp_auth                 no         http://tims.cisco.com/view-entity.cmd?ent=1303319
Tvh1303321c           https://${DUT}/monitor_email/mail_flow_reports/rate_limit_sender                 no         http://tims.cisco.com/view-entity.cmd?ent=1303321
Tvh1303322c           https://${DUT}/monitor_email/system_reports/system_capacity                      no         http://tims.cisco.com/view-entity.cmd?ent=1303322
Tvh1303323c           https://${DUT}/monitor_email/email_reports/data_status                           no         http://tims.cisco.com/view-entity.cmd?ent=1303323
Tvh1303324c           https://${DUT}/monitor_email/email_reports/scheduled_reports                     no         http://tims.cisco.com/view-entity.cmd?ent=1303324
Tvh1303326c           https://${DUT}/monitor_email/email_reports/archived_reports                      no         http://tims.cisco.com/view-entity.cmd?ent=1303326
Tvh1303327c           https://${DUT}/monitor_email_tracking/message_tracking                           no         http://tims.cisco.com/view-entity.cmd?ent=1303327
Tvh1303328c           https://${DUT}/monitor_email_tracking/tracking_availability                      no         http://tims.cisco.com/view-entity.cmd?ent=1303328
Tvh1303329c           https://${DUT}/monitor_email_quarantine/spam_quarantine_search                   no         http://tims.cisco.com/view-entity.cmd?ent=1303329
Tvh1303330c           https://${DUT}/monitor_email_quarantine/local_quarantines                        no         http://tims.cisco.com/view-entity.cmd?ent=1303330
Tvh1303331c           https://${DUT}/monitor_web/wsa_user_report                                       no         http://tims.cisco.com/view-entity.cmd?ent=1303331
Tvh1303332c           https://${DUT}/monitor_web/monitor_overview                                      no         http://tims.cisco.com/view-entity.cmd?ent=1303332
Tvh1303333c           https://${DUT}/monitor_web/users                                                 no         http://tims.cisco.com/view-entity.cmd?ent=1303333
Tvh1303334c           https://${DUT}/monitor_web/user_count                                            no         http://tims.cisco.com/view-entity.cmd?ent=1303334
Tvh1303335c           https://${DUT}/monitor_web/web_sites                                             no         http://tims.cisco.com/view-entity.cmd?ent=1303335
Tvh1303336c           https://${DUT}/monitor_web/url_categories                                        no         http://tims.cisco.com/view-entity.cmd?ent=1303336
Tvh1303338c           https://${DUT}/monitor_web/applications                                          no         http://tims.cisco.com/view-entity.cmd?ent=1303338
Tvh1303339c           https://${DUT}/monitor_web/security/anti_malware                                 no         http://tims.cisco.com/view-entity.cmd?ent=1303339
Tvh1303340c           https://${DUT}/monitor_web/security/advanced_malware_protection                  no         http://tims.cisco.com/view-entity.cmd?ent=1303340
Tvh1303341c           https://${DUT}/monitor_web/security/amp_file_analysis                            no         http://tims.cisco.com/view-entity.cmd?ent=1303341
Tvh1303342c           https://${DUT}/monitor_web/security/amp_verdict_updates                          no         http://tims.cisco.com/view-entity.cmd?ent=1303342
Tvh1303343c           https://${DUT}/monitor_web/security/web_reputation_filters                       no         http://tims.cisco.com/view-entity.cmd?ent=1303343
Tvh1303344c           https://${DUT}/monitor_web/security/l4_traffic_monitor                           no         http://tims.cisco.com/view-entity.cmd?ent=1303344
Tvh1303346c           https://${DUT}/monitor_web/socks_reports/socks                                   no         http://tims.cisco.com/view-entity.cmd?ent=1303346
Tvh1303347c           https://${DUT}/monitor_web/mus_reports/mus                                       no         http://tims.cisco.com/view-entity.cmd?ent=1303347
Tvh1303348c           https://${DUT}/monitor_web/reporting_services/tracking_search                    no         http://tims.cisco.com/view-entity.cmd?ent=1303348
Tvh1303349c           https://${DUT}/monitor_web/reporting_services/system_capacity                    no         http://tims.cisco.com/view-entity.cmd?ent=1303349
Tvh1303350c           https://${DUT}/monitor_web/reporting_services/data_availability                  no         http://tims.cisco.com/view-entity.cmd?ent=1303350
Tvh1303351c           https://${DUT}/monitor_web/reporting_services/scheduled_reports                  no         http://tims.cisco.com/view-entity.cmd?ent=1303351
Tvh1303352c           https://${DUT}/monitor_web/reporting_services/archived_reports                   no         http://tims.cisco.com/view-entity.cmd?ent=1303352
Tvh1303353c           https://${DUT}/web_utilities/appliance_status                                    no         http://tims.cisco.com/view-entity.cmd?ent=1303353
Tvh1303354c           https://${DUT}/web_utilities/display_settings                                    no         http://tims.cisco.com/view-entity.cmd?ent=1303354
Tvh1303355c           https://${DUT}/web_utilities/centralized_configuration/configuration_masters     no         http://tims.cisco.com/view-entity.cmd?ent=1303355
Tvh1303356c           https://${DUT}/web_utilities/centralized_upgrade/centralized_upgrade_manager     no         http://tims.cisco.com/view-entity.cmd?ent=1303356
Tvh1303357c           https://${DUT}/services/system_status                                            no         http://tims.cisco.com/view-entity.cmd?ent=1303357
Tvh1303358c           https://${DUT}/services/security_appliances                                      no         http://tims.cisco.com/view-entity.cmd?ent=1303358
Tvh1303361c           https://${DUT}/services/email/centralized_reporting                              no         http://tims.cisco.com/view-entity.cmd?ent=1303361
Tvh1303362c           https://${DUT}/services/email/centralized_tracking                               no         http://tims.cisco.com/view-entity.cmd?ent=1303362
Tvh1303363c           https://${DUT}/services/centralized_configuration/configuration                  no         http://tims.cisco.com/view-entity.cmd?ent=1303363
Tvh1303364c           https://${DUT}/services/centralized_configuration/centralized_web_reporting      no         http://tims.cisco.com/view-entity.cmd?ent=1303364
Tvh1303371c           https://${DUT}/system_administration/health                                      no         http://tims.cisco.com/view-entity.cmd?ent=1303371
Tvh1303372c           https://${DUT}/system_administration/alerts                                      no         http://tims.cisco.com/view-entity.cmd?ent=1303372
Tvh1303373c           https://${DUT}/system_administration/log_subscriptions                           no         http://tims.cisco.com/view-entity.cmd?ent=1303373
Tvh1303261c           https://${DUT}/system_administration/return_address                              no         http://tims.cisco.com/view-entity.cmd?ent=1303261
Tvh1303262c           https://${DUT}/system_administration/ssl_config                                  no         http://tims.cisco.com/view-entity.cmd?ent=1303262
Tvh1303272c           https://${DUT}/system_administration/access/users                                no         http://tims.cisco.com/view-entity.cmd?ent=1303272
Tvh1303273c           https://${DUT}/system_administration/access/custom_roles                         no         http://tims.cisco.com/view-entity.cmd?ent=1303273
Tvh1303275c           https://${DUT}/system_administration/access/network_access                       no         http://tims.cisco.com/view-entity.cmd?ent=1303275
Tvh1303276c           https://${DUT}/system_administration/ldap                                        no         http://tims.cisco.com/view-entity.cmd?ent=1303276
Tvh1303277c           https://${DUT}/system_administration/saml                                        no         http://tims.cisco.com/view-entity.cmd?ent=1303277
Tvh1303278c           https://${DUT}/system_administration/disk_management                             no         http://tims.cisco.com/view-entity.cmd?ent=1303278
Tvh1303279c           https://${DUT}/system_administration/shutdown_reboot                             no         http://tims.cisco.com/view-entity.cmd?ent=1303279
Tvh1303280c           https://${DUT}/system_administration/configuration_file                          no         http://tims.cisco.com/view-entity.cmd?ent=1303280
Tvh1303281c           https://${DUT}/system_administration/upgrades/system_upgrade                     no         http://tims.cisco.com/view-entity.cmd?ent=1303281
Tvh1303282c           https://${DUT}/system_administration/upgrades/update_settings                    no         http://tims.cisco.com/view-entity.cmd?ent=1303282
Tvh1303283c           https://${DUT}/system_administration/system_preferences/general_settings         no         http://tims.cisco.com/view-entity.cmd?ent=1303283
Tvh1303284c           https://${DUT}/system_administration/system_time/time_zone                       no         http://tims.cisco.com/view-entity.cmd?ent=1303284
Tvh1303285c           https://${DUT}/system_administration/system_time/time_settings                   no         http://tims.cisco.com/view-entity.cmd?ent=1303285
Tvh1303286c           https://${DUT}/system_administration/feature_keys/smart_licensing                no         http://tims.cisco.com/view-entity.cmd?ent=1303286
Tvh1303288c           https://${DUT}/system_administration/feature_keys/smart_licensing_entitlement    no         http://tims.cisco.com/view-entity.cmd?ent=1303288
Tvh1303289c           https://${DUT}/system_administration/system_setup/euqssw_reset                   no         http://tims.cisco.com/view-entity.cmd?ent=1303289
Tvh1303290c           https://${DUT}/system_administration/system_setup/euqssw_next_steps              no         http://tims.cisco.com/view-entity.cmd?ent=1303290
Tvh1303381c           https://${DUT}/services/email/spam_quarantine                                    no         http://tims.cisco.com/view-entity.cmd?ent=1303381
Tvh1303376c           https://${DUT}/services/security_appliances                                      no         http://tims.cisco.com/view-entity.cmd?ent=1303376
Tvh1303377c           https://${DUT}/services/centralized_configuration/configuration                  no         http://tims.cisco.com/view-entity.cmd?ent=1303377
Tvh1378163c           https://${DUT}:83                                                                no         http://tims.cisco.com/view-entity.cmd?ent=1378163
Tvh1378164c           https://${DUT}:83/Dispatcher                                                     no         http://tims.cisco.com/view-entity.cmd?ent=1378164
Tvh1303370c           https://${DUT}/network/cloud_service_settings                                    no         http://tims.cisco.com/view-entity.cmd?ent=1303370
Tvh1303380c           https://${DUT}/login                                                             yes        http://tims.cisco.com/view-entity.cmd?ent=1303380
Tvh1303374c           http://${DUT}                                                                    yes        http://tims.cisco.com/view-entity.cmd?ent=1303374
