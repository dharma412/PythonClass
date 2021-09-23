#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase, DEFAULT
import traceback

class CallaheadConfig(CliKeywordBase):
    """
    cli -> callaheadconfig

    Provides keywords for configuring SMTP Call-Ahead profiles
    """

    def get_keyword_names(self):
        return ['callahead_config_new',
                'callahead_config_edit',
                'callahead_config_delete',
                'callahead_config_print',
                'callahead_config_test',
                'callahead_config_flushcache',
                ]

    def callahead_config_new(self, *args):
        """
        Creates new SMTP Call-Ahead profile.

        callaheadconfig -> new

        *Parameters*:
        - `profile_type`: Specify type of profile. Either '1' or '2'.
          1 -> Delivery Host. 2 -> Static Call-Ahead Servers.
        - `profile_name`: Name of the profile
        - `call_ahead_servers`: Specify one or more Call-Ahead servers
          hostname separated by commas
        - `advanced_settings`: Change advanced settings. Either 'yes' or 'no'
        - `mail_from`: Specify MAIL FROM address
        - `ip_interface`: Specify the IP interface for this profile
        - `request_timeout`: Specify the validation request timeout (in seconds)
        - `action_for_recipients`: Specify the default action for
          non-verifiable recipients. Either '1' or '2'.
          1 -> ACCEPT. 2 -> REJECT
        - `action_for_failure`: Specify the default action for temporary
          failure (4xx error). Either '1' or '2' or '3'.
          1 -> REJECT with same code. 2-> REJECT with custom code. 3-> ACCEPT
        - `smtp_code`: Specify the custom SMTP response code
        - `smtp_text`: Specify the custom SMTP response text
        - `max_rcpt_session`: Speciy the maximum number of recipients
          to validate per SMTP session
        - `max_simultaneous_conn`: Specify the maximum number of simultaneous
          connections to Call-Ahead server
        - `cache_entries`: Specify cache entries
        - `cache_ttl`: Specify cache TTL (in seconds)

        *Examples*:
        | Callahead Config New | profile_type=1 | profile_name=test |
        | ... | advanced_settings=yes | max_rcpt_session=2 |
        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.callaheadconfig().new(**kwargs)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def callahead_config_edit(self, *args):
        """
        Modify an existing SMTP Call-Ahead profile.

        callaheadconfig -> edit

        *Parameters*:
        - `profile_edit`: Specify the profile to be edited
        - `profile_type`: Specify type of profile. Either '1' or '2'.
          1 -> Delivery Host. 2 -> Static Call-Ahead Servers
        - `profile_name`: Name of the profile
        - `call_ahead_servers`: Specify one or more Call-Ahead servers
          hostname separated by commas
        - `advanced_settings`: Change advanced settings. Either 'yes' or 'no'
        - `mail_from`: Specify MAIL FROM address
        - `ip_interface`: Specify the IP interface for this profile
        - `request_timeout`: Specify the validation request timeout (in seconds)
        - `action_for_recipients`: Specify the default action for
          non-verifiable recipients. Either '1' or '2'.
          1 -> ACCEPT. 2 -> REJECT
        - `action_for_failure`: Specify the default action for temporary
          failure (4xx error). Either '1' or '2' or '3'.
          1 -> REJECT with same code. 2-> REJECT with custom code. 3-> ACCEPT
        - `smtp_code`: Specify the custom SMTP response code
        - `smtp_text`: Specify the custom SMTP response text
        - `max_rcpt_session`: Speciy the maximum number of recipients
          to validate per SMTP session
        - `max_simultaneous_conn`: Specify the maximum number of simultaneous
          connections to Call-Ahead server
        - `cache_entries`: Specify cache entries
        - `cache_ttl`: Specify cache TTL (in seconds)

        *Examples*:
        | Callahead Config Edit | profile_edit=1 | profile_type=2 |
        | ... | profile_name=newtest | call_ahead_servers=ss.com |
        | ... | advanced_settings=yes | max_rcpt_session=3 |
        | ... | action_for_failure=2 | smtp_code=460 | smtp_text=smtp fail |
        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.callaheadconfig().edit(**kwargs)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def callahead_config_delete(self, profile_name):
        """
        Deletes SMTP Call-Ahead profile.

        callaheadconfig -> delete

        *Parameters*:
        - `profile_name`: Name of the profile to be deleted

        *Examples*:
        | Callahead Config Delete | newtest |
        """
        try:
            self._cli.callaheadconfig().delete(profile_name=profile_name)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def callahead_config_print(self, profile_name):
        """
        Displays SMTP Call-Ahead profile.

        callaheadconfig -> print

        *Parameters*:
        - `profile_name`: Name of the profile to be displayed

        *Examples*:
        | ${Output}= | Callahead Config Print | newtest |
        """
        try:
            return self._cli.callaheadconfig().\
              print_method(profile_name=profile_name)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def callahead_config_test(self, profile_name, address, ldap=DEFAULT):
        """
        Tests the SMTP Call-Ahead profile created

        callaheadconfig -> test

        *Parameters*:
        - `profile_name`: Name of the profile to be tested
        - `address`: Specify the recipient address to verify
        - `ldap`: Specify a LDAP-Routing query configured on the system
          to be used for the test. Default is None.

        *Examples*:
        | ${Test_Status}= | Callahead Config Test | newtest | ss@ss.com |
        """
        try:
            return self._cli.callaheadconfig().\
              test(profile_name, address, ldap=ldap)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def callahead_config_flushcache(self, profile_name='all', confirm='yes'):
        """
        Flushes SMTP Call-Ahead cache

        callaheadconfig -> flushcache

        *Parameters*:
        - `profile_name`: Name of the profile to be flushed
        - `confirm`: Confirm flush of cached SMTP Call-Ahead results.
          Either 'yes' or 'no'

        *Examples*:
        | Callahead Config FlushCache | profile_name=newtest | confirm=yes |
        | Callahead Config FlushCache | profile_name=all |
        """
        try:
            self._cli.callaheadconfig().flushcache(profile_name=profile_name,\
              confirm=self._process_yes_no(confirm))
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e


