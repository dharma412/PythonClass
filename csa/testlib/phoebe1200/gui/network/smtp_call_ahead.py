#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/network/smtp_call_ahead.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $


from common.gui.decorators import go_to_page, set_speed
from common.gui.guiexceptions import ConfigError, GuiValueError
from common.gui.guicommon import GuiCommon

ADD_PROFILE_BUTTON = "//input[@value='Add Profile...']"
PROFILES_TABLE = "//table[@class='cols']"
PROFILE_NAME_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                 (PROFILES_TABLE, name)
PROFILE_NAMES = "%s//tr[td]" % (PROFILES_TABLE,)
PROFILE_NAME_BY_IDX = lambda idx: "xpath=(%s)[%d]/td" % (PROFILE_NAMES, idx)
SERVER_TYPE_BY_IDX = lambda idx: "xpath=(%s)[%d]/td[2]" % (PROFILE_NAMES, idx)
PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                   "/following-sibling::td[2]/img" % (PROFILES_TABLE, name)
FLUSH_CACHE_BUTTON = "//input[@value='Flush Cache']"

PROFILE_NAME = "//input[@id='profile_name']"
PROFILE_TYPE = "//select[@id='profile_type']"
STATIC_CALL_AHEAD_SERVER = "//input[@id='static_server']"

ADVANCED_ARROW_CLOSED = "//div[@id='optionsLinkClosed']"
ADVANCED_INTERFACE = "//select[@id='interface']"
ADVANCED_MAIL_FROM = "//input[@id='mail_from_address']"
ADVANCED_REQUEST_TIMEOUT = "//input[@id='timeout_period']"
ADVANCED_VALIDATION_FAILURE_ACTION = "//select[@id='validation_failure_action']"
ADVANCED_VALIDATION_FAILURE_SMTP_CODE = "//input[@id='validation_failure_smtp_code']"
ADVANCED_VALIDATION_FAILURE_SMTP_TEXT = "//input[@id='validation_failure_smtp_text']"
ADVANCED_TEMPORARY_FAILURE_ACTION = "//select[@id='temp_failure_action']"
ADVANCED_TEMPORARY_FAILURE_SMTP_CODE = "//input[@id='temp_failure_smtp_code']"
ADVANCED_TEMPORARY_FAILURE_SMTP_TEXT = "//input[@id='temp_failure_smtp_text']"
ADVANCED_MAX_RECIPIENTS_PER_SESSION = "//input[@id='max_recipients']"
ADVANCED_MAX_CONNECTIONS_PER_SERVER = "//input[@id='max_connections']"
ADVANCED_CACHE_SIZE = "//input[@id='cache_size']"
ADVANCED_CACHE_TTL = "//input[@id='cache_ttl']"

PAGE_PATH = ('Network', 'SMTP Call-Ahead')


