#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/monitor/quarantines/spam.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from locators import *
from qcommon import QuarantinesCommon
from qexceptions import QuarantineIsAlreadyEnabled
import re

from common.gui.decorators import set_speed


class SpamQuarantine(QuarantinesCommon):
    """
    Class to manage Spam Quarantine settings.
    """
    sq = 'Spam Quarantine'

    def _open_spam_page(self):
        self._navigate_to('Monitor', self.sq)

    def _edit_spam_page(self):
        self._open_spam_page()
        link = self._get_edit_quarantine_link(self.sq)
        self.click_element(link)

    def _set_local_users_sq(self, local_users, confirm):
        """
        Set Spam Quarantine administrative users.
        """
        if local_users is None:
            return None
        self._debug \
            ('Set administrative local users allowed to access the quarantine')
        err = 'No Local Users found for assignment'
        not_found = 'User not found for assignment'
        self._set_items(SPAM_QUARANTINE_USERS_LINK,
                        SPAM_QUARANTINE_USERS_DIALOG,
                        'adminusers',
                        local_users,
                        err,
                        not_found,
                        confirm)

    def _set_ext_groups_sq(self, ext_groups, confirm):
        """
        Set Spam Quarantine administrative groups.
        """
        if ext_groups is None:
            return None
        self._debug \
            ('Set administrative external auth groups allowed to access the quarantine')
        err = 'No External Groups found for assignment'
        not_found = 'External Group not found for assignment'
        self._set_items(SPAM_QUARANTINE_EXT_GROUPS_LINK,
                        SPAM_QUARANTINE_EXT_GROUPS_DIALOG,
                        'external_admin_groups',
                        ext_groups,
                        err,
                        not_found,
                        confirm)

    def _set_custom_roles_sq(self, custom_roles, confirm):
        """
        Set Spam Quarantine administrative roles.
        """
        self._set_custom_roles_common(SPAM_QUARANTINE_CUSTOM_ROLES_LINK,
                                      SPAM_QUARANTINE_CUSTOM_ROLES_DIALOG,
                                      custom_roles,
                                      confirm)

    def _enable_spam_quarantine(self):
        """
        Click link to enable spam quarantine and select checkbox.
        """
        row_idx, col_idx = self._is_quarantine_present(self.sq)
        if self._is_enabled(row_idx):
            raise QuarantineIsAlreadyEnabled(self.sq)
        link = \
            "%s//tr[%s]/td[1]/a[text()='Enable']" % (QUARANTINES_TABLE, row_idx)
        self.click_element(link)
        # select checkbox if it is not selected
        self._select_checkbox(SPAM_QUARANTINE_ENABLE_DISABLE)

    def _disable_spam_quarantine(self):
        """
        Open Spam Quarantine edit page and un-select checkbox.
        """
        self._edit_spam_page()
        self._unselect_checkbox(SPAM_QUARANTINE_ENABLE_DISABLE)

    def _spam_quarantine_set_main_settings(self,
                                           delete_oldest=None,
                                           scheduled_delete=None,
                                           scheduled_delete_ttl=None,
                                           notify_ironport_on_release=None):
        """
        Defines Spam Quarantine main settings.

        This method is used for both
        - enabling Spam Quarantine;
        - modifying previously configured Spam Quarantine.

        For this reason arguments like 'scheduled_delete_ttl' may not depend on
        'scheduled_delete'. For example, when user modifies Spam Quarantine and
        does not provide 'scheduled_delete' option in function call(defaults to None) but it
        is selected in WUI - we should allow configuring other options like 'scheduled_delete_ttl'
        by getting real state of 'scheduled_delete'.
        """
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_OUT_OF_LIMIT_ACTION, delete_oldest)
        if scheduled_delete is not None:
            if scheduled_delete:
                self._click_radio_button \
                    (SPAM_QUARANTINE_ENABLE_SCHEDULED_DELETE(0))
            else:
                self._click_radio_button \
                    (SPAM_QUARANTINE_ENABLE_SCHEDULED_DELETE(1))
        if self._is_checked(SPAM_QUARANTINE_ENABLE_SCHEDULED_DELETE(0)):
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_SCHEDULED_DELETE_TTL, scheduled_delete_ttl)
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_NOTIFY_IRONPORT_ON_MESSAGE_RELEASE,
             notify_ironport_on_release)

    def _spam_quarantine_set_appearance(self,
                                        logo=None,
                                        login_page_message=None):
        """
        Defines Spam Quarantine appearance settings.

        This method is used for both
        - enabling Spam Quarantine;
        - modifying previously configured Spam Quarantine.
        """
        if logo is not None:
            if logo.lower() == 'current':
                self._click_radio_button(SPAM_QUARANTINE_LOGO_CURRENT)
            elif logo.lower() == 'ironport':
                self._click_radio_button(SPAM_QUARANTINE_LOGO_IRONPORT)
            else:
                self._click_radio_button(SPAM_QUARANTINE_LOGO_CUSTOM)
                self._input_text_if_not_none(SPAM_QUARANTINE_LOGO_PATH, logo)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_LOGIN_PAGE_MESSAGE, login_page_message)

    def _spam_quarantine_set_users(self,
                                   local_users=None,
                                   ext_auth_groups=None,
                                   custom_roles=None,
                                   confirm=True):
        """
        Defines administrative local users,external auth groups and custom roles
        for Spam Quarantine settings.

        This method is used for both
        - enabling Spam Quarantine;
        - modifying previously configured Spam Quarantine.
        """
        self._set_local_users_sq(local_users, confirm)
        self._set_ext_groups_sq(ext_auth_groups, confirm)
        self._set_custom_roles_sq(custom_roles, confirm)

    def _spam_quarantine_set_euq(self,
                                 enable_euq=None,
                                 euq_auth_type=None,
                                 use_mailbox_pop=None,
                                 use_mailbox_imap=None,
                                 mailbox_server=None,
                                 mailbox_server_transport=None,
                                 mailbox_server_port=None,
                                 append_domain=None,
                                 test_user=None,
                                 test_password=None,
                                 run_test=False,
                                 hide_message_bodies=None):
        """
        Defines Spam Quarantine EUQ settings.

        This method is used for both
        - enabling Spam Quarantine;
        - modifying previously configured Spam Quarantine.
        """
        test_result = None
        self._select_unselect_checkbox(SPAM_QUARANTINE_EUQ_ENABLE, enable_euq)
        self.select_from_dropdown_list \
            (SPAM_QUARANTINE_EUQ_AUTH_TYPE, euq_auth_type)
        if 'mailbox' in \
                self._get_selected_label(SPAM_QUARANTINE_EUQ_AUTH_TYPE).lower():
            if use_mailbox_pop is not None:
                if use_mailbox_pop:
                    self._click_radio_button(SPAM_QUARANTINE_EUQ_MAILBOX('pop3'))
            if use_mailbox_imap is not None:
                if use_mailbox_imap:
                    self._click_radio_button(SPAM_QUARANTINE_EUQ_MAILBOX('imap'))
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_EUQ_MAILBOX_SERVER, mailbox_server)
            self.select_from_dropdown_list \
                (SPAM_QUARANTINE_EUQ_MAILBOX_CONNECTION, mailbox_server_transport)
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_EUQ_MAILBOX_SERVER_PORT, mailbox_server_port)
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_EUQ_MAILBOX_APPEND_DOMAIN, append_domain)
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_EUQ_MAILBOX_TEST_USER, test_user)
            self._input_text_if_not_none \
                (SPAM_QUARANTINE_EUQ_MAILBOX_TEST_PASSWORD, test_password)
            if run_test:
                self.click_button(SPAM_QUARANTINE_EUQ_MAILBOX_TEST_BUTTON)
                test_result = self._get_result()
                self._info(test_result)
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_EUQ_HIDE_MESSAGE_BODIES, hide_message_bodies)
        return test_result

    def _spam_quarantine_set_notification(self,
                                          enable_notification=None,
                                          notification_subject=None,
                                          notification_title=None,
                                          notification_friendly_username=None,
                                          notification_username=None,
                                          notification_domain=None,
                                          notification_to='all users',
                                          notification_to_ldap_group_query=None,
                                          notification_to_ldap_group_name=None,
                                          notification_to_exclude_ldap_query=None,
                                          notification_language=None,
                                          notification_template=None,
                                          notification_auto_login=None,
                                          notification_format=None,
                                          notification_bounce_address=None,
                                          notification_consolidate=None,
                                          notification_schedule=None,
                                          notification_schedule_day=None,
                                          notification_schedule_weekdays=None,
                                          notification_schedule_hours=None):
        """
        Defines Spam Quarantine Notifications settings.

        This method is used for both
        - enabling Spam Quarantine;
        - modifying previously configured Spam Quarantine.

        For this reason arguments like 'notification_schedule_hours' may not depend on
        'notification_schedule'. For example, when user modifies Spam Quarantine and
        does not provide 'notification_schedule' option in function call(defaults to None) but it
        is selected in WUI and equals is 'daily'- we should allow configuring other options
        like 'notification_schedule_hours' by getting real state of 'notification_schedule'.
        """
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_NOTIFICATION_ENABLE, enable_notification)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_FRIENDLY_USERNAME, notification_friendly_username)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_FROM_USERNAME, notification_username)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_FROM_DOMAIN, notification_domain)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_SUBJECT, notification_subject)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_TITLE, notification_title)
        self.select_from_dropdown_list \
            (SPAM_QUARANTINE_NOTIFICATION_LANGUAGE, notification_language)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_TEMPLATE, notification_template)
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_NOTIFICATION_AUTO_LOGIN, notification_auto_login)
        self.select_from_dropdown_list \
            (SPAM_QUARANTINE_NOTIFICATION_FORMAT, notification_format)
        self._input_text_if_not_none \
            (SPAM_QUARANTINE_NOTIFICATION_BOUNCE_ADDR, notification_bounce_address)
        self._select_unselect_checkbox \
            (SPAM_QUARANTINE_NOTIFICATION_CONSOLIDATE, notification_consolidate)

        _notify_to = None
        notify_to_opts = ('all users', 'ldap users')
        if notification_to is not None:
            _notify_to = notification_to.lower()
            if _notify_to not in notify_to_opts:
                raise ValueError \
                    ('Incorrect spam notification to parameter: %s.\
                 Should be one from: %s' % \
                     (notification_to, ','.join(notify_to_opts)))
            if _notify_to == 'all users':
                self._click_radio_button \
                    (SPAM_QUARANTINE_NOTIFICATION_TO_ALL_USERS)
            if _notify_to == 'ldap users':
                self._click_radio_button \
                    (SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USERS)
                if notification_to_ldap_group_query is not None:
                    self.select_from_dropdown_list \
                        (SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_GROUP_QUERY, \
                         notification_to_ldap_group_query)
                    self._input_text_if_not_none \
                        (SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_GROUP_NAME, \
                         notification_to_ldap_group_name)
                    self.click_button \
                        (SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USER_ADD_BTN, "don't wait")
                    if notification_to_exclude_ldap_query:
                        self._select_unselect_checkbox \
                            (SPAM_QUARANTINE_NOTIFICATION_TO_EXCLUDE_LDAP_USERS, True)
                else:
                    raise ValueError \
                        ('LDAP Group Query parameter' + \
                         '[notification_to_ldap_group_query] can not be None')

        _scheduler = None
        scheduler_opts = ('monthly', 'daily', 'weekly')
        if notification_schedule is not None:
            _scheduler = notification_schedule.lower()
            if _scheduler not in scheduler_opts:
                raise ValueError \
                    ('Incorrect spam notification schedule parameter: %s.\
             Should be one from: %s' % \
                     (notification_schedule, ','.join(scheduler_opts)))
        if _scheduler == 'monthly':
            self._click_radio_button \
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_MONTHLY)
        if _scheduler == 'weekly':
            self._click_radio_button \
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_WEEKLY)
        if self._is_checked(SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_WEEKLY):
            self.select_from_dropdown_list \
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAY, notification_schedule_day)
        if _scheduler == 'daily':
            self._click_radio_button(SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY)
            self._set_daily_notification_schedule \
                (notification_schedule_weekdays, notification_schedule_hours)

    def _convert_str_to_list(self, value, separator=","):
        if isinstance(value, basestring):
            value = map(lambda x: x.strip(), value.split(separator))
        return value

    def _set_daily_notification_schedule(self,
                                         notification_schedule_weekdays,
                                         notification_schedule_hours):

        notification_schedule_weekdays = self._convert_str_to_list(
            notification_schedule_weekdays)
        notification_schedule_hours = self._convert_str_to_list(
            notification_schedule_hours)
        notification_schedule_weekdays = \
            [day.lower() for day in notification_schedule_weekdays]
        days = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                 '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17', '18', '19', '20', '21', '22', '23')

        # Clear previous schedule
        for day in days:
            self._unselect_checkbox \
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS(day))
        for hour in hours:
            self._unselect_checkbox \
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR(hour))

        # Set new for days
        for day in notification_schedule_weekdays:
            if day in days:
                self._select_checkbox \
                    (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS(day))
            else:
                raise ValueError \
                    ('Incorrect day parameter: %s. Should be one from: %s ' % \
                     (day, ','.join(days)))

        # For hours
        if notification_schedule_hours is not None:
            for hour in notification_schedule_hours:
                if hour in hours:
                    self._select_checkbox \
                        (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR(hour))
                else:
                    raise ValueError \
                        ('Incorrect hour parameter: %s. Should be one from: %s ' % \
                         (hour, ','.join(hours)))

    def _edit_spam_quarantine(self,
                              delete_oldest=None,
                              scheduled_delete=None,
                              scheduled_delete_ttl=None,
                              notify_ironport_on_release=None,
                              logo=None,
                              login_page_message=None,
                              enable_euq=None,
                              euq_auth_type=None,
                              use_mailbox_pop=None,
                              use_mailbox_imap=None,
                              mailbox_server=None,
                              mailbox_server_transport=None,
                              mailbox_server_port=None,
                              append_domain=None,
                              test_user=None,
                              test_password=None,
                              run_test=False,
                              hide_message_bodies=None,
                              enable_notification=None,
                              notification_subject=None,
                              notification_title=None,
                              notification_friendly_username=None,
                              notification_username=None,
                              notification_domain=None,
                              notification_to=None,
                              notification_to_ldap_group_query=None,
                              notification_to_ldap_group_name=None,
                              notification_to_exclude_ldap_query=None,
                              notification_language=None,
                              notification_template=None,
                              notification_auto_login=None,
                              notification_format=None,
                              notification_bounce_address=None,
                              notification_consolidate=None,
                              notification_schedule=None,
                              notification_schedule_day=None,
                              notification_schedule_weekdays=None,
                              notification_schedule_hours=None,
                              local_users=None,
                              ext_auth_groups=None,
                              custom_roles=None,
                              confirm=True):
        self._spam_quarantine_set_main_settings(
            delete_oldest=delete_oldest,
            scheduled_delete=scheduled_delete,
            scheduled_delete_ttl=scheduled_delete_ttl,
            notify_ironport_on_release=notify_ironport_on_release)
        self._spam_quarantine_set_appearance(logo=logo,
                                             login_page_message=login_page_message)
        self._spam_quarantine_set_users(local_users=local_users,
                                        ext_auth_groups=ext_auth_groups,
                                        custom_roles=custom_roles,
                                        confirm=confirm)
        self._spam_quarantine_set_euq(enable_euq=enable_euq,
                                      euq_auth_type=euq_auth_type,
                                      use_mailbox_pop=use_mailbox_pop,
                                      use_mailbox_imap=use_mailbox_imap,
                                      mailbox_server=mailbox_server,
                                      mailbox_server_transport=mailbox_server_transport,
                                      mailbox_server_port=mailbox_server_port,
                                      append_domain=append_domain,
                                      test_user=test_user,
                                      test_password=test_password,
                                      run_test=run_test,
                                      hide_message_bodies=hide_message_bodies)
        self._spam_quarantine_set_notification(enable_notification=enable_notification,
                                               notification_subject=notification_subject,
                                               notification_title=notification_title,
                                               notification_friendly_username=notification_friendly_username,
                                               notification_username=notification_username,
                                               notification_domain=notification_domain,
                                               notification_to=notification_to,
                                               notification_to_ldap_group_query=notification_to_ldap_group_query,
                                               notification_to_ldap_group_name=notification_to_ldap_group_name,
                                               notification_to_exclude_ldap_query=notification_to_exclude_ldap_query,
                                               notification_language=notification_language,
                                               notification_template=notification_template,
                                               notification_auto_login=notification_auto_login,
                                               notification_format=notification_format,
                                               notification_bounce_address=notification_bounce_address,
                                               notification_consolidate=notification_consolidate,
                                               notification_schedule=notification_schedule,
                                               notification_schedule_day=notification_schedule_day,
                                               notification_schedule_weekdays=notification_schedule_weekdays,
                                               notification_schedule_hours=notification_schedule_hours)
        self._click_submit_button()

    def quarantines_spam_edit(self,
                              delete_oldest=None,
                              scheduled_delete=None,
                              scheduled_delete_ttl=None,
                              notify_ironport_on_release=None,
                              logo=None,
                              login_page_message=None,
                              enable_euq=None,
                              euq_auth_type=None,
                              use_mailbox_pop=None,
                              use_mailbox_imap=None,
                              mailbox_server=None,
                              mailbox_server_transport=None,
                              mailbox_server_port=None,
                              append_domain=None,
                              test_user=None,
                              test_password=None,
                              run_test=False,
                              hide_message_bodies=None,
                              enable_notification=None,
                              notification_subject=None,
                              notification_title=None,
                              notification_friendly_username=None,
                              notification_username=None,
                              notification_domain=None,
                              notification_to=None,
                              notification_to_ldap_group_query=None,
                              notification_to_ldap_group_name=None,
                              notification_to_exclude_ldap_query=False,
                              notification_language=None,
                              notification_template=None,
                              notification_auto_login=None,
                              notification_format=None,
                              notification_bounce_address=None,
                              notification_consolidate=None,
                              notification_schedule=None,
                              notification_schedule_day=None,
                              notification_schedule_weekdays=None,
                              notification_schedule_hours=None,
                              local_users=None,
                              ext_auth_groups=None,
                              custom_roles=None,
                              confirm=True):
        """
        Edit Spam Quarantine settings.

        *Parameters*:
        - `delete_oldest`: When storage space is full, automatically delete oldest messages first. Boolean.
        - `scheduled_delete`: Scheduled delete or not. Boolean.
        - `scheduled_delete_ttl`: Days to delete after if `scheduled_delete` is True.
        - `notify_ironport_on_release`: Send a copy of released messages to IronPort for analysis. Boolean.
        - `logo`: Quarantine log. Options:
        | ironport| Use IronPort logo |
        | custom  | Use custom logo (path to file on local machine) |
        | current | Use current logo. |
        - `login_page_message`: Login Page Message.
        - `enable_euq`: Enable End User Quarantine. Boolean.
        - `euq_auth_type`: End User Quarantine authentication type.
        Case insensitive, regex=begins with. Eg: _mailbox_, _Ldap_ are correct.
        Options:
        | None |
        | Mailbox (IMAP/POP) |
        | LDAP |
        - `use_mailbox_pop`: Use POP3 protocol if `euq_auth_type` is _Mailbox_.
        - `use_mailbox_imap`: Use IMAP protocol if `euq_auth_type` is _Mailbox_.
        - `mailbox_server`: Mailbox server if `euq_auth_type` is _Mailbox_.
        - `mailbox_server_transport`:  Connection to use if `euq_auth_type` is _Mailbox_. Case insensitive.
        Options are:
        | None |
        | SSL |
        - `mailbox_server_port`: Mailbox server port if `euq_auth_type` is _Mailbox_.
        - `append_domain`: Append Domain to Unqualified Usernames. String.
        - `test_user`: Test user if `euq_auth_type` is _Mailbox_. String
        - `test_password`: Test password if `euq_auth_type` is _Mailbox_. String.
        - `run_test`: Run test. Boolean. Gets result and prints at _INFO_ level, but does not return it.
        Use `Spam Quarantine Edit Euq` keyword to test authentication.
        - `hide_message_bodies`: Do not display message bodies to end-users until message is released. Boolean.
        - `enable_notification`: Enable Spam Notification. Boolean.
        - `notification_subject`: Notification subject.
        - `notification_title`:  Notification title.
        - `notification_friendly_username`:  Notificatiozon friendly username.
        - `notification_username`:  Notification username.
        - `notification_domain`:  Notification domain.
        - `notification_to`: Notification recipients.
        Options are:
        | All Users |
        | LDAP Users |
        - `notification_to_ldap_group_query: LDAP Group query configured on DUT.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_ldap_group_name`: LDAP Group name configured on the LDAP server.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_exclude_ldap_query`: Whether to exlcude LDAP users. Yes or  No.
        (Applicable only if notification_to set to "LDAP Users")
        Options are:
        | True | False |
        - `notification_language`:  Notification language. Options as they are seen in WUI.
        Case insensitive, uses regex=begins with.
        Values like _English_, _deutsch_ are correct.
        - `notification_template`: Message Body.
        - `notification_auto_login` : Enable autologin without credentials. Boolean
        - `notification_format`:Message format. Case insesitive. Options:
        | HTML (recommended) |
        | Text |
        | HTML/Text |
        - `notification_bounce_address`: Deliver Bounce Message to address.
        - `notification_consolidate`: Consolidate notifications sent to the same LDAP user at different addresses. Boolean.
        - `notification_schedule`: Notification Schedule. One from: _monthly_, _weekly_, _daily_. Case insensitive.
        - `notification_schedule_day`: Day of a week if `notification_schedule` is _weekly_.
        - `notification_schedule_weekdays`:Select weekday. Correct values are Mon, Tue, Wed, Thu, Fri, Sat, Sun. List or CSV
        - `notification_schedule_hours`: Hours. Correct values are: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10,... 23.
        List or CSV
        - `local_users`: Local administrative users. String of comma separated values.
        ${EMPTY} to clear settings.
        - `ext_auth_groups`: External administrative groups. String of comma separated values.
        ${EMPTY} to clear settings.
        Options are:
        | operators |
        | readonly |
        | guest |
        | helpdesk |
        - `custom_roles`: Custom administrative roles . String of comma separated values.
        ${EMPTY} to clear settings.
        - `confirm`: Confirm applies to users/groups/roles settings dialog. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | Quarantines Spam Edit |
        | ... | delete_oldest=${True} |
        | ... | scheduled_delete=${False} |
        | ... | notify_ironport_on_release=${False} |
        | ... | logo=current |
        | ... | login_page_message=Hello!!! Welcome to ${DUT}'s Super Spam Quarantine |
        | ... | enable_euq=${True} |
        | ... | euq_auth_type=ldap |
        | ... | hide_message_bodies=${False} |
        | ... | enable_notification=${True} |
        | ... | notification_subject=SARF Test Spam Quarantine Notification From ${DUT} |
        | ... | notification_title=SARF Test Spam Quarantine Notification |
        | ... | notification_username=sarf |
        | ... | notification_domain=${DUT} |
        | ... | notification_to=LDAP Users |
        | ... | notification_to_ldap_group_query=OpenLDAP.group |
        | ... | notification_to_ldap_group_name=TestGroup |
        | ... | notification_language=English |
        | ... | notification_template=${message} |
        | ... | notification_auto_login=${True} |
        | ... | notification_format=html |
        | ... | notification_bounce_address=testuser@${DUT} |
        | ... | notification_schedule=weekly |
        | ... | notification_schedule_day=monday |
        | ... | local_users=${EMPTY} |
        | ... | ext_auth_groups=helpdesk |
        """
        self._info('Edit quarantine: %s' % self.sq)
        self._edit_spam_page()
        self._edit_spam_quarantine(
            delete_oldest=delete_oldest,
            scheduled_delete=scheduled_delete,
            scheduled_delete_ttl=scheduled_delete_ttl,
            notify_ironport_on_release=notify_ironport_on_release,
            logo=logo,
            login_page_message=login_page_message,
            enable_euq=enable_euq,
            euq_auth_type=euq_auth_type,
            use_mailbox_pop=use_mailbox_pop,
            use_mailbox_imap=use_mailbox_imap,
            mailbox_server=mailbox_server,
            mailbox_server_transport=mailbox_server_transport,
            mailbox_server_port=mailbox_server_port,
            append_domain=append_domain,
            test_user=test_user,
            test_password=test_password,
            run_test=run_test,
            hide_message_bodies=hide_message_bodies,
            enable_notification=enable_notification,
            notification_subject=notification_subject,
            notification_title=notification_title,
            notification_friendly_username=notification_friendly_username,
            notification_username=notification_username,
            notification_domain=notification_domain,
            notification_to=notification_to,
            notification_to_ldap_group_query=notification_to_ldap_group_query,
            notification_to_ldap_group_name=notification_to_ldap_group_name,
            notification_to_exclude_ldap_query=notification_to_exclude_ldap_query,
            notification_language=notification_language,
            notification_template=notification_template,
            notification_auto_login=notification_auto_login,
            notification_format=notification_format,
            notification_bounce_address=notification_bounce_address,
            notification_consolidate=notification_consolidate,
            notification_schedule=notification_schedule,
            notification_schedule_day=notification_schedule_day,
            notification_schedule_weekdays=notification_schedule_weekdays,
            notification_schedule_hours=notification_schedule_hours,
            local_users=local_users,
            ext_auth_groups=ext_auth_groups,
            custom_roles=custom_roles,
            confirm=confirm)

    def quarantines_spam_enable(self,
                                delete_oldest=None,
                                scheduled_delete=None,
                                scheduled_delete_ttl=None,
                                notify_ironport_on_release=None,
                                logo=None,
                                login_page_message=None,
                                enable_euq=None,
                                euq_auth_type=None,
                                use_mailbox_pop=None,
                                use_mailbox_imap=None,
                                mailbox_server=None,
                                mailbox_server_transport=None,
                                mailbox_server_port=None,
                                append_domain=None,
                                test_user=None,
                                test_password=None,
                                run_test=False,
                                hide_message_bodies=None,
                                enable_notification=None,
                                notification_subject=None,
                                notification_title=None,
                                notification_friendly_username=None,
                                notification_username=None,
                                notification_domain=None,
                                notification_to=None,
                                notification_to_ldap_group_query=None,
                                notification_to_ldap_group_name=None,
                                notification_to_exclude_ldap_query=False,
                                notification_language=None,
                                notification_template=None,
                                notification_auto_login=None,
                                notification_format=None,
                                notification_bounce_address=None,
                                notification_consolidate=None,
                                notification_schedule=None,
                                notification_schedule_day=None,
                                notification_schedule_weekdays=None,
                                notification_schedule_hours=None,
                                local_users=None,
                                ext_auth_groups=None,
                                custom_roles=None,
                                confirm=True):
        """
        Enable and configure Spam Quarantine settings.

        *Parameters*:
        - `delete_oldest`: When storage space is full, automatically delete oldest messages first. Boolean.
        - `scheduled_delete`: Scheduled delete or not. Boolean.
        - `scheduled_delete_ttl`: Days to delete after if `scheduled_delete` is True.
        - `notify_ironport_on_release`: Send a copy of released messages to IronPort for analysis. Boolean.
        - `logo`: Quarantine log. Options:
        | ironport| Use IronPort logo |
        | custom  | Use custom logo (path to file on local machine) |
        | current | Use current logo. |
        - `login_page_message`: Login Page Message.
        - `enable_euq`: Enable End User Quarantine. Boolean.
        - `euq_auth_type`: End User Quarantine authentication type. Case insensitive, regex=begins with.
        Eg: _mailbox_, _Ldap_ are correct.
        Options:
        | None |
        | Mailbox (IMAP/POP) |
        | LDAP |
        - `use_mailbox_pop`: Use POP3 protocol if `euq_auth_type` is _Mailbox_.
        - `use_mailbox_imap`: Use IMAP protocol if `euq_auth_type` is _Mailbox_.
        - `mailbox_server`: Mailbox server if `euq_auth_type` is _Mailbox_.
        - `mailbox_server_transport`:  Connection to use if `euq_auth_type` is _Mailbox_.
        Case insensitive. Options are:
        | None |
        | SSL |
        - `mailbox_server_port`: Mailbox server port if `euq_auth_type` is _Mailbox_.
        - `append_domain`: Append Domain to Unqualified Usernames. String.
        - `test_user`: Test user if `euq_auth_type` is _Mailbox_. String
        - `test_password`: Test password if `euq_auth_type` is _Mailbox_. String.
        - `run_test`: Run test. Boolean. Gets result and prints at _INFO_ level, but does not return it.
        Use `Spam Quarantine Edit Euq` keyword to test authentication.
        - `hide_message_bodies`: Do not display message bodies to end-users until message is released. Boolean.
        - `enable_notification`: Enable Spam Notification. Boolean.
        - `notification_subject`: Notification subject.
        - `notification_title`:  Notification title.
        - `notification_friendly_username`:  Notification friendly username.
        - `notification_username`:  Notification username.
        - `notification_to`: Notification recipients.
        Options are:
        | All Users |
        | LDAP Users |
        - `notification_to_ldap_group_query: LDAP Group query configured on DUT.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_ldap_group_name`: LDAP Group name configured on the LDAP server.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_exclude_ldap_query`: Whether to exlcude LDAP users.
        (Applicable only if notification_to set to "LDAP Users")
        Options are:
        | True | False |
        - `notification_language`:  Notification language. Options as they are seen in WUI.
        - `notification_domain`:  Notification domain.
        - `notification_language`:  Notification language. Options as they are seen in WUI.
        Case insensitive, uses regex=begins with.
        Values like _English_, _deutsch_ are correct.
        - `notification_template`: Message Body.
        - `notification_auto_login` : Enable autologin without credentials. Boolean
        - `notification_format`:Message format. Case insensitive. Options:
        | HTML (recommended) |
        | Text |
        | HTML/Text |
        - `notification_bounce_address`: Deliver Bounce Message to address.
        - `notification_consolidate`: Consolidate notifications sent to the same LDAP user at different addresses. Boolean.
        - `notification_schedule`: Notification Schedule.
        One from: _monthly_, _weekly_, _daily_. Case insensitive.
        - `notification_schedule_day`: Day of a week if `notification_schedule` is _weekly_.
        - `notification_schedule_weekdays`:Select weekday. Correct values are Mon, Tue, Wed, Thu, Fri, Sat, Sun. List or CSV.
        - `notification_schedule_hours`: Hours. Correct values are: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10,... 23.
        List or CSV.
        - `local_users`: Local administrative users.
        String of comma separated values. ${EMPTY} to clear settings.
        - `ext_auth_groups`: External administrative groups.
        String of comma separated values. ${EMPTY} to clear settings.
        Options are:
        | operators |
        | readonly |
        | guest |
        | helpdesk |
        - `custom_roles`: Custom administrative roles .
        String of comma separated values. ${EMPTY} to clear settings.
        - `confirm`: Confirm applies to users/groups/roles settings dialog. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsAlreadyEnabled`: If quarantine is already enabled (no Enable link).

        *Examples*:
        | ${message}=  Catenate |
        | ... | SEPARATOR=\n |
        | ... | This is SARF test - enable Spam Quarantine. |
        | ... | There are %new_message_count% new messages in your Email Quarantine. |
        | ... | Messages will be automatically removed from the quarantine after %days_until_expire% day(s). |
        | ... | To see all quarantined messages view %quarantine_url%. |
        | Quarantines Spam Enable |
        | ... | delete_oldest=${False} |
        | ... | scheduled_delete=${True} |
        | ... | scheduled_delete_ttl=20 |
        | ... | notify_ironport_on_release=${True} |
        | ... | logo=ironport |
        | ... | login_page_message=Welcome to ${DUT}'s Spam Quarantine |
        | ... | enable_euq=${True} |
        | ... | euq_auth_type=mailbox |
        | ... | use_mailbox_pop={True} |
        | ... | mailbox_server=mail.${NETWORK} |
        | ... | mailbox_server_transport=ssl |
        | ... | mailbox_server_port=999 |
        | ... | append_domain=mail.${NETWORK} |
        | ... | test_user=testuser |
        | ... | test_password=ironport |
        | ... | run_test=${True} |
        | ... | hide_message_bodies=${True} |
        | ... | enable_notification=${True} |
        | ... | notification_subject=Spam Quarantine Notification From ${DUT} |
        | ... | notification_title=Spam Quarantine Notification |
        | ... | notification_friendly_username=Super Mailer |
        | ... | notification_username=antispammer |
        | ... | notification_domain=${DUT} |
        | ... | notification_to=LDAP Users |
        | ... | notification_to_ldap_group_query=OpenLDAP.group |
        | ... | notification_to_ldap_group_name=ea_upq_admin |
        | ... | notification_to_exclude_ldap_query=${True} |
        | ... | notification_language=Deutsch |
        | ... | notification_template=${message} |
        | ... | notification_auto_login=${True} |
        | ... | notification_format=text |
        | ... | notification_bounce_address=testuser@${DUT} |
        | ... | notification_schedule=daily |
        | ... | notification_schedule_weekdays=Mon, Tue, Wed  |
        | ... | notification_schedule_hours=00, 03, 06, 12, 21 |
        | ... | local_users=read1, oper1, guest1 |
        | ... | ext_auth_groups=readonly, guest, operators |
        | ... | custom_roles=role1, role2 |
        """
        self._info('Enable quarantine: %s' % self.sq)
        self._open_spam_page()
        self._enable_spam_quarantine()
        self._edit_spam_quarantine(
            delete_oldest=delete_oldest,
            scheduled_delete=scheduled_delete,
            scheduled_delete_ttl=scheduled_delete_ttl,
            notify_ironport_on_release=notify_ironport_on_release,
            logo=logo,
            login_page_message=login_page_message,
            enable_euq=enable_euq,
            euq_auth_type=euq_auth_type,
            use_mailbox_pop=use_mailbox_pop,
            use_mailbox_imap=use_mailbox_imap,
            mailbox_server=mailbox_server,
            mailbox_server_transport=mailbox_server_transport,
            mailbox_server_port=mailbox_server_port,
            append_domain=append_domain,
            test_user=test_user,
            test_password=test_password,
            run_test=run_test,
            hide_message_bodies=hide_message_bodies,
            enable_notification=enable_notification,
            notification_subject=notification_subject,
            notification_title=notification_title,
            notification_friendly_username=notification_friendly_username,
            notification_username=notification_username,
            notification_domain=notification_domain,
            notification_to=notification_to,
            notification_to_ldap_group_query=notification_to_ldap_group_query,
            notification_to_ldap_group_name=notification_to_ldap_group_name,
            notification_to_exclude_ldap_query=notification_to_exclude_ldap_query,
            notification_language=notification_language,
            notification_template=notification_template,
            notification_auto_login=notification_auto_login,
            notification_format=notification_format,
            notification_bounce_address=notification_bounce_address,
            notification_consolidate=notification_consolidate,
            notification_schedule=notification_schedule,
            notification_schedule_day=notification_schedule_day,
            notification_schedule_weekdays=notification_schedule_weekdays,
            notification_schedule_hours=notification_schedule_hours,
            local_users=local_users,
            ext_auth_groups=ext_auth_groups,
            custom_roles=custom_roles,
            confirm=confirm)

    def quarantines_spam_edit_main_settings(self,
                                            open_edit_page=True,
                                            delete_oldest=None,
                                            scheduled_delete=None,
                                            scheduled_delete_ttl=None,
                                            notify_ironport_on_release=None,
                                            submit=True):
        """
        Edit Spam Quarantine settings - configure main settings.
        The same can be done with `Spam Quarantine Edit` keyword.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `delete_oldest`: When storage space is full, automatically delete oldest messages first. Boolean.
        - `scheduled_delete`: Scheduled delete or not. Boolean.
        - `scheduled_delete_ttl`: Days to delete after if `scheduled_delete` is True.
        - `notify_ironport_on_release`: Send a copy of released messages to IronPort for analysis. Boolean.
        - `submit`: Submit changes. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no Edit link).

        *Examples*:
        | Quarantines Spam Edit Main Settings |
        | ... | scheduled_delete_ttl=5 |
        | ... | submit=${False} |
        """
        if open_edit_page:
            self._edit_spam_page()
        self._spam_quarantine_set_main_settings(
            delete_oldest=delete_oldest,
            scheduled_delete=scheduled_delete,
            scheduled_delete_ttl=scheduled_delete_ttl,
            notify_ironport_on_release=notify_ironport_on_release)
        self._handle_submit(submit)

    def quarantines_spam_edit_appearance(self,
                                         open_edit_page=True,
                                         logo=None,
                                         login_page_message=None,
                                         submit=True):
        """
        Edit Spam Quarantine settings - configure appearance.
        The same can be done with `Spam Quarantine Edit` keyword.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `login_page_message`: Login Page Message.
        - `submit`: Submit changes. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | Quarantines Spam Edit Appearance |
        | ... | open_edit_page=${True} |
        | ... | logo=ironport |
        | ... | login_page_message=Welcome to ${DUT}'s Spam Quarantine |
        | ... | submit=${True} |

        | Quarantines Spam Edit Appearance |
        | ... | open_edit_page=${False} |
        | ... | logo=/home/petro/Pictures/superlogo.gif |
        | ... | submit=${False} |
        """
        if open_edit_page:
            self._edit_spam_page()
        self._spam_quarantine_set_appearance(logo=logo,
                                             login_page_message=login_page_message)
        self._handle_submit(submit)

    def quarantines_spam_edit_euq(self,
                                  open_edit_page=True,
                                  enable_euq=None,
                                  euq_auth_type=None,
                                  use_mailbox_pop=None,
                                  use_mailbox_imap=None,
                                  mailbox_server=None,
                                  mailbox_server_transport=None,
                                  mailbox_server_port=None,
                                  append_domain=None,
                                  test_user=None,
                                  test_password=None,
                                  run_test=False,
                                  hide_message_bodies=None,
                                  submit=True):
        """
        Edit Spam Quarantine settings - configure EUQ.
        The same can be done with `Spam Quarantine Edit` keyword.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `enable_euq`: Enable End User Quarantine. Boolean.
        - `euq_auth_type`: End User Quarantine authentication type.
        Case insensitive, regex=begins with. Eg: _mailbox_, _Ldap_ are correct.
        Options:
        | None |
        | Mailbox (IMAP/POP) |
        | LDAP |
        - `use_mailbox_pop`: Use POP3 protocol if `euq_auth_type` is _Mailbox_.
        - `use_mailbox_imap`: Use IMAP protocol if `euq_auth_type` is _Mailbox_.
        - `mailbox_server`: Mailbox server if `euq_auth_type` is _Mailbox_.
        - `mailbox_server_transport`:  Connection to use if `euq_auth_type` is _Mailbox_. Case insensitive.
        Options are:
        | None |
        | SSL |
        - `mailbox_server_port`: Mailbox server port if `euq_auth_type` is _Mailbox_.
        - `append_domain`: Append Domain to Unqualified Usernames. String.
        - `test_user`: Test user if `euq_auth_type` is _Mailbox_. String
        - `test_password`: Test password if `euq_auth_type` is _Mailbox_. String.
        - `run_test`: Run test. Boolean.
        - `hide_message_bodies`: Do not display message bodies to end-users until message is released. Boolean.
        - `submit`: Submit changes. Boolean.

        *Return*:
        Authentication result(if test was done). String.

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | ${auth_res}= | Quarantines Spam Edit Euq |
        | ... | open_edit_page=${False} |
        | ... | enable_euq=${True} |
        | ... | euq_auth_type=mailbox |
        | ... | use_mailbox_pop={True} |
        | ... | mailbox_server=mail.${NETWORK} |
        | ... | mailbox_server_transport=ssl |
        | ... | mailbox_server_port=999 |
        | ... | append_domain=mail.${NETWORK} |
        | ... | test_user=testuser |
        | ... | test_password=ironport |
        | ... | run_test=${True} |
        | Log | ${auth_res} |
        """
        if open_edit_page:
            self._edit_spam_page()
        auth_test_result = self._spam_quarantine_set_euq(enable_euq=enable_euq,
                                                         euq_auth_type=euq_auth_type,
                                                         use_mailbox_pop=use_mailbox_pop,
                                                         use_mailbox_imap=use_mailbox_imap,
                                                         mailbox_server=mailbox_server,
                                                         mailbox_server_transport=mailbox_server_transport,
                                                         mailbox_server_port=mailbox_server_port,
                                                         append_domain=append_domain,
                                                         test_user=test_user,
                                                         test_password=test_password,
                                                         run_test=run_test,
                                                         hide_message_bodies=hide_message_bodies)
        self._handle_submit(submit)
        return auth_test_result

    def quarantines_spam_edit_notifications(self,
                                            open_edit_page=True,
                                            enable_notification=None,
                                            notification_subject=None,
                                            notification_title=None,
                                            notification_friendly_username=None,
                                            notification_username=None,
                                            notification_domain=None,
                                            notification_to=None,
                                            notification_to_ldap_group_query=None,
                                            notification_to_ldap_group_name=None,
                                            notification_to_exclude_ldap_query=False,
                                            notification_language=None,
                                            notification_template=None,
                                            notification_auto_login=None,
                                            notification_format=None,
                                            notification_bounce_address=None,
                                            notification_consolidate=None,
                                            notification_schedule=None,
                                            notification_schedule_day=None,
                                            notification_schedule_weekdays=None,
                                            notification_schedule_hours=None,
                                            submit=True):
        """
        Edit Spam Quarantine settings configure Spam Notifications.
        The same can be done with `Spam Quarantine Edit` keyword.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `enable_notification`: Enable Spam Notification. Boolean.
        - `notification_subject`: Notification subject.
        - `notification_title`:  Notification title.
        - `notification_friendly_username`:  Notification friendly username.
        - `notification_username`:  Notification username.
        - `notification_domain`:  Notification domain.
        - `notification_to`: Notification recipients.
        Options are:
        | All Users |
        | LDAP Users |
        - `notification_to_ldap_group_query: LDAP Group query configured on DUT.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_ldap_group_name`: LDAP Group name configured on the LDAP server.
        (Applicable only if notification_to set to "LDAP Users")
        - `notification_to_exclude_ldap_query`: Whether to exlcude LDAP users.
        (Applicable only if notification_to set to "LDAP Users")
        Options are:
        | True | False |
        - `notification_language`:  Notification language. Options as they are seen in WUI.
        Case insensitive, uses regex=begins with.
        Values like _English_, _deutsch_ are correct.
        - `notification_template`: Message Body.
        - `notification_auto_login`: Enable autologin without credentials. Boolean
        - `notification_format`:Message format. Case insensitive. Options:
        | HTML (recommended) |
        | Text |
        | HTML/Text |
        - `notification_bounce_address`: Deliver Bounce Message to address.
        - `notification_consolidate`: Consolidate notifications sent to the same LDAP user at different addresses. Boolean.
        - `notification_schedule`: Notification Schedule.
        One from: _monthly_, _weekly_, _daily_. Case insensitive.
        - `notification_schedule_day`: Day of a week if `notification_schedule` is _weekly_.

        - `notification_schedule_day`: Day of a week if `notification_schedule` is _weekly_.
        - `notification_schedule_weekdays`:Select weekday. Correct values are Mon, Tue, Wed, Thu, Fri, Sat, Sun. List or CSV.
        - `notification_schedule_hours`: Hours. Correct values are: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10,... 23.
        List or CSV.
        - `submit`: Submit changes. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | Quarantines Spam Edit Notifications |
        | ... | enable_notification=${True} |
        | ... | notification_subject= From ${DUT} |
        | ... | notification_title=SQ Notification |
        | ... | notification_friendly_username=Mario |
        | ... | notification_username=supermario |
        | ... | notification_domain=${DUT} |
        | ... | notification_to=All Users |
        | ... | notification_language=English |
        | ... | notification_template=Some text goes here |
        | ... | notification_auto_login=${True} |
        | ... | notification_format=html/text |
        | ... | notification_bounce_address=mario@${DUT} |
        | ... | notification_schedule=weekly |
        | ... | notification_schedule_day=Wednesday |
        """
        if open_edit_page:
            self._edit_spam_page()
        self._spam_quarantine_set_notification(enable_notification=enable_notification,
                                               notification_subject=notification_subject,
                                               notification_title=notification_title,
                                               notification_friendly_username=notification_friendly_username,
                                               notification_username=notification_username,
                                               notification_domain=notification_domain,
                                               notification_to=notification_to,
                                               notification_to_ldap_group_query=notification_to_ldap_group_query,
                                               notification_to_ldap_group_name=notification_to_ldap_group_name,
                                               notification_to_exclude_ldap_query=notification_to_exclude_ldap_query,
                                               notification_language=notification_language,
                                               notification_template=notification_template,
                                               notification_auto_login=notification_auto_login,
                                               notification_format=notification_format,
                                               notification_bounce_address=notification_bounce_address,
                                               notification_consolidate=notification_consolidate,
                                               notification_schedule=notification_schedule,
                                               notification_schedule_day=notification_schedule_day,
                                               notification_schedule_weekdays=notification_schedule_weekdays,
                                               notification_schedule_hours=notification_schedule_hours)
        self._handle_submit(submit)

    def quarantines_spam_edit_users(self,
                                    open_edit_page=True,
                                    local_users=None,
                                    ext_auth_groups=None,
                                    custom_roles=None,
                                    confirm=True,
                                    submit=True):
        """
        Edit Spam Quarantine settings - configure administrative users.
        The same can be done with `Spam Quarantine Edit` keyword.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `local_users`: Local administrative users.
        String of comma separated values. ${EMPTY} to clear settings.
        - `ext_auth_groups`: External administrative groups.
        String of comma separated values. ${EMPTY} to clear settings.
        Options are:
        | operators |
        | readonly |
        | guest |
        | helpdesk |
        - `custom_roles`: Custom administrative roles .
        String of comma separated values. ${EMPTY} to clear settings.
        - `confirm`: Confirm applies to users/groups/roles settings dialog. Boolean.
        - `submit`: Submit changes. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | Quarantines Spam Edit Users |
        | ... | local_users=read1, oper1 |
        | ... | ext_auth_groups=readonly, guest, operators |
        | ... | custom_roles=role1, role2 |
        | ... | submit=${False} |

        | Quarantines Spam Edit Users |
        | ... | open_edit_page=${False} |
        | ... | local_users=${EMPTY} |
        | ... | ext_auth_groups=readonly |
        | ... | submit=${True} |
        """
        if open_edit_page:
            self._edit_spam_page()
        self._spam_quarantine_set_users(local_users=local_users,
                                        ext_auth_groups=ext_auth_groups,
                                        custom_roles=custom_roles,
                                        confirm=confirm)
        self._handle_submit(submit)

    def quarantines_spam_delete_existing_ldap_group_queries(self,
                                                            open_edit_page=True,
                                                            ldap_queries_to_delete='All',
                                                            submit=True):
        """
        This keyword deletes the already configured ldap group queries
        for Spam Quarantine Notification.

        *Parameters*:
        - `open_edit_page`: Open Edit Spam Quarantine page. Boolean.
        If False - assume we are at the needed page.
        - `ldap_queries_to_delete`: List of LDAP group query names.
        Default value: All
        - `submit`: Submit changes. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `ValueError`: If there is no such LDAP group query configured.

        *Examples*:
        | @{ldap_groups}= | Create List |
        | ...  OpenLDAP.group: ea_upq_admin |
        | Quarantines Spam Delete Existing Ldap Group Queries |
        | ...  ldap_queries_to_delete=@{ldap_groups} |
        | Commit Changes |
        """
        if open_edit_page:
            self._edit_spam_page()
        self.select_from_dropdown_list(SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_GROUP_QUERY, \
                                       'vm09bsd0064.cs2.group')
        if ldap_queries_to_delete == 'All':
            existing_elements = self.get_list_items( \
                SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST)
            self._info("elements : %s" % existing_elements)
            for eachElement in existing_elements:
                self.select_from_list( \
                    SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST, \
                    'label=%s' % eachElement)
                # self.select_all_from_list(\
                # SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST)
                self.click_button( \
                    SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USER_DEL_BTN)
        else:
            self._info("LDAP Group Queries to delete: %s" \
                       % ldap_queries_to_delete)
            for ldap_query_to_delete in ldap_queries_to_delete:
                existing_query = self.get_list_items( \
                    SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST)
                self._info("Existing LDAP Grpoup queries: %s" % existing_query)
                self._info("Selecting requested query from list: %s" \
                           % ldap_query_to_delete)
                dest_entry = filter(lambda x: x.find(ldap_query_to_delete) >= 0,
                                    existing_query)
                if dest_entry:
                    self._info("Deleting LDAP group query: %s" % dest_entry)
                    self.select_from_list( \
                        SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST, dest_entry[0])
                else:
                    raise ValueError('There is no "%s" user available for removal. ' \
                                     'Available entries are:\n%s'(user_to_delete, existing_users))
                self.click_button( \
                    SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USER_DEL_BTN, "don't wait")
        self._handle_submit(submit)

    def quarantines_spam_disable(self, confirm=True):
        """
        Disable Spam Quarantine.

        *Parameters*:
        - `confirm`: Confirm disable. Boolean.

        *Return*:
        None

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).

        *Examples*:
        | Quarantines Spam Disable |
        """
        self._info('Disable quarantine: %s' % self.sq)
        self._disable_spam_quarantine()
        # the line below does not work due to incorrect locator in guicommon.py
        # self._click_submit_button(wait=False, accept_confirm_dialog=True)
        #
        # maybe there is no need to keep so strict locator in guicommon.py
        # and use
        # //[@id="confirmation_dialog"]//button[text()="Continue"]
        # instead of
        # //div[@id="confirmation_dialog"]/div/span/button[text()="Continue"]
        # here the dialog's buttons are not inside div section.
        #
        self.click_button(COMMON_SUBMIT_BUTTON, "don't wait")
        self._click_submit_button_custom('Continue', 'Cancel', confirm=confirm)

    def quarantines_spam_get_settings(self):
        """
        Not Implemented. Should parse page...
        """
        self._not_impl(self.spam_quarantines_get_settings)
        self._info('Get quarantine settings: %s' % self.sq)
        self._open_spam_page()

    def quarantines_spam_is_active(self):
        """
        Check if Spam Quarantine is active.
        It is active if it is click-able.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.

        *Examples*:
        | ${res} | Quarantines Spam Is Active |
        | Should Be True | ${res} |
        """
        self._info('Check if quarantine is active: %s' % self.sq)
        self._open_spam_page()
        return self._is_active(self.sq)

    def quarantines_spam_is_enabled(self):
        """
        Check if Spam Quarantine is enabled.
        It is enabled if corresponding row has Edit link.
        In WUI it may be marked as disabled because of
        corresponding feature inactive/not-configured(like SQ ports of CASE engine).

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.

        *Examples*:
        | ${res} | Quarantines Spam Is Enabled |
        | Should Not Be True | ${res} |
        """
        self._info('Check if quarantine is enabled: %s' % self.sq)
        self._open_spam_page()
        row_idx, col_idx = self._is_quarantine_present(self.sq)
        return self._is_enabled(row_idx)
