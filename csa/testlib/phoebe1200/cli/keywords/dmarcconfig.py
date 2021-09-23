#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/dmarcconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class dmarcconfig(CliKeywordBase):
    """Keywords for dmarcconfig cli command. """

    def get_keyword_names(self):
        return ['dmarc_config_setup',
                'dmarc_config_profiles_new',
                'dmarc_config_profiles_edit',
                'dmarc_config_profiles_delete',
                'dmarc_config_profiles_print',
                'dmarc_config_profiles_import',
                'dmarc_config_profiles_export',
                'dmarc_config_profiles_clear'
                ]

    def dmarc_config_setup(self, *args):
        """Setup - Change Global Settings in dmarcconfig

        CLI command: dmarcconfig > setup

        *Parameters:*
        - `modify_dmarc_report`: modify DMARC report settings?. YES or NO.
                                 No by default.
        - `time_report`: time of day to generate aggregate feedback reports.
                         Use 24-hour format (HH:MM)
        - `send_report`: Would you like to send DMARC error reports? YES or NO.
        - `entity_name` : Enter the entity name responsible for report
                          generation. This is added to the DMARC aggregate
                          reports.
        - `additional_contact` : Enter additional contact information to be
                                 added to DMARC aggregate reports. This could be
                                 an email address, URL of a website with
                                 additional help, a phone number etc.
        - `send_copy`: Would you like to send a copy of all aggregate reports?
                       YES or NO
        - `email_addresses` : Enter a comma separated list of email addresses to
                              send a copy of all aggregate reports
        - `bypass_addresslist` : Would you like to bypass DMARC verification for
                                 an addresslist? YES or NO
        - `address_list` : Select the address list to bypass DMARC verification
        - `bypass_header` : Would you like to bypass DMARC verification for
                            specific header fields? YES or NO
        - `add_header` : Enter the header field name. String
        - `remove_header` : Enter the number of header field to remove from the
                            list.

        *Return:*
        None

        *Examples:*
        | Dmarc Config Setup | modify_dmarc_report=yes | send_report=yes |
        | Dmarc Config Setup | bypass_addresslist=yes | add_header=hello |
        | Dmarc Config Setup | bypass_addresslist=yes | remove_header=1 |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().setup(**kwargs)

    def dmarc_config_profiles_new(self, *args):
        """Add dmarcconfig profile

        CLI command: dmarcconfig > Profiles -> New

        *Parameters:*
        - `name`: Enter the name of the new DMARC verification profile
        - `reject_action` : Select the message action when the DMARC policy is
                            reject as per the table below
        | 1 | No Action |
        | 2 | Quarantine the message |
        | 3 | Reject the message |

        - `select_quarantine_reject` : Select the quarantine for messages that
           fail DMARC verification (when the policy action is reject).
        - `smtp_response_code` : Enter the SMTP response code for rejected
                                 messages
        - `smtp_response_text` : Enter the SMTP response text for rejected
                                 messages
        - `quarantine_action` : Select the message action when the DMARC policy
                                is quarantine as per the table below
        | 1 | No Action |
        | 2 | Quarantine the message |
        - `select_quarantine` : Select the quarantine for messages that fail
           DMARC verification (when the policy action is quarantine).
        - `smtp_action_temporary` : What SMTP action should be taken in case of
                                    temporary failure? as per table below
        | 1 | Accept |
        | 2 | Reject |
        - `smtp_code_temporary` : Enter the SMTP response code for rejected
                                  messages in case of temporary failure
        - `smtp_text_temporary` : Enter the SMTP response text for rejected
                                  messages in case of temporary failure
        - `smtp_action_permanent` : What SMTP action should be taken in case of
                                    permanent failure? as per table below
        | 1 | Accept |
        | 2 | Reject |
        - `smtp_code_permanent` : Enter the SMTP response code for rejected
                                  messages in case of permanent failure
        - `smtp_text_permanent` : Enter the SMTP response text for rejected
                                  messages in case of permanent failure

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles New | name=test | reject_action=2 |
        | ... select_quarantine_reject=1 |
        | Dmarc Config Profiles New | name=test | reject_action=1 |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles().new(**kwargs)

    def dmarc_config_profiles_edit(self, *args):
        """Edit dmarcconfig profile

        CLI command: dmarcconfig > Profiles -> Edit

        *Parameters:*
        - `profile_name`: Name of the profile to be edited
        - `name`: name of DMARC verification profile
        - `reject_action` : Select the message action when the DMARC policy is
                            reject as per the table below
        | 1 | No Action |
        | 2 | Quarantine the message |
        | 3 | Reject the message |

        - `select_quarantine_reject` : Select the quarantine for messages that
           fail DMARC verification (when the policy action is reject).
        - `smtp_response_code` : Enter the SMTP response code for rejected
                                 messages
        - `smtp_response_text` : Enter the SMTP response text for rejected
                                 messages
        - `quarantine_action` : Select the message action when the DMARC policy
                                is quarantine as per the table below
        | 1 | No Action |
        | 2 | Quarantine the message |
        - `select_quarantine` : Select the quarantine for messages that fail
           DMARC verification (when the policy action is quarantine).
        - `smtp_action_temporary` : What SMTP action should be taken in case of
                                    temporary failure? as per table below
        | 1 | Accept |
        | 2 | Reject |
        - `smtp_code_temporary` : Enter the SMTP response code for rejected
                                  messages in case of temporary failure
        - `smtp_text_temporary` : Enter the SMTP response text for rejected
                                  messages in case of temporary failure
        - `smtp_action_permanent` : What SMTP action should be taken in case of
                                    permanent failure? as per table below
        | 1 | Accept |
        | 2 | Reject |
        - `smtp_code_permanent` : Enter the SMTP response code for rejected
                                  messages in case of permanent failure
        - `smtp_text_permanent` : Enter the SMTP response text for rejected
                                  messages in case of permanent failure

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles Edit | profile_name=test | name=test1 |
        | ... select_quarantine_reject=1 |

        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles(). \
            edit(kwargs.pop('profile_name', None), **kwargs)

    def dmarc_config_profiles_delete(self, *args):
        """
        Delete the dmarc profile
        CLI command: dmarcconfig > Profiles -> Delete

        *Parameters:*
        - `profile_name`: Name of the profile to be deleted

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles Delete | profile_name=test |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles().delete(**kwargs)

    def dmarc_config_profiles_print(self, *args):
        """
        Print the dmarc profile details
        CLI command: dmarcconfig > Profiles -> Print

        *Parameters:*
        - `profile_name`: Name of the profile to be printed

        *Return:*
        Details of the profile

        *Examples:*
        | ${profile_detail}= | Dmarc Config Profiles Print | profile_name=test |
        | Log | ${profile_detail} |
        """

        kwargs = self._convert_to_dict(args)
        return self._cli.dmarcconfig().profiles().Print(**kwargs)

    def dmarc_config_profiles_import(self, *args):
        """
        Import the dmarc profile from file
        CLI command: dmarcconfig > Profiles ->  Import

        *Parameters:*
        - `file_name`: Enter the name of the file on machine

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles Import | file_name=testfile |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles().Import(**kwargs)

    def dmarc_config_profiles_export(self, *args):
        """
        Export the dmarc profile to file
        CLI command: dmarcconfig > Profiles ->  Export

        *Parameters:*
        - `file_name`: Enter the name for the exported file

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles Export | file_name=testfile |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles().export(**kwargs)

    def dmarc_config_profiles_clear(self, *args):
        """
        Clear all the dmarc verification profiles
        CLI command: dmarcconfig > Profiles -> Clear

        *Parameters:*
        - `confirm` : Are you sure you want to clear profiles? YES or NO
                      Default is NO

        *Return:*
        None

        *Examples:*
        | Dmarc Config Profiles Clear | confirm=YES |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.dmarcconfig().profiles().clear(**kwargs)
