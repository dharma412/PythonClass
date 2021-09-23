#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/policyconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from sal.containers.yesnodefault import YES, NO
import ast
import traceback


class PolicyConfig(CliKeywordBase):
    """
    cli -> policyconfig

    """

    def get_keyword_names(self):
        return ['spam_params_get',
                'suspected_spam_params_get',
                'antivirus_params_get',
                'repaired_virus_params_get',
                'encrypted_virus_params_get',
                'unscannable_virus_params_get',
                'infected_virus_params_get',
                'advancedmalware_params_get',
                'action_cond_params_get',
                'outbreak_params_get',
                'graymail_safe_unsubscribe_params_get',
                'graymail_marketing_email_params_get',
                'graymail_social_networking_email_params_get',
                'graymail_bulk_email_params_get',
                'policyconfig_new',
                'policyconfig_delete',
                'policyconfig_print',
                'policyconfig_move',
                'policyconfig_search',
                'policyconfig_clear',
                'policyconfig_edit_name',
                'policyconfig_edit_new',
                'policyconfig_edit_delete',
                'policyconfig_edit_print',
                'policyconfig_edit_antispam_enable',
                'policyconfig_edit_antispam_disable',
                'policyconfig_edit_antispam_default',
                'policyconfig_edit_antispam_edit',
                'policyconfig_edit_antivirus_enable',
                'policyconfig_edit_antivirus_disable',
                'policyconfig_edit_antivirus_default',
                'policyconfig_edit_antivirus_edit',
                'policyconfig_filters_new',
                'policyconfig_filters_delete',
                'policyconfig_filters_print',
                'policyconfig_filters_rename',
                'policyconfig_filters_edit_rename',
                'policyconfig_filters_edit_desc',
                'policyconfig_filters_edit_add',
                'policyconfig_filters_edit_delete',
                'policyconfig_filters_edit_move',
                'policyconfig_filters_edit_toggle_all',
                'policyconfig_edit_filters_enable',
                'policyconfig_edit_filters_disable',
                'policyconfig_edit_filters_default',
                'policyconfig_edit_filters_edit',
                'policyconfig_edit_outbreak_enable',
                'policyconfig_edit_outbreak_disable',
                'policyconfig_edit_outbreak_edit',
                'policyconfig_edit_assign_add',
                'policyconfig_edit_assign_delete',
                'policyconfig_edit_outbreak_default',
                'policyconfig_edit_advancedmalware_enable',
                'policyconfig_edit_advancedmalware_disable',
                'policyconfig_edit_advancedmalware_default',
                'policyconfig_edit_advancedmalware_edit',
                'policyconfig_edit_graymail_enable',
                'policyconfig_edit_graymail_disable',
                'policyconfig_edit_graymail_default',
                'policyconfig_edit_graymail_edit'
                ]

    def spam_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Spam Handling

        *Parameters*:
        - `action_spam`: to do with messages identified as spam
        - `use_brightmail`: to use Symantec Brightmail, Yes or No
        - `use_cloudmark`: to use Cloudmark Service, Yes or No
        - `use_ipas`: to use IronPort Anti-Spam,  Yes or No
        - `use_multiscan`: to use Multiscan Service,  Yes or No
        - `use_ims`: to use Intelligent Multi-Scan, Yes or No
        - `header`: add a custom header, Yes or No
        - `header_name`: name of the header
        - `content`: header value
        - `envelope_recipient`: send spam to an alternate envelope recipient, Yes or No
        - `email`: alternate envelope recipient email address to send spam
        - `sent_to`: spam sent to an external quarantine, Yes or No
        - `host`: external quarantine host to send spam
        - `text_add`: add text to the subject of messages
        - `text`: text to be appended or preprended
        - `score_ims`: Intelligent Multi-Scan spam threshold
        - `score`: IronPort Anti-Spam spam threshold
        - `score_cloudmark`: Service Provider Edition spam threshold
        - `archive`: to archive messages identified as spam, Yes or No

        *Examples*:

        | Spam Params Get | use_ipas=yes | score=60 |
        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def suspected_spam_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Suspected Spam Handling

        *Parameters*:
        - `special_treatment`: Enable treatment of suspected spam, Yes or No
        - `action_spam_suspected`: take action with messages identified as Suspected Spam
        - `score_sus_ims`: Intelligent Multi-Scan suspect spam threshold
        - `score_sus_cloudmark`: Cloudmark Service Provider Edition suspect spam threshold
        - `score_suspected`: suspect spam threshold
        - `archive_suspected`: archive messages identified as Suspected Spam, Yes or No
        - `text_add_suspected`: append/prepend text to the subject of messages
        - `text_suspected`: Text to be appended or prepended
        - `sent_to_suspected`: Enable spam sending to an external quarantine or alt-host, Yes or No
        - `host_suspected`: external host
        - `header_suspected`: add a custom header ("yes" or "no")
        - `header_name_suspected`: name of the header
        - `content_suspected`: header value
        - `envelope_recipient_suspected`: Enable spam sent to an alternate envelope recipient, Yes or No
        - `email_suspected`: email address to send spam

        *Examples*:

        | Suspected Spam Params Get | special_treatment=yes | action_spam_suspected=3 |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def antivirus_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Antivirus Handling

        *Parameters*:
        - `antivirus_mcafee`: to use McAfee, Yes or No
        - `antivirus_sophos`: to use Sophos, Yes or No
        - `scan_messages`:  like the system to scan
        - `drop_attachments`: Drop infected attachments
        - `insert_xheader`: automatically insert an X-header

        *Examples*:

        | Antivirus Params Get | antivirus_mcafee=yes |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def repaired_virus_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Repaired Message Handling

        *Parameters*:
        - `repaired_edit`: actions for Repaired Message Handling, Yes or No
        - `repaired_action`: Action applied to the original message
        - `repaired_add_header`: add a custom header, Yes or No
        - `repaired_header`: Enter the header name
        - `repaired_header_content`: Enter the header content
        - `repaired_redirect`: redirect mail to an alternate email
        - `repaired_modify_subject`: modify subject, Yes or No
        - `repaired_text_position`: position of text in Subject
        - `repaired_text_add`: text to add to subject
        - `repaired_message_body_template`: Select a custom message body
        - `repaired_notific_sender`: send notification to sender, Yes or No
        - `repaired_notific_recipient`: send notification to the message recipients
        - `repaired_notific_third`:  send notification to a third party
        - `repaired_address`: address(es) to send notifications to
        - `repaired_message_body`: to use a custom message body
        - `repaired_notific_subj`:  notification subject
        - `repaired_remove_config`: Remove configuration for template
        - `repaired_deliver_address`: the address to deliver to
        - `repaired_mailhost`: the mailhost to deliver to
        - `repaired_deliver_mailhost`: deliver mail to an alternate mailhost
        - `repaired_archive`: archive the original infected message, Yes or No

        *Examples*:

        | Repaired virus Params Get | repaired_edit=yes | repaired_action=5 |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def encrypted_virus_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Encrypted Message Handling

        *Parameters*:
        - `encrypted_edit`: actions for Encrypted Message Handling, Yes or No
        - `encrypted_action`: Action applied to the original message
        - `encrypted_text_add`: Enter the text to add
        - `encrypted_message_body`: to use a custom message body
        - `encrypted_message_body_template`: Select a custom message body
        - `encrypted_text_position`: Select position of text
        - `encrypted_deliver_mailhost`: deliver mail to an alternate mailhost, Yes or No
        - `encrypted_mailhost`: the mailhost to deliver to
        - `encrypted_archive`: archive the original infected message
        - `encrypted_notific_subj`:  notification subject
        - `encrypted_notific_sender`: notification to the message sender
        - `encrypted_notific_third`:  notification to a third party
        - `encrypted_redirect`: redirect mail to an alternate email, Yes or No
        - `encrypted_deliver_address`: the address to deliver redirected mail
        - `encrypted_notific_recipient`: notification to the message recipients
        - `encrypted_add_header`: to add a custom header, Yes or No
        - `encrypted_header`: header name
        - `encrypted_header_content`: header content
        - `encrypted_address`: address(es) to send notifications to
        - `encrypted_modify_subject`: modify the subject, Yes or No
        - `encrypted_remove_config`: Remove configuration for template

        *Examples*:

        | Encrypted virus Params Get | encrypted_edit=yes | encrypted_action=5 |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def unscannable_virus_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Unscannable Message Handling

        *Parameters*:
        - `unscannable_edit`: actions for Unscannable Message Handling, Yes or No
        - `unscannable_action`: Action applied to the original message
        - `unscannable_mailhost`: the mailhost to deliver to
        - `unscannable_modify_subject`: to modify the subject
        - `unscannable_notific_third`:  notification to a third party, Yes or No
        - `unscannable_address`: address(es) to send notifications to
        - `unscannable_notific_sender`: notification to the message sender, Yes or No
        - `unscannable_notific_subj`:  notification subject
        - `unscannable_text_position`: position of text added to subject
        - `unscannable_text_add`: the text to add to subject
        - `unscannable_notific_recipient`: notification to the message recipients, Yes or No
        - `unscannable_message_body_template`: Select a custom message body
        - `unscannable_deliver_mailhost`: deliver mail to an alternate mailhost, Yes or No
        - `unscannable_add_header`: add a custom header, Yes or No
        - `unscannable_header`: Enter the header name
        - `unscannable_header_content`: Enter the header content
        - `unscannable_deliver_address`: the address to deliver to
        - `unscannable_remove_config`: Remove configuration for template
        - `unscannable_redirect`: redirect mail to an alternate email, Yes or No
        - `unscannable_message_body`: to use a custom message body
        - `unscannable_archive`: archive the original infected message

        *Examples*:

        | Unscannable virus Params Get | unscannable_edit=yes | unscannable_action=5 |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def infected_virus_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Virus Infected Message Handling

        *Parameters*:
        - `infected_edit`: actions for Virus Infected Message Handling, Yes or No
        - `infected_action`: Action applied to the original message
        - `infected_archive`: archive the original infected message, Yes or No
        - `infected_deliver_address`: the address to deliver to
        - `infected_mailhost`: the mailhost to deliver to
        - `infected_notific_third`:  notification to a third party, Yes or No
        - `infected_notific_sender`: notification to the message sender, Yes or No
        - `infected_notific_recipient`: notification to the message recipients, Yes or No
        - `infected_notific_subj`:  notification subject
        - `infected_text_add`: Enter the text to add to subject
        - `infected_address`: address(es) to send notifications to
        - `infected_redirect`: redirect mail to an alternate email, Yes or No
        - `infected_deliver_mailhost`: deliver mail to an alternate mailhost, Yes or No
        - `infected_message_body`: to use a custom message body
        - `infected_message_body_template`: Select a custom message body
        - `infected_add_header`: to add a custom header
        - `infected_header`: Enter the header name
        - `infected_header_content`: Enter the header content
        - `infected_modify_subject`: modify the subject, Yes or No
        - `infected_text_position`: position of text to add to subject
        - `infected_remove_config`: Remove configuration for template

        *Examples*:

        | Infected virus Params Get | infected_edit=yes | infected_action=5 |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def advancedmalware_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Advanced Malware Protection Handling

        *Parameters*:
        - `special_treatment`: Enable Advanced malware protection, Yes or No # check
        - `edit_action_file_analysis`: Edit the actions for Messages with File Analysis Pending, Yes or No
        - `apply_action_message`: Apply Action to the original message , options 1 for quarantine or 2 for deliver
        - `enable_file_analysis`: Enable file analysis, Yes or No
        - `insert_xheader`: automatically insert an X-header, Yes or No
        - `edit_action`: to edit the actions for Unscannable Message Handling, Yes or No
        - `action-message`: action applied to the original message
        - `archive_unscannable`: to archive the original infected message, Yes or No
        - `add_header`: add a custom header, Yes or No
        - `header_name`: the header name
        - `header_content`: the header content
        - `modify_subject`: modify the subject, Yes or No
        - `position_text`: postion of text, to be appended or preprended
        - `text`: text to add
        - `archive`: to archive the original infected message, Yes or No
        - `edit_action_malware`: to edit the actions for Malware Infected Message, Yes or No
        - `action-message_malware`: action applied to the original message
        - `drop_infected`: drop infected attachments, Yes or No
        - `archive_malware`: to archive the original infected message, Yes or No

        *Examples*:

        | Advancedmalware Params Get | insert_xheader=yes | edit_action=yes |
        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def outbreak_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for Outbreak Handling

        *Parameters*:
        - `threshold_quarantine`: threshold value to quarantine messages
        - `retention_attachment`: maximum retention period for viral attachment
        - `modification`: enable message modification, Yes or No
        - `retention_all`: maximum retention period for all
        - `proxy`: enable modification of suspicious URLs to use proxy, Yes or No
        - `exclude_domain`: domains to exclude from URL modification, Yes or No
        - `domains`: Domain names to be excluded
        - `signed_message`: exclude signed messages, Yes or No
        - `add_disclaimer`: add a dislaimer, Yes or No
        - `disclaimer`: disclaimer to add
        - `threshold_modify`: threshold value to modify messages
        - `add_text`: position of text to be added to subject
        - `text`: text to be added

        *Examples*:

        | Outbreak Params Get | threshold_quarantine=3 | retention_attachment=5h |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def graymail_safe_unsubscribe_params_get(self, *args):
        """
        Returns a dictionary that holds parameters for Graymail Safe Unsubscribe handling

        *Parameters*
        - `enable_safe_unsubscribe`: Enable Safe Unsubscribe feature for the given policy (Default: No).
        - `safe_unsubscribe_only_unsigned_msg`: Whether to Safely Unsubscribe unsigned messages only (Default: No).

        *Examples*:

        | ${safe_unsubscribe_dict} | Graymail Safe Unsubscribe Params Get |
        | ... | enable_safe_unsubscribe=Yes | safe_unsubscribe_only_unsigned_msg=No |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def graymail_marketing_email_params_get(self, *args):
        """
        Returns a dictionary that holds parameters for Marketing email scanning configurations

        *Parameters*
        - `enable_marketing_email_actions`: Enables actions for Marketing emails (Default: No).
        - `marketing_mail_action`: Action for Marketing emails (Default: DELIVER).
                Options are: (ID & String both works)
                           1. DELIVER
                           2. DROP
                           3. BOUNCE
                           4. IRONPORT QUARANTINE
        - `marketing_mail_archive_messages`: Archives Marketing emails (Default: No).

        Below parameters are valid only if "marketing_mail_action" is set to 'DELIVER' or 'IRONPORT QUARANTINE'
        - `marketing_mail_to_external_quarantine`: Quarantines Marketing emails to an external host (Default: No).
        - `marketing_mail_external_host`: External hostname for Quarantined Marketing emails.
        - `marketing_mail_add_subject_text`: Add customised text to Marketing email's subject (Default: NONE)
                Options are: (ID and String both works)
                           1. PREPEND
                           2. APPEND
                           3. NONE
        - `marketing_mail_subject_text`: Text to append or prepand to Marketing email's subject.
        - `marketing_mail_add_custom_header`: Add a custom header to Marketing emails (Default: No).
        - `marketing_mail_custom_header_name`: Name of the custom header.
        - `marketing_mail_custom_header_value`: Value of the custom header.
        - `marketing_mail_send_to_altrcpt`: Deliver Marketing mails to an alternate email address.
        - `marketing_mail_altrcpt_email_address`: Alternate email address to deliver Marketing emails.

        *Examples*

         | ${marketing_email_dict}= | Graymail Marketing Email Params Get |
         | ... | enable_marketing_email_actions=Yes |
         | ... | marketing_mail_action=DELIVER |
         | ... | marketing_mail_to_external_quarantine=Yes |
         | ... | marketing_mail_external_host=exthost.com |
         | ... | marketing_mail_archive_messages=Yes |
         | ... | marketing_mail_add_subject_text=1 |
         | ... | marketing_mail_subject_text=[TESTSUB] |
         | ... | marketing_mail_add_custom_header=Yes |
         | ... | marketing_mail_custom_header_name=TESTHEADERNAME |
         | ... | marketing_mail_custom_header_value=TestHeaderValue |
         | ... | marketing_mail_send_to_altrcpt=Yes |
         | ... | marketing_mail_altrcpt_email_address=alt@rcpt.com |
        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def graymail_social_networking_email_params_get(self, *args):
        """
        Returns a dictionary that holds parameters for Social Networking email scanning configurations

        *Parameters*
        - `enable_social_networking_email_actions`: Enables actions for Social Networking emails (Default: No).
        - `social_networking_mail_action`: Action for Social Networking emails (Default: DELIVER).
                Options are: (ID & String both works)
                           1. DELIVER
                           2. DROP
                           3. BOUNCE
                           4. IRONPORT QUARANTINE
        - `social_networking_mail_archive_messages`: Archives Social Networking emails (Default: No).

        Below parameters are valid only if "social_networking_mail_action" is set to 'DELIVER' or 'IRONPORT QUARANTINE'
        - `social_networking_mail_to_external_quarantine`: Quarantines Social Networking emails to an external host (Default: No).
        - `social_networking_mail_external_host`: External hostname for Quarantined Social Networking emails.
        - `social_networking_mail_add_subject_text`: Add customised text to Social Networking email's subject (Default: NONE)
                Options are: (ID and String both works)
                           1. PREPEND
                           2. APPEND
                           3. NONE
        - `social_networking_mail_subject_text`: Text to append or prepand to Social Networking email's subject.
        - `social_networking_mail_add_custom_header`: Add a custom header to Social Networking emails (Default: No).
        - `social_networking_mail_custom_header_name`: Name of the custom header.
        - `social_networking_mail_custom_header_value`: Value of the custom header.
        - `social_networking_mail_send_to_altrcpt`: Deliver Social Networking mails to an alternate email address.
        - `social_networking_mail_altrcpt_email_address`: Alternate email address to deliver Social Networking emails.

        *Examples*

         | ${social_networking_email_dict}= | Graymail Social Networking Email Params Get |
         | ... | enable_social_networking_email_actions=Yes |
         | ... | social_networking_mail_action=DELIVER |
         | ... | social_networking_mail_to_external_quarantine=Yes |
         | ... | social_networking_mail_external_host=exthost.com |
         | ... | social_networking_mail_archive_messages=Yes |
         | ... | social_networking_mail_add_subject_text=1 |
         | ... | social_networking_mail_subject_text=[TESTSUB] |
         | ... | social_networking_mail_add_custom_header=Yes |
         | ... | social_networking_mail_custom_header_name=TESTHEADERNAME |
         | ... | social_networking_mail_custom_header_value=TestHeaderValue |
         | ... | social_networking_mail_send_to_altrcpt=Yes |
         | ... | social_networking_mail_altrcpt_email_address=alt@rcpt.com |
        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def graymail_bulk_email_params_get(self, *args):
        """
        Returns a dictionary that holds parameters for Bulk email scanning configurations

        *Parameters*
        - `enable_bulk_email_actions`: Enables actions for Bulk emails (Default: No).
        - `bulk_mail_action`: Action for Bulk emails (Default: DELIVER).
                Options are: (ID & String both works)
                           1. DELIVER
                           2. DROP
                           3. BOUNCE
                           4. IRONPORT QUARANTINE
        - `bulk_mail_archive_messages`: Archives Bulk emails (Default: No).

        Below parameters are valid only if "bulk_mail_action" is set to 'DELIVER' or 'IRONPORT QUARANTINE'
        - `bulk_mail_to_external_quarantine`: Quarantines Bulk emails to an external host (Default: No).
        - `bulk_mail_external_host`: External hostname for Quarantined Bulk emails.
        - `bulk_mail_add_subject_text`: Add customised text to Bulk email's subject (Default: NONE)
                Options are: (ID and String both works)
                           1. PREPEND
                           2. APPEND
                           3. NONE
        - `bulk_mail_subject_text`: Text to append or prepand to Bulk email's subject.
        - `bulk_mail_add_custom_header`: Add a custom header to Bulk emails (Default: No).
        - `bulk_mail_custom_header_name`: Name of the custom header.
        - `bulk_mail_custom_header_value`: Value of the custom header.
        - `bulk_mail_send_to_altrcpt`: Deliver Bulk mails to an alternate email address.
        - `bulk_mail_altrcpt_email_address`: Alternate email address to deliver Bulk emails.

        *Examples*

         | ${bulk_email_dict}= | Graymail Bulk Email Params Get |
         | ... | enable_bulk_email_actions=Yes |
         | ... | bulk_mail_action=DELIVER |
         | ... | bulk_mail_to_external_quarantine=Yes |
         | ... | bulk_mail_external_host=exthost.com |
         | ... | bulk_mail_archive_messages=Yes |
         | ... | bulk_mail_add_subject_text=1 |
         | ... | bulk_mail_subject_text=[TESTSUB] |
         | ... | bulk_mail_add_custom_header=Yes |
         | ... | bulk_mail_custom_header_name=TESTHEADERNAME |
         | ... | bulk_mail_custom_header_value=TestHeaderValue |
         | ... | bulk_mail_send_to_altrcpt=Yes |
         | ... | bulk_mail_altrcpt_email_address=alt@rcpt.com |

        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def action_cond_params_get(self, *args):
        """
        Returns Dictionary that holds parameter for action or condition Handling

        *Parameters*:
        - `action_condition`: Action or Condition
        - `action`: Action to be used
        - `condition`: Condition to be used
        - `use_opp_tls`: use opportunistic TLS
        - `encrypt_profile`: Choose the encryption profile
        - `file_type_strip`: file type to strip
        - `iia_verdict_to_match`: Choose Image Analysis verdict to match
        - `log_text`: text you want to log to mail logs
        - `notification_email`: to send the notification
        - `attach_filenames`: filenames for
        - `mesg_matched`: Messages arrived via listeners
        - `edit_bcc_alt_host`: alternate host of the Bcc message
        - `insert_header`: name of the header to insert
        - `value_header`: the value for this header
        - `redirect_host`: host to redirect mail
        - `strip_header`: name of the header to strip
        - `edit_return_path_notific`: return path of the notification
        - `listener`: Currently configured listeners
        - `bcc_alt_host`: Enter alternate host to redirect mail to:
        - `copy_include`: include a copy of the original message
        - `redirect_mail`: address to redirect mail to
        - `mime_strip`: MIME type to strip
        - `use_custom_subj`: use a custom subject line?
        - `bytes`: minimum size, in bytes
        - `return_path`: Enter the return path address:
        - `use_custom_notific`: custom template for the notification?
        - `edit_subject_notific`: line used on the notification
        - `bind_interface`: interfaces to bind the connection
        - `enter_text`: enter specific text
        - `urlcategory_defang`: Url Categories to defang (comma seperated)
        - `url_whitelist`: Selct the urls to be whitelisted
        - `exclude_signedmessages`: exclude signedmessages (Default value = Y)
        - `urlcategory_replace`: Url Categories to replece (comma seperated)
        - `urlcategory_redirect`: Url Categories to redirect (comma seperated)
        - `smime_profile`: Choose the S/MIME sending profile you want to use
        - `message_language`: Choose which Language to match
        - `message_language_match`: Choose which messages will match this rule
        - `macro_detection`: Enter the supported file types, separated by commaEnter the supported file types, separated by commass
        *Examples*:

        | Action Cond Params Get | action_condition=Action | action=Drop |
        | ${action} | Action Cond Params Get | action_condition=Action |
        | ... |  action=Defang URL based on category |
        | ... |  urlcategory_defang=31,44 |
        | ... |  url_whitelist=2 |
        | ... |  exclude_signedmessages=Y |
        | ${action1}  Action Cond Params Get |  action_condition=Action |
        | ... |  action=Replace URL based on category |
        | ... |  urlcategory_replace=12,23 |
        | ... |  url_whitelist=1 |
        | ... |  exclude_signedmessages=N |
        | ${action2}  Action Cond Params Get | action_condition=Action |
        | ... |  action=Redirect URL to Cisco Security proxy |
        | ... |  urlcategory_redirect=10,18 |
        | ... |  url_whitelist=3 |
        | ... |  exclude_signedmessages=Y |
        """
        kwargs = self._convert_to_dict(args)
        return kwargs

    def policyconfig_new(self, policy_type, *args):
        """
        This keyword will create new policy for given policy type

        policyconfig -> incoming -> new

        *Parameters*:
        - `policy_type`: Policy Type, "incoming" or "outgoing"
        - `policy_name`: Name of the policy to be added. String. Mandatory
        - `add_senders_and_receivers`: Add entry for policy senders/receivers, "Yes" or "No".
                Default: Yes
        - `add_senders`: Add senders for this policy, "Yes" or "No"
                Default: Yes
        - `sender_policy_applies_for`: Policy is applicable for sender option.
                Default: 1
                Optioins:
                    1. All Senders
                    2. Any of the added senders
                    3. None of the added senders
        - `sender_add_domain_entries`: Enter sender domain entries, "Yes" or "No".
                Default: Yes.
                (Applicable if 'sender_policy_applies_for' is set to option 2 or 3)
        - `sender_domain_entries`: Enter the senders for this policy [comma separated]
                Required, if 'sender_add_domain_entries' is set to 'Yes'
        - `sender_add_ldap_group_membership`: Use LDAP group memberships for sender, "Yes" or "No".
                Default: No
        - `sender_ldap_group_name`: Enter groupname for LDAP query for sender, "Yes" or "No".
                Required, if 'sender_add_ldap_group_membership' is set to 'Yes'
        - `sender_ldap_group_query`: Select an LDAP group query for sender.
                Required, if 'sender_add_ldap_group_membership' is set to 'Yes'
        - `sender_add_another_group_membership`: Add another LDAP group membership for sender, "Yes" or "No".
                Default: No
                (Applicable if 'sender_add_ldap_group_membership' is set to 'Yes')
        - `add_receivers`: Add receivers for this policy, "Yes" or "No"
                Default: Yes
        - `receiver_policy_applies_for`: Policy applicable for receiver option.
                Default: 1
                Optioins:
                    1. All Receivers
                    2. Any of the added receivers
                    3. All of the added receivers
        - `receiver_add_domain_entries`: Enter receiver domain entries, "Yes" or "No".
                Default: Yes
                (Applicable if 'receiver_policy_applies_for' is set to option 2 or 3)
        - `receiver_domain_entries`: Enter the receivers for this policy [comma separated]
                Required, if 'receiver_add_domain_entries' is set to 'Yes'
        - `receiver_add_ldap_group_membership`: Use LDAP group memberships for receiver, "Yes" or "No".
                Default: No
        - `receiver_ldap_group_name`: Enter groupname for LDAP query for receiver.
                Required, if 'receiver_add_ldap_group_membership' is set to 'Yes'
        - `receiver_ldap_group_query`: Select an LDAP group query for receiver.
                Required, if 'receiver_add_ldap_group_membership' is set to 'Yes'
        - `receiver_add_another_group_membership`: Add another LDAP group membership for receiver, "Yes" or "No".
                Default: No
                (Applicable if 'receiver_add_ldap_group_membership' is set to 'Yes')
        - `add_exceptions`: Enter Exceptions for receiver.
                Default: No
                (Applicable if 'receiver_policy_applies_for' is set to option 3)
        - `exception_add_domain_entries`: Enter domain entries for exceptions, "Yes" or "No".
                Default: Yes
                (Applicable if 'add_exceptions' is set to 'Yes')
        - `exception_domain_entries`: Enter the exceptions for this policy [comma separated]
                Required, if 'exception_add_domain_entries' is set to 'Yes'
        - `exception_add_ldap_group_membership`: Use LDAP group membership exceptions, "Yes" or "No".
                Default: No
        - `exception_ldap_group_name`: Enter groupname for LDAP query for exception.
                Required, if 'exception_add_ldap_group_membership' is set to 'Yes'
        - `exception_ldap_group_query`: Select an LDAP group query for exception.
                Required, if 'exception_add_ldap_group_membership' is set to 'Yes'
        - `exception_add_another_group_membership`: Add another LDAP group membership exception, "Yes" or "No".
                Default: No
                (Applicable if 'exception_add_ldap_group_membership' is set to 'Yes')
        - `add_another_entry`: Add another entry of senders/receivers.
                Default: No
        - `antispam_enable`: Enable Anti-Spam support for this policy, "Yes" or "No".
                Default: No
        - `antispam_table`: Use the policy table default, "Yes" or "No".
                Default: Yes
                (Applicable if 'antispam_enable' is set to 'Yes')
        - `antivirus_enable`: Enable Anti-Virus support for this policy, "Yes" or "No".
                Default: No
        - `antivirus_table`: Use the policy table default, "Yes" or "No".
                Default: Yes
                (Applicable if 'antivirus_enable' is set to 'Yes')
        - `advancedmalware_enable`: Enable Advanced-Malware protection for this policy, "Yes" or "No".
                Default: No
        - `advancedmalware_table`: Use the policy table default, "Yes" or "No".
                Default: Yes
                (Applicable if 'advancedmalware_enable' is set to 'Yes')
        - `content_filter_enable`: Enable Content Filters for this policy, "Yes" or "No".
                Default: No
        - `content_filter_table`: Use the policy table default, "Yes" or "No".
                Default: Yes
                (Applicable if 'content_filter_enable' is set to 'Yes')
        - `vof_enable`: Enable Outbreak Filters for this policy, "Yes" or "No".
                Default: No
        - `vof_table`: Use the policy table default, "Yes" or "No".
                Default: Yes
                (Applicable if 'vof_enable' is set to 'Yes')
        - `assign_user_role`: Assign any user roles to access, "Yes" or "No".
                Default: No

        *Examples*:

        | Policyconfig New | Incoming | test_policy      |
        | ... | add_senders_and_receivers=Yes            |
        | ... | add_senders=yes                          |
        | ... | sender_policy_applies_for=2              |
        | ... | ender_add_domain_entries=Yes             |
        | ... | sender_domain_entries=@test.ibqa         |
        | ... | sender_add_ldap_group_membership=Y       |
        | ... | sender_ldap_group_name=ea_upq_admin      |
        | ... | sender_ldap_group_query=1                |
        | ... | sender_add_another_group_membership=No   |
        | ... | add_receivers=yes                        |
        | ... | receiver_policy_applies_for=3            |
        | ... | receiver_add_domain_entries=y            |
        | ... | receiver_domain_entries=test@abc.com     |
        | ... | receiver_add_ldap_group_membership=Yes   |
        | ... | receiver_ldap_group_name=rcpt_ldap_grp   |
        | ... | receiver_ldap_group_query=2              |
        | ... | receiver_add_another_group_membership=N  |
        | ... | add_exceptions=Yes                       |
        | ... | exception_add_domain_entries=Y           |
        | ... | exception_domain_entries=spam@abc.com    |
        | ... | exception_add_ldap_group_membership=no   |
        | ... | add_another_entry=N                      |
        | ... | antispam_enable=Yes                      |
        | ... | antivirus_enable=Yes                     |
        | ... | advancedmalware_enable=Yes               |
        | ... | vof_enable=Yes                           |
        | ... | content_filter_enable=Yes                |
        | ... | assign_user_role=No                      |
        | Commit                                         |

        """
        try:
            kwargs = self._convert_to_dict(args)
            result_obj = self._cli.policyconfig().choose(policy_type).new(**kwargs)
            if kwargs.has_key('vof_modify') and kwargs['vof_modify'].lower() == "yes":
                result_obj.new(vof_file_ext)
            if kwargs.has_key('assign_user') and kwargs['assign_user'].lower() == "yes":
                result_obj.add(user_role)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_delete(self, policy_type, policy_name):
        """
        This keyword will delete given policy

        policyconfig -> incoming -> delete

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy_name`: Name of the policy to be deleted.

        *Examples*:

        | Policyconfig Delete | Incoming | policy_name=mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).delete(policy_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_print(self, policy_type, policy_name):

        """
        This keyword return policy details for given Incoming policy

        policyconfig -> incoming -> print

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy_name`: Name of the policy to be printed.

        *Examples*:

        | Policyconfig print | Incoming | policy_name=mypolicy |

        """
        try:
            return str(self._cli.policyconfig().choose(policy_type).print_policy(policy_name))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_move(self, policy_type, policy_name, position):

        """
        This keyword is to move given Incoming policy to given position

        policyconfig -> incoming -> move

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy_name`: Name of the policy to be printed.
        - `position`: Position the policy need to be shifted

        *Examples*:

        | Policyconfig Move | Incoming | policy_name=mypolicy1 | position=1 |

        """
        try:
            self._cli.policyconfig().choose(policy_type).move(policy_name, position)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_search(self, policy_type, policy_member):

        """
        This keyword return search details for given Incoming policy member

        policyconfig -> incoming -> search

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy_member`: policy member to be searched.

        *Examples*:

        | Policyconfig Search | Incoming | re@mem.com |

        """
        try:
            return str(self._cli.policyconfig().choose(policy_type).search(policy_member))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_clear(self, policy_type):

        """
        This keyword deletes all policies

        policyconfig -> incoming -> clear

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.

        *Examples*:

        | Policyconfig Clear | Incoming |

        """
        try:
            self._cli.policyconfig().choose(policy_type).clear()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_name(self, policy_type, policy, policy_name):

        """
        This keyword changes name of given Incoming policy

        policyconfig -> incoming -> Edit -> name

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `policy_name`: New Incoming policy name.

        *Examples*:

        | Policyconfig Edit Name | Incoming | mypolicy | mypolicy1 |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).name(policy_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_new(self, policy_type, policy_name, *args):

        """
        This keyword changes adds new member to given Incoming policy

        policyconfig -> incoming -> Edit -> new

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `add_senders`: Add senders for this policy, "Yes" or "No"
                Default: Yes
        - `sender_policy_applies_for`: Policy is applicable for sender option.
                Default: 1
                Optioins:
                    1. All Senders
                    2. Any of the added senders
                    3. None of the added senders
        - `sender_add_domain_entries`: Enter sender domain entries, "Yes" or "No".
                Default: Yes.
                (Applicable if 'sender_policy_applies_for' is set to option 2 or 3)
        - `sender_domain_entries`: Enter the senders for this policy [comma separated]
                Required, if 'sender_add_domain_entries' is set to 'Yes'
        - `sender_add_ldap_group_membership`: Use LDAP group memberships for sender, "Yes" or "No".
                Default: No
        - `sender_ldap_group_name`: Enter groupname for LDAP query for sender, "Yes" or "No".
                Required, if 'sender_add_ldap_group_membership' is set to 'Yes'
        - `sender_ldap_group_query`: Select an LDAP group query for sender.
                Required, if 'sender_add_ldap_group_membership' is set to 'Yes'
        - `sender_add_another_group_membership`: Add another LDAP group membership for sender, "Yes" or "No".
                Default: No
                (Applicable if 'sender_add_ldap_group_membership' is set to 'Yes')
        - `add_receivers`: Add receivers for this policy, "Yes" or "No"
                Default: Yes
        - `receiver_policy_applies_for`: Policy applicable for receiver option.
                Default: 1
                Optioins:
                    1. All Receivers
                    2. Any of the added receivers
                    3. All of the added receivers
        - `receiver_add_domain_entries`: Enter receiver domain entries, "Yes" or "No".
                Default: Yes
                (Applicable if 'receiver_policy_applies_for' is set to option 2 or 3)
        - `receiver_domain_entries`: Enter the receivers for this policy [comma separated]
                Required, if 'receiver_add_domain_entries' is set to 'Yes'
        - `receiver_add_ldap_group_membership`: Use LDAP group memberships for receiver, "Yes" or "No".
                Default: No
        - `receiver_ldap_group_name`: Enter groupname for LDAP query for receiver.
                Required, if 'receiver_add_ldap_group_membership' is set to 'Yes'
        - `receiver_ldap_group_query`: Select an LDAP group query for receiver.
                Required, if 'receiver_add_ldap_group_membership' is set to 'Yes'
        - `receiver_add_another_group_membership`: Add another LDAP group membership for receiver, "Yes" or "No".
                Default: No
                (Applicable if 'receiver_add_ldap_group_membership' is set to 'Yes')
        - `add_exceptions`: Enter Exceptions for receiver.
                Default: No
                (Applicable if 'receiver_policy_applies_for' is set to option 3)
        - `exception_add_domain_entries`: Enter domain entries for exceptions, "Yes" or "No".
                Default: Yes
                (Applicable if 'add_exceptions' is set to 'Yes')
        - `exception_domain_entries`: Enter the exceptions for this policy [comma separated]
                Required, if 'exception_add_domain_entries' is set to 'Yes'
        - `exception_add_ldap_group_membership`: Use LDAP group membership exceptions, "Yes" or "No".
                Default: No
        - `exception_ldap_group_name`: Enter groupname for LDAP query for exception.
                Required, if 'exception_add_ldap_group_membership' is set to 'Yes'
        - `exception_ldap_group_query`: Select an LDAP group query for exception.
                Required, if 'exception_add_ldap_group_membership' is set to 'Yes'
        - `exception_add_another_group_membership`: Add another LDAP group membership exception, "Yes" or "No".
                Default: No
                (Applicable if 'exception_add_ldap_group_membership' is set to 'Yes')

        *Examples*:

        | Policyconfig Edit New | Incoming | test_policy |
        | ... | add_senders=yes                          |
        | ... | sender_policy_applies_for=2              |
        | ... | ender_add_domain_entries=Yes             |
        | ... | sender_domain_entries=@test.ibqa         |
        | ... | sender_add_ldap_group_membership=Y       |
        | ... | sender_ldap_group_name=ea_upq_admin      |
        | ... | sender_ldap_group_query=1                |
        | ... | sender_add_another_group_membership=No   |
        | ... | add_receivers=yes                        |
        | ... | receiver_policy_applies_for=3            |
        | ... | receiver_add_domain_entries=y            |
        | ... | receiver_domain_entries=test@            |
        | ... | receiver_add_ldap_group_membership=NO    |
        | ... | add_another_entry=N                      |
        | Commit                                         |


        """
        try:
            kwargs = self._convert_to_dict(args)
            self._cli.policyconfig().choose(policy_type).edit(policy_name).new(**kwargs)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_delete(self, policy_type, policy, policy_member=None):

        """
        This keyword delete given member from given Incoming policy

        policyconfig -> incoming -> Edit -> delete

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `policy_member`: policy member to be deleted.

        *Examples*:

        | Policyconfig Edit Delete | Incoming | re@mem.com |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).delete(policy_member)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_print(self, policy_type, policy):

        """
        This keyword prints all members from given Incoming policy

        policyconfig -> incoming -> Edit -> Print

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Print | Incoming |

        """
        try:
            return str(self._cli.policyconfig().choose(policy_type).edit(policy).print_members())
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antispam_enable(self, policy_type, policy, spam_dict=None, suspected_spam_dict=None):

        """
        This keyword enables anti-spam for given Incoming policy

        policyconfig -> incoming -> Edit -> Antispam -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `spam_dict`: Dictionary that holds below parameters related to Spam and
                       can be generated using keyword, spam_params_get.
        - `suspected_spam_dict`: Dictionary that holds below parameters related to Suspected Spam
                       can be generated using keyword, suspected_spam_params_get.

        *Examples*:

        | ${spam_dict} | get spam params | action_spam=DELIVER | text=SPAMMED |
        | ${suspected_spam_dict}= | Suspected Spam Params Get | action_spam_suspected=DROP |
        | Policyconfig Edit Antispam Enable | Incoming |
        | ... | mypolicy |
        | ... | ${spam_dict} |
        | ... | ${suspected_spam_dict} |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antispam().enable(spam_dict, suspected_spam_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antispam_disable(self, policy_type, policy):

        """
        This keyword disables anti-spam for given Incoming policy

        policyconfig -> incoming -> Edit -> Antispam -> disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Antispam Disable | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antispam().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antispam_default(self, policy_type, policy):

        """
        This keyword sets default for anti-spam for given Incoming policy

        policyconfig -> incoming -> Edit -> Antispam -> default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Antispam Default | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antispam().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antispam_edit(self, policy_type, policy, spam_dict=None,
                                        suspected_spam_dict=None):

        """
        This keyword edits anti-spam for given Incoming policy

        policyconfig -> incoming -> Edit -> Antispam -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `spam_dict`: Dictionary that holds below parameters related to Spam and
                       can be generated using keyword, spam_params_get.
        - `suspected_spam_dict`: Dictionary that holds below parameters related to Suspected Spam
                       can be generated using keyword, suspected_spam_params_get.

        *Examples*:
        | ${spam_dict}= | get spam params | action_spam=DELIVER | text=SPAMMED |
        | Policyconfig Edit Antispam Edit | Incoming |
        | ... | mypolicy |
        | ... | ${spam_dict} |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antispam(). \
                edit(spam_dict, suspected_spam_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antivirus_enable(self, policy_type, policy, antivirus_dict=None,
                                           repaired_dict=None, encrypted_dict=None,
                                           unscannable_dict=None, infected_dict=None):

        """
        This keyword enables anti-virus for given Incoming policy

        policyconfig -> incoming -> Edit -> antivirus -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `antivirus_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, antivirus_params_get.
        - `repaired_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, repaired_virus_params_get.
        - `encrypted_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, get_encryption_virus_params.
        - `unscannable_dict`: Dictionary that holds parameters related to Unscannable Message Handling
                            can be generated using keyword, unscannable_virus_params_get.
        - `infected_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, infected_virus_params_get.

        *Examples*:


        | ${antivirus_dict} | Antivirus Params Get | insert_xheader=Yes |
        | ${encrypted_dict} | Encrypted Virus Params Get | encrypted_edit=Yes |
        | ... | encrypted_action=5 |
        | Policyconfig Edit AntiVirus Enable | Incoming |
        | ... | mypolicy |
        | ... | ${antivirus_dict} |
        | ... | ${encrypted_dict} |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antivirus().enable(antivirus_dict,
                                                                                         repaired_dict, encrypted_dict,
                                                                                         unscannable_dict,
                                                                                         infected_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antivirus_disable(self, policy_type, policy):

        """
        This keyword disables anti-virus for given Incoming policy

        policyconfig -> incoming -> Edit -> antivirus -> disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit antivirus Disable | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antivirus().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antivirus_default(self, policy_type, policy):

        """
        This keyword is to set default for anti-virus for given Incoming policy

        policyconfig -> incoming -> Edit -> antivirus -> default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit antivirus Default | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antivirus().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_antivirus_edit(self, policy_type, policy, antivirus_dict=None,
                                         repaired_dict=None, encrypted_dict=None,
                                         unscannable_dict=None, infected_dict=None):

        """
        This keyword enables anti-virus for given Incoming policy

        policyconfig -> incoming -> Edit -> antivirus -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `antivirus_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, antivirus_params_get.
        - `repaired_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, repaired_virus_params_get.
        - `encrypted_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, get_encryption_virus_params.
        - `unscannable_dict`: Dictionary that holds parameters related to Unscannable Message Handling
                            can be generated using keyword, unscannable_virus_params_get.
        - `infected_dict`: Dictionary that holds settings for Antivirus and can be generated
                            using keyword, infected_virus_params_get.

        *Examples*:


        | ${infected_dict} | Infected Virus Params Get | infected_edit=Yes |
        | ... | encrypted_action | 5 |
        | Policyconfig Edit AntiVirus Enable | Incoming |
        | ... | mypolicy |
        | ... | ${infected_dict} |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).antivirus().edit(antivirus_dict,
                                                                                       repaired_dict, encrypted_dict,
                                                                                       unscannable_dict, infected_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_new(self, policy_type, filter_name, action,
                                 description=None, condition=None):
        """
        This keyword creates new Filter

        policyconfig -> incoming -> Filters -> New

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `description`: Description of the filter.
        - `action`: Dictionary containing parameters for action to be set.
                    can be generated using keyword, action_cond_params_get.
        - `condition`: Dictionary containing parameters for condition to be set.
                    can be generated using keyword, action_cond_params_get.
        - `url_category` : Select teh url categories here (comma seperated)
        - `url_whitelist`: Select the url whitelist here

        *Examples*:

        | ${action} | Action Cond Params Get | action_condition=Action |
        | ... | action=Insert A Custom Header |
        | ... | insert_header=X-ContFilt |
        | ... | value_header=filter match |

        | ${cond} | Action Cond Params Get | action_condition=Condition |
        | ... | sender_add=contfilt@somehost.qa |
        | Policyconfig Filters New | Incoming |
        | ... | mypolicy |
        | ... | ${action} |
        | ... | action |
        | ... | ${cond} |

        ${cond} | Action Cond Params Get | action_condition=Condition | condition=URL Category in Message Body | url_category=3,4 | url_whitelist=2 |
        | Policyconfig Filters New | Incoming |
        | ... |  newpolicy |
        | ... |  ${action} |
        | ... |  newpolicy |
        | ... |  ${cond} |
        Policyconfig Filters New | Outgoing |
        | ... |  newpolicy1 |
        | ... |  ${action1} |
        | ... |  newpolicy1 |
        | ... |  ${cond} |
        | Policyconfig Filters New | Incoming |
        | ... |  newpolicy2 |
        | ... |  ${action2} |
        | ... |  newpolicy2 |
        | ... |  ${cond} |
        """
        try:
            action['action_condition'] = 'Action'
            self._cli.policyconfig().choose(policy_type). \
                filters().new(filter_name, description).add_save(action)
            if condition:
                condition['action_condition'] = 'Condition'
                self._cli.policyconfig().choose(policy_type). \
                    filters().edit(filter_name).add(condition)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_delete(self, policy_type, filter_name):
        """
        This keyword deletes given Filter

        policyconfig -> incoming -> Filters -> Delete

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.

        *Examples*:
        | Policyconfig Filters Delete Test | Incoming |
        | Policyconfig Filters Delete | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().delete(filter_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_print(self, policy_type):
        """
        This keyword prints all Filter

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.

        *Examples*:

        | Policyconfig Filters Print | Incoming |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().print_filters()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_rename(self, policy_type, filter_name, new_filter_name):
        """
        This keyword renames given Filter

        policyconfig -> incoming -> Filters -> Rename

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `new_filter_name`: New name of the filter.

        *Examples*:

        | Policyconfig Filters Rename | Incoming | mypolicy1 | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().rename(filter_name, new_filter_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_add(self, policy_type, filter_name, input_dict):
        """
        This keyword adds new condition or action to given Filter

        policyconfig -> incoming -> Filters -> Edit -> Add

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `input_dict`: Dictionary holding parameters for action or condition to be
                        added. can be generated using keyword, action_cond_params_get.

        *Examples*:

        | ${cond} | Action Cond Params Get | action_condition=Condition |
        | ... | condition=Envelope Sender Address |
        | ... | sender_add=contfilt@somehost.qa |
        | Policyconfig Filters Edit Add | Incoming | mypolicy | ${cond} |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).add(input_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_rename(self, policy_type, filter_name, new_filter_name):
        """
        This keyword renames given Filter

        policyconfig -> incoming -> Filters -> Edit -> Rename

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `new_filter_name`: New name of the filter.

        *Examples*:

        | Policyconfig Filters Edit Rename | Incoming | mypolicy1 | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).rename(new_filter_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_desc(self, policy_type, filter_name, description):
        """
        This keyword changes description of given Filter

        policyconfig -> incoming -> Filters -> Edit -> Desc

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `description`: New description of the filter.

        *Examples*:

        | Policyconfig Filters Edit Desc | Incoming | mypolicy | This is test |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).desc(description)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_delete(self, policy_type, filter_name, *args):
        """
        This keyword deletes condition or action from given Filter

        policyconfig -> incoming -> Filters -> Edit -> Delete

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `action_condition`: New name of the filter.
        - `condition`: number of the Condition to be deleted.
        - `action`: number of the Action to be deleted.
        *Examples*:

        | Policyconfig Filters Edit Delete | Incoming | mypolicy |
        | ... | condition=1 |

        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).delete(**kwargs)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_move(self, policy_type, filter_name, *args):
        """
        This keyword moves given Condition or Action to given position

        policyconfig -> incoming -> Filters -> Edit -> Move

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        - `action_condition`: action or condition.
        - `to_move`: number of the Condition or Action to move.
        - `position`: new position.

        *Examples*:

        | Policyconfig Filters Edit Move | Incoming | mypolicy |
        | ... | to_move=2 |
        | ... | position=1 |

        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).move(**kwargs)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_filters_edit_toggle_all(self, policy_type, filter_name):
        """
        This keyword is to Toggle which conditions must be true for given Filter

        policyconfig -> incoming -> Filters -> Edit -> Rename

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `filter_name`: Name of the filter.
        *Examples*:

        | Policyconfig Filters Edit Toggle All | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                filters().edit(filter_name).toggle_all()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_filters_enable(self, policy_type, policy, filter_to_enable):
        """
        This keyword enables given Filter for given policy

        policyconfig -> incoming -> Edit -> Filters -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `filter_to_enable`: filter to be enabled.

        *Examples*:

        | Policyconfig Edit Filters Enable | Incoming | mypolicy | myfilter |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).filters().enable(filter_to_enable)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_filters_edit(self, policy_type, policy, filter_to_toggle):
        """
        This keyword edit given Filter to toggle for given policy

        policyconfig -> incoming -> Edit -> Filters -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `filter_to_toggle`: filter to be toggled between enabled and disabled.

        *Examples*:

        | Policyconfig Edit Filters Edit | Incoming | mypolicy | myfilter |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).filters().edit(filter_to_toggle)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_filters_default(self, policy_type, policy):
        """
        This keyword sets default Filter settings for given policy

        policyconfig -> incoming -> Edit -> Filters -> Default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.

        *Examples*:

        | Policyconfig Edit Filters Default | Incoming |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).filters().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_filters_disable(self, policy_type, policy):
        """
        This keyword disables Filter settings for given policy

        policyconfig -> incoming -> Edit -> Filters -> Disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.

        *Examples*:

        | Policyconfig Edit Filters Disable | Incoming |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).filters().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_outbreak_enable(self, policy_type, policy, *args):
        """
        This keyword enables outbreak for given policy

        policyconfig -> incoming -> Edit -> Outbreak -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `file_extension`: file_extension that bypass Outbreak Filters.
        - `retention_attachment` - maximum retention period for viral attachment
        - `deliver_all` :  deliver all non viral threat messages without quarantining
        - `include_outbreak_header` : Enable X-IronPort-Outbreak headers in messages
        - `status_header_appear` : X-IronPort-Outbreak-Status header should appear
        - `enable_description_header` : Enable the X-IronPort-Outbreak-Description
                                        header
        - `enable_alternate_destination` : Enable Alternate Destination Mailhost
        - `enter_alternate_destination` : Enter Alternate Destination Mailhost
        - `threshold_modify` - threshold value to modify messages
        - `add_text` - add text to the subject
        - `retention_all` - maximum retention period for all
        - `signed_message` - signed messages
        - `threshold_quarantine` - threshold value to quarantine messages
        - `domains` - Domain names
        - `proxy` - web security proxy
        - `add_disclaimer` - add a dislaimer, Yes or No
        - `disclaimer` - choose a disclaimer
        - `text` - text do you want
        - `modification` - enable the message modification
        - `exclude_domain` - like to specify a list of domains

        *Examples*:

        | Policyconfig Edit Outbreak Enable | Incoming | mypolicy |
        | ... | file_extension=exe |
        | ... | threshold_quarantine=5 |

        """
        kwargs = self._convert_to_dict(args)
        try:
            file_extension = kwargs.pop("file_extension", None)
            if file_extension:
                self._cli.policyconfig().choose(policy_type).edit(policy). \
                    vof().enable(YES, kwargs).new(file_extension)
            else:
                self._cli.policyconfig().choose(policy_type).edit(policy). \
                    vof().enable(NO, kwargs)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_outbreak_edit(self, policy_type, policy, *args):
        """
        This keyword edit outbreak settings for given policy

        policyconfig -> incoming -> Edit -> Outbreak -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `file_extension`: file_extension that bypass Outbreak Filters.
        - `retention_attachment` - maximum retention period for viral attachment
        - `deliver_all` :  deliver all non viral threat messages without quarantining
        - `include_outbreak_header` : Enable X-IronPort-Outbreak headers in messages
        - `status_header_appear` : X-IronPort-Outbreak-Status header should appear
        - `enable_description_header` : Enable the X-IronPort-Outbreak-Description
                                        header
        - `enable_alternate_destination` : Enable Alternate Destination Mailhost
        - `enter_alternate_destination` : Enter Alternate Destination Mailhost
        - `threshold_modify` - threshold value to modify messages
        - `add_text` - add text to the subject
        - `retention_all` - maximum retention period for all
        - `signed_message` - signed messages
        - `threshold_quarantine` - threshold value to quarantine messages
        - `domains` - Domain names
        - `proxy` - web security proxy
        - `add_disclaimer` - add a dislaimer, Yes or No
        - `disclaimer` - choose a disclaimer
        - `text` - text do you want
        - `modification` - enable the message modification
        - `exclude_domain` - like to specify a list of domains

        *Examples*:

        | Policyconfig Edit Outbreak Edit | Incoming | mypolicy |
        | ... | file_extension=exe |
        | ... | threshold_quarantine=5 |

        """
        kwargs = self._convert_to_dict(args)
        try:
            file_extension = kwargs.pop("file_extension", None)
            if file_extension:
                self._cli.policyconfig().choose(policy_type).edit(policy). \
                    vof().edit('y', kwargs).new(file_extension)
            else:
                self._cli.policyconfig().choose(policy_type).edit(policy). \
                    vof().edit('n', kwargs)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_outbreak_disable(self, policy_type, policy):
        """
        This keyword disable outbreak settings for given policy

        policyconfig -> incoming -> Edit -> Outbreak -> Disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.

        *Examples*:

        | Policyconfig Edit Outbreak Disable | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).vof().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_outbreak_default(self, policy_type, policy):
        """
        This keyword sets default outbreak settings for given policy

        policyconfig -> incoming -> Edit -> Outbreak -> Default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.

        *Examples*:

        | Policyconfig Edit Outbreak Default | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).vof().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_assign_add(self, policy_type, policy, user_role):
        """
        This keyword assigns given user_role to given policy

        policyconfig -> incoming -> Edit -> Assign -> Add

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `user_role`: user role to be added.

        *Examples*:

        | Policyconfig Edit Assign Add | Incoming | mypolicy | custom |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).assign().add(user_role)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_assign_delete(self, policy_type, policy, user_role):
        """
        This keyword deletes given user_role from given policy

        policyconfig -> incoming -> Edit -> Assign -> Delete

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Policy to be edited.
        - `user_role`: user role to be deleted.

        *Examples*:

        | Policyconfig Edit Assign Delete | Incoming | mypolicy | custom |

        """
        try:
            self._cli.policyconfig().choose(policy_type). \
                edit(policy).assign().delete(user_role)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_advancedmalware_enable(self, policy_type, policy, advancedmalware_dict=None):

        """
        This keyword enables Advancedmalware for given Incoming policy

        policyconfig -> incoming -> Edit -> Advancedmalware -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `advancedmalware_dict`: Dictionary that holds below parameters related to advanced malware
                                  protection and can be generated using keyword,amp_params_get.

        *Examples*:
        | Policyconfig Edit Advancedmalware Enable | Incoming | mypolicy | ${amp_dict}|

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy). \
                advancedmalware().enable(advancedmalware_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_advancedmalware_disable(self, policy_type, policy):

        """
        This keyword disables Advancedmalware for given Incoming policy

        policyconfig -> incoming -> Edit -> Advancedmalware -> disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Advancedmalware Disable | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).advancedmalware().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_advancedmalware_default(self, policy_type, policy):

        """
        This keyword sets default for Advancedmalware for given Incoming policy

        policyconfig -> incoming -> Edit -> Advancedmalware -> default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Advancedmalware Default | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).advancedmalware().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_advancedmalware_edit(self, policy_type, policy, advancedmalware_dict=None):

        """
        This keyword edits Advancedmalware for given Incoming policy

        policyconfig -> incoming -> Edit -> Antispam -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `amp_dict`: Dictionary that holds below parameters related to Malware and
                       can be generated using keyword, advancedmalware_params_get.

        *Examples*:
        | ${amp_dict}= | get spam params | action_spam=DELIVER | text=SPAMMED |
        | Policyconfig Edit Advancedmalware Edit | Incoming |
        | ... | mypolicy |
        | ... | ${am_pdict} |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).advancedmalware().edit(advancedmalware_dict)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_graymail_enable(self, policy_type, policy, safe_unsubscribe_dict=None,
                                          marketing_email_dict=None, social_networking_email_dict=None,
                                          bulk_email_dict=None):
        """
        This keyword enables Graymail for a given Incoming/Outgoing policy and also changes its config.

        policyconfig -> incoming/outgoing -> Edit -> Graymail -> Enable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `safe_unsubscribe_dict`: Dictionary that holds below parameters related to Safe Unsubscribe
                config & can be generated using 'Graymail Safe Unsubscribe Params Get' keyword.
        - `marketing_email_dict`: Dictionary that holds below parameters related to Marketing Emails
                config & can be generated using 'Graymail Marketing Email Params Get' keyword.
        - `social_networking_email_dict`: Dictionary that holds below parameters related to Social Networking Emails
                config & can be generated using 'Graymail Social Networking Email Params Get' keyword.
        - `bulk_email_dict`: Dictionary that holds below parameters related to Bulk Emails
                config & can be generated using 'Graymail Bulk Email Params Get' keyword.

        *Examples*:
        | ${safe_unsubscribe_dict}= |  Graymail Safe Unsubscribe Params Get |
        | ... | enable_safe_unsubscribe=Yes |
        | ${marketing_email_dict}= |  Graymail Marketing Email Params Get |
        | ... | enable_marketing_email_actions=Yes |
        | ... | marketing_mail_action=DROP |
        | ... | marketing_mail_archive_messages=No |
        | Policyconfig Edit Graymail Enable |
        | ... | Incoming |
        | ... | TestPol10 |
        | ... | ${safe_unsubscribe_dict} |
        | ... | ${marketing_email_dict} |
        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).graymail(). \
                enable(safe_unsubscribe_dict, marketing_email_dict, social_networking_email_dict, bulk_email_dict,
                       policy_type)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_graymail_disable(self, policy_type, policy):
        """
        This keyword disables Graymail for a given Incoming/Outgoing policy

        policyconfig -> incoming/outgoing -> Edit -> Graymail -> Disable

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Graymail Disable | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).graymail().disable()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_graymail_default(self, policy_type, policy):
        """
        This keyword resets Graymail config to DEFAULT for a given Incoming/Outgoing policy

        policyconfig -> incoming/outgoing -> Edit -> Graymail -> Default

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.

        *Examples*:

        | Policyconfig Edit Graymail Default | Incoming | mypolicy |

        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).graymail().default()
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def policyconfig_edit_graymail_edit(self, policy_type, policy, safe_unsubscribe_dict=None,
                                        marketing_email_dict=None, social_networking_email_dict=None,
                                        bulk_email_dict=None):
        """
        This keyword edit Graymail configurations for a given Incoming/Outgoing policy

        policyconfig -> incoming/outgoing -> Edit -> Graymail -> Edit

        *Parameters*:
        - `policy_type`: Policy Type, incoming or outgoing.
        - `policy`: Incoming policy name.
        - `safe_unsubscribe_dict`: Dictionary that holds below parameters related to Safe Unsubscribe
                config & can be generated using 'Graymail Safe Unsubscribe Params Get' keyword.
        - `marketing_email_dict`: Dictionary that holds below parameters related to Marketing Emails
                config & can be generated using 'Graymail Marketing Email Params Get' keyword.
        - `social_networking_email_dict`: Dictionary that holds below parameters related to Social Networking Emails
                config & can be generated using 'Graymail Social Networking Email Params Get' keyword.
        - `bulk_email_dict`: Dictionary that holds below parameters related to Bulk Emails
                config & can be generated using 'Graymail Bulk Email Params Get' keyword.

        *Examples*:
        | ${safe_unsubscribe_dict}= |  Graymail Safe Unsubscribe Params Get |
        | ... | enable_safe_unsubscribe=Yes |
        | ${marketing_email_dict}= |  Graymail Marketing Email Params Get |
        | ... | enable_marketing_email_actions=Yes |
        | ... | marketing_mail_action=DROP |
        | ... | marketing_mail_archive_messages=No |
        | Policyconfig Edit Graymail Edit |
        | ... | Incoming |
        | ... | TestPol10 |
        | ... | ${safe_unsubscribe_dict} |
        | ... | ${marketing_email_dict} |
        """
        try:
            self._cli.policyconfig().choose(policy_type).edit(policy).graymail(). \
                edit(safe_unsubscribe_dict, marketing_email_dict, social_networking_email_dict, bulk_email_dict,
                     policy_type)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