class SMTPCallAhead(GuiCommon):
    """Keywords for GUI interaction with Network -> SMTP Call-Ahead
    page"""

    def get_keyword_names(self):
        return ['smtp_call_ahead_add_profile',
                'smtp_call_ahead_edit_profile',
                'smtp_call_ahead_delete_profile',
                'smtp_call_ahead_is_profile_exist',
                'smtp_call_ahead_get_all_profiles',
                'smtp_call_ahead_flush_cache']

    def _edit_smtp_call_ahead_settings(self, settings):
        if settings.has_key('profile_name'):
            self.input_text(PROFILE_NAME, settings['profile_name'])
        else:
            raise GuiValueError('Must provide a SMTP Call-Ahead profile name')

        if settings.has_key('profile_type'):
            self.select_from_list(PROFILE_TYPE, settings['profile_type'])

            if settings['profile_type'].lower() == 'static call-ahead server':
                if settings.has_key('static_call_ahead_server'):
                    self.input_text(STATIC_CALL_AHEAD_SERVER, settings['static_call_ahead_server'])
                else:
                    raise GuiValueError('Must provide a SMTP Call-Ahead server name')

        if self._is_visible(ADVANCED_ARROW_CLOSED):
            self.click_element(ADVANCED_ARROW_CLOSED)
        if settings.has_key('interface'):
            self.select_from_list(ADVANCED_INTERFACE, settings['interface'])

        if settings.has_key('mail_from'):
            self.input_text(ADVANCED_MAIL_FROM, settings['mail_from'])

        if settings.has_key('request_timeout'):
            self.input_text(ADVANCED_REQUEST_TIMEOUT, settings['request_timeout'])

        if settings.has_key('validation_failure_action'):
            self.select_from_list(ADVANCED_VALIDATION_FAILURE_ACTION, settings['validation_failure_action'])
            if settings['validation_failure_action'].lower() == 'reject with custom code':
                if settings.has_key('validation_failure_smtp_code'):
                    self.input_text(ADVANCED_VALIDATION_FAILURE_SMTP_CODE, settings['validation_failure_smtp_code'])
                if settings.has_key('validation_failure_smtp_text'):
                    self.input_text(ADVANCED_VALIDATION_FAILURE_SMTP_TEXT, settings['validation_failure_smtp_text'])

        if settings.has_key('temporary_failure_action'):
            self.select_from_list(ADVANCED_TEMPORARY_FAILURE_ACTION, settings['temporary_failure_action'])
            if settings['temporary_failure_action'].lower() == 'reject with custom code':
                if settings.has_key('temporary_failure_smtp_code'):
                    self.input_text(ADVANCED_TEMPORARY_FAILURE_SMTP_CODE, settings['temporary_failure_smtp_code'])
                if settings.has_key('temporary_failure_smtp_text'):
                    self.input_text(ADVANCED_TEMPORARY_FAILURE_SMTP_TEXT, settings['temporary_failure_smtp_text'])

        if settings.has_key('max_recipients_per_session'):
            self.input_text(ADVANCED_MAX_RECIPIENTS_PER_SESSION, settings['max_recipients_per_session'])

        if settings.has_key('max_connections_per_server'):
            self.input_text(ADVANCED_MAX_CONNECTIONS_PER_SERVER, settings['max_connections_per_server'])

        if settings.has_key('cache_size'):
            self.input_text(ADVANCED_CACHE_SIZE, settings['cache_size'])

        if settings.has_key('cache_ttl'):
            self.input_text(ADVANCED_CACHE_TTL, settings['cache_ttl'])

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_add_profile(self, settings={}):
        """Add new SMTP Call-Ahead profile

        *Parameters:*
            Takes a dictionary with below parameters:
            -`profile_name`: Name of the SMTP Call-Ahead profile.
            -`profile_type`: Type of Call-Ahead server.
            -`static_call_ahead_server`: Host name of the Static Call-Ahead Server.
                Valid when "profile_type" parameter is set to "Static Call-Ahead Server"
                Default: "Use Delivery Host"
            -`interface`: Interface name to be used. Default: "Auto"
            -`mail_from`: Mail From Address. Default <BLANK>
            -`request_timeout`: Validation Request Timeout value. Default: 30 seconds.
            -`validation_failure_action`: Action for Validation Filure. Default: "Accept".
            -`validation_failure_smtp_code`: Custom SMTP code to be used for validation failure.
                Valid when "validation_failure_action" is set to "Reject with Custom Code".
            -`validation_failure_smtp_text`: Custom SMTP response message for validation failure.
                Valid when "validation_failure_action" is set to "Reject with Custom Code".
            -`temporary_failure_action`: Action for Temporary failure. Default: "Reject".
            -`temporary_failure_smtp_code`: Custom SMTP code to be used for temporary failure.
                Valid when "temporary_failure_action" is set to "Reject with Custom Code".
            -`temporary_failure_smtp_text`: Custom SMTP response message for temporary failure.
                Valid when "temporary_failure_action" is set to "Reject with Custom Code".
            -`max_recipients_per_session`: Number of maximum recipients per session.
            -`max_connections_per_server`: Number of maximum connection per server.
            -`cache_size`: Size of cache.
            -`cache_ttl`: TTL (time to live) of cache.

        *Exceptions:*
        - `ConfigError`: If profile with given name already exists
        - `GuiValueError`: If any wrong value is provided for any GUI field.

        """
        if self._is_element_present(PROFILE_NAME_LINK(settings['profile_name'])):
            raise ConfigError('SMTP Call-Ahead profile named "%s" is ' \
                              'already present in profiles list' % settings['profile_name'])

        self.click_button(ADD_PROFILE_BUTTON)
        self._edit_smtp_call_ahead_settings(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_edit_profile(self, settings={}):
        """Edit existing SMTP Call-Ahead profile

        *Parameters:*
            Takes a dictionary with below parameters:
            -`profile_name`: Name of the SMTP Call-Ahead profile.
            -`profile_type`: Type of Call-Ahead server.
            -`static_call_ahead_server`: Host name of the Static Call-Ahead Server.
                Valid when "profile_type" parameter is set to "Static Call-Ahead Server"
                Default: "Use Delivery Host"
            -`interface`: Interface name to be used. Default: "Auto"
            -`mail_from`: Mail From Address. Default <BLANK>
            -`request_timeout`: Validation Request Timeout value. Default: 30 seconds.
            -`validation_failure_action`: Action for Validation Filure. Default: "Accept".
            -`validation_failure_smtp_code`: Custom SMTP code to be used for validation failure.
                Valid when "validation_failure_action" is set to "Reject with Custom Code".
            -`validation_failure_smtp_text`: Custom SMTP response message for validation failure.
                Valid when "validation_failure_action" is set to "Reject with Custom Code".
            -`temporary_failure_action`: Action for Temporary failure. Default: "Reject".
            -`temporary_failure_smtp_code`: Custom SMTP code to be used for temporary failure.
                Valid when "temporary_failure_action" is set to "Reject with Custom Code".
            -`temporary_failure_smtp_text`: Custom SMTP response message for temporary failure.
                Valid when "temporary_failure_action" is set to "Reject with Custom Code".
            -`max_recipients_per_session`: Number of maximum recipients per session.
            -`max_connections_per_server`: Number of maximum connection per server.
            -`cache_size`: Size of cache.
            -`cache_ttl`: TTL (time to live) of cache.

        *Exceptions:*
        - `ConfigError`: If profile with given name already exists
        - `GuiValueError`: If any wrong value is provided for any GUI field.
        """

        if not self._is_element_present(PROFILE_NAME_LINK(settings['profile_name'])):
            raise ConfigError('SMTP Call-Ahead profile named "%s" does not exist ' \
                              % settings['profile_name'])

        self.click_button(PROFILE_NAME_LINK(settings['profile_name']))
        self._edit_smtp_call_ahead_settings(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_delete_profile(self, profile_name):
        """Delete existing SMTP Call-Ahead profile

        *Parameters:*
        - `profile_name`: existing SMTP Call-Ahead profile name or 'all'
        to clear all existing SMTP Call-Ahead profiles.
        If there are no profiles and the keyword was invoked with
        'all' parameter then it will return silently.

        *Exceptions:*
        - `ValueError`: if profile with given name does not exist

        *Examples:*
        """

        if not self._is_element_present(PROFILE_DELETE_LINK(profile_name)):
            raise ValueError('SMTP Call-Ahead profile named "%s" is not ' \
                             'present in profiles list' % (profile_name,))
        self.click_button(PROFILE_DELETE_LINK(profile_name), 'don\'t wait')
        self._click_continue_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_is_profile_exist(self, profile_name):
        """Return whether SMTP Call-Ahead profile with given name exists on appliance

        *Parameters:*
        - `profile_name`: existing SMTP Call-Ahead profile name

        *Return:*
        ${True} if profile exists and ${False} otherwise

        *Examples:*
        | Verify Profile Existence |
        |  | [Arguments] | ${profile_name} | ${should_exist}=${True} |
        |  | ${is_exist}= | SMTP Call Ahead Is Profile Exist | ${profile_name} |
        |  | ${verifier_kw}= | Set Variable If | ${should_exist} |
        |  | ... | Should Be True | Should Not Be True |
        |  | Run Keyword | ${verifier_kw} | ${is_exist} |
        """
        return self._is_element_present(PROFILE_NAME_LINK(profile_name))

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_get_all_profiles(self):
        """Return all existing SMTP Call-Ahead profiles

        *Return:*
        A list of dictionaries which keys are *Profile Name* and *Server Type*

        *Examples:*
        | ${profiles_info}= | SMTP Call Ahead Get All Profiles |
        | Log Dictionary | ${profiles_info} |
        | ${profile_names}= | Get From Dictionary | ${profiles_info} | Profile Name |
        | :FOR | ${profile_name} | IN | @{ALL_PROFILE_NAMES} |
        | \ | ${server_type}= | Get From Dictionary | ${profiles_info} | ${profile_name} |
        | \ | Should Be Equal As Strings | ${server_type} | Static Call-Ahead Server |
        """

        result = {}
        profiles_count = int(self.get_matching_xpath_count(PROFILE_NAMES))
        for profile_idx in xrange(1, 1 + profiles_count):
            profile_name = self.get_text(PROFILE_NAME_BY_IDX(profile_idx)).strip()
            server_type = self.get_text(SERVER_TYPE_BY_IDX(profile_idx)).strip()
            result[profile_name] = server_type
        return result

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_call_ahead_flush_cache(self, confirm_cache_clear=True):
        """Clears SMTP Call-Ahead profiles' cache.

        *Parameters:*
        - `confirm_cache_clear`: Whether to flush SMTP Call-Ahead cache or not.
           Default value: True

        *Return:*
        None.

        *Examples:*
        | Smtp Call Ahead Flush Cache |
        | Smtp Call Ahead Flush Cache | confirm_cache_clear=${False} |
        """

        self.click_button(FLUSH_CACHE_BUTTON, 'don\'t wait')
        if confirm_cache_clear:
            self._click_continue_button(text='Flush Cache')
        else:
            self._click_continue_button(text='Cancel')
