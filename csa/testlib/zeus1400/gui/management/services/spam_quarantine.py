#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/services/spam_quarantine.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import time
import re
from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions
from common.gui.guiexceptions import GuiValueError

EDIT_BUTTON_LOC = "xpath=//form[@name='form_euq']//input[@type='button' and @name='slbl_enable']"
ENABLE_BUTTON_LOC = "xpath=//form[@name='form_euq']//input[@type='button' and @name='slbl_enable' and contains(@value, 'Enable')]"
SYNC_ALL_APPLIANCES_BUTTON_LOC = "//*[@type='button' and @value='Synchronize All Appliances']"

ENABLE_CHECKBOX_LOC = "//input[@type='checkbox' and @name='enabled']"
INTERFACE_LOC = "interface"
PORT_LOC = "server_port"
PRIMARY_SERVER_LOC = "release_host"
PRIMARY_PORT_LOC = "release_port"
ALTERNATIVE_SERVER_LOC = "alt_release_host"
ALTERNATIVE_PORT_LOC = "alt_release_port"
DELETE_AFTER_RB1_LOC = "disable_time_expire_0"
DELETE_AFTER_RB2_LOC = "disable_time_expire_1"
DELETE_AFTER_DAYS_LOC = "message_ttl"
SEND_COPY_LOC = "to_corpus"
LOGO_RB_CURRENT_LOC = "current_logo_id"
LOGO_RB_DEFAULT_LOC = "default_logo_id"
LOGO_RB_CUSTOM_LOC = "custom_logo_id"
LOGO_INPUT_LOC = "custom_logo"
LOGIN_MSG_LOC = "custom_login_message"
LOCAL_USERS_LINK_LOC = "adminusers_dialog_link"
LDAP_GROUPS_LINK_LOC = "external_admin_groups_dialog_link"
CUSTOM_ROLES_LINK_LOC = "custom_roles_dialog_link"

END_USER_ACCESS_ENABLE_LOC = "enable_end_user_access"
END_USER_AUTH_LOC = "authentication"
END_USER_HIDE_BODIES_LOC = "hide_message_bodies"
END_USER_POP_LOC = "method_pop3"
END_USER_IMAP_LOC = "method_imap"
END_USER_SERVER_LOC = "server"
END_USER_SECUR_LOC = "transport"
END_USER_PORT_LOC = "port"
END_USER_DOMAIN_LOC = "default_domain"
END_USER_TEST_USER_LOC = "test_user"
END_USER_TEST_PASSW_LOC = "test_password"
END_USER_TEST_BUTTON_LOC = "//input[@type='button' and @value='Test']"

SPAM_NOTIF_ENABLE_LOC = "enable_notification"
SPAM_NOTIF_FROM_FNAME_LOC = "from_friendlyname"
SPAM_NOTIF_FROM_USERNAME_LOC = "from_username"
SPAM_NOTIF_FROM_DOMAIN_LOC = "from_domain"
SPAM_NOTIF_SUBJECT_LOC = "subject"
SPAM_NOTIF_TITLE_LOC = "title"
SPAM_NOTIF_LANG_LOC = "language"
SPAM_NOTIF_BODY_LOC = "template"
SPAM_NOTIF_FORMAT_LOC = "format"
SPAM_NOTIF_ENABLE_LOGIN_LOC = "enable_auto_login"
SPAM_NOTIF_BOUNCE_ADDR_LOC = "bounce_address"
SPAM_NOTIF_CONSOLID_LOC = "enable_alias_consolidation"
SPAM_NOTIF_MONTHLY_LOC = "monthly"
SPAM_NOTIF_WEEKLY_LOC = "weekly"
SPAM_NOTIF_WEEK_DAY_LOC = "notification_frequency_lo[]"
SPAM_NOTIF_DAILY_LOC = "specificdays"
SPAM_NOTIF_DAILY_SELECT_LOC = "notification_frequency_daily_select"
SPAM_NOTIF_HOUR_PREFIX_LOC = "notification_frequency_lo"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS = lambda day: "//*[@id='multi_days_picker_%s']" % day
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR = lambda hour: "//*[@id='time_picker_%s00']" % hour

SLBL_EDIT_BUTTON_LOC = "xpath=//form[@name='form_slbl']//input[@type='button' and @name='slbl_enable']"
SLBL_ENABLE_BUTTON_LOC = "xpath=//form[@name='form_slbl']//input[@type='button' and @name='slbl_enable' and contains(@value, 'Enable')]"
SLBL_ENABLE_CHECKBOX_LOC = "//input[@type='checkbox' and @name='enable_slbl']"
SLBL_MAX_ITEMS_LOC = "max_slbl_entries"
SLBL_UPDATE_FREQ_LOC = "update_frequency_period"

class SpamQuarantine(GuiCommon):
    """ Keywords for "Management Appliance-> Centralized Services -> Spam
    Quarantine" GUI page. """

    def get_keyword_names(self):
        return [
                'spam_quarantine_enable',
                'spam_quarantine_edit',
                'spam_quarantine_edit_enduser_access',
                'spam_quarantine_edit_notification',
                'spam_quarantine_disable',
                'spam_quarantine_slbl_enable',
                'spam_quarantine_slbl_edit',
                'spam_quarantine_slbl_disable',
                'spam_quarantine_sync_appliances',
                ]


    def _open_page(self):
        """ Open 'Spam Quarantine' page """
        self._navigate_to('Management Appliance', 'Centralized Services', 'Spam Quarantine')


    def _is_isq_enabled(self):
        """ Return True if the ISQ is already enabled """
        return not self._is_element_present(ENABLE_BUTTON_LOC)


    def _open_form(self):
        """ Open 'Edit Spam Quarantine' page """
        self.click_button(EDIT_BUTTON_LOC)

    def _get_result(self):
        try:
            res, msg = self._check_action_result()
            result = '%s: %s' % (res, msg)
        except GuiValueError as err:
            result = err
        return result

    def _select_on_dialog(self, items_list, clear_others=False):
        """ Selects items, specified in items_list, on open dialog. """
        absent_items = ''
        items_found = map(lambda s:False, items_list)

        dialog_loc = "//div[contains(@id, 'dialog_c') and contains(@style, 'visible')]"
        if not self._is_element_present(dialog_loc):
            raise ValueError("No open dialog was found.")
            return absent_items

        # Loop through labels on the dialog.
        labels_loc = dialog_loc + "//label"
        checkboxes_loc = dialog_loc + "//input[@type = 'checkbox']"
        labels_count = int(self.get_matching_xpath_count(labels_loc))
        for label_num in range(1, labels_count + 1):
            label_loc = "xpath=(" + labels_loc + ")[" + str(label_num) + "]"
            label_text = self.get_text(label_loc)
            checkbox_loc = "xpath=(" + checkboxes_loc + ")[" + str(label_num) + "]"
            checkbox_needed = False

            # Loop through input list to find if the checkbox should be checked
            for index, item in enumerate(items_list):
                if re.search(item, label_text) is not None:
                    items_found[index] = True
                    checkbox_needed = True
                    break
            checkbox_state = self._is_checked(checkbox_loc)
            if checkbox_needed and (not checkbox_state):
                self._set_checkbox(True, checkbox_loc)
            elif (not checkbox_needed) and clear_others and checkbox_state:
                self._set_checkbox(False, checkbox_loc)

        # Collect not found items to report in Log.
        for index, item_found in enumerate(items_found):
            if not item_found:
                absent_items += "'" + items_list[index] + "', "
        if absent_items != '':
            absent_items = "Items [" + absent_items + \
            "] were not found on dialog '" + \
            self.get_text(dialog_loc + "//*[contains(@id, 'dialog_h')]") + \
            "'."

        # Close dialog
        OK_loc = dialog_loc+"//*[@type='button' and text()='OK']"
        self.click_button(OK_loc, "don't wait")

        return absent_items


    def _select_item_from_list(self, select_list, item, list_name=''):
        if item is None:
            return

        if list_name != '': list_name = "'" + list_name + "' "

        if not self._is_element_present(select_list):
            raise self.GuiFeatureDisabledError(\
                '%slist is not available' % (list_name,))

        splitter_position = int(item.rfind(' > '))
        self._debug(splitter_position)

        group_name = ''
        item_name = ''
        if(splitter_position > -1):
            group_name = item[0:splitter_position]
            self._info('"' + group_name + '"')
            item_name = item[(splitter_position+3):len(item)]
            self._info('"' + item_name + '"')
        else:
            item_name = item

        location_prefix = '//select[@name=\'' + select_list + '\']'
        optgroups = int(self.get_matching_xpath_count(location_prefix + '/optgroup[@label]'))
        self._debug(optgroups)

        if (optgroups > 0):
            group_loc = location_prefix + '/optgroup[@label=\'' + group_name + '\']'
            if ( int(self.get_matching_xpath_count(group_loc)) > 0):
                item_loc = group_loc + '/option[contains(text(),\''+item_name+'\')]'
                if (int(self.get_matching_xpath_count(item_loc)) > 0):
                    item_value = self.get_element_attribute(item_loc+'@value')
                    self.select_from_list(select_list, item_value)
                else:
                    raise ValueError('"%s" item of "%s" in "%s"list is not avaliable' %\
                    (item_name, group_name, list_name))
            else:
                raise ValueError('"%s" group in %slist is not avaliable' %\
                    (group_name, list_name))
        else:
            item_loc = location_prefix + '/option[contains(text(),\''+item_name+'\')]'
            if (int(self.get_matching_xpath_count(item_loc)) > 0):
                item_value = self.get_element_attribute(item_loc + "@value")
                self.select_from_list(select_list, item_value)
            else:
                raise ValueError('"%s" item in "%s"list is not avaliable' %\
                (item_name, list_name))


    def spam_quarantine_enable(self, interface=None, port=None ):
        """ Enable Spam Quarantine settings.

        Parameters:
            - `interface`:
                Quarantine IP Interface.
            - `port`:
                Quarantine Port. It is required parameter and must be > 0.

        Examples:
        | Spam Quarantine Enable |
        | ... | port=6000 |
        | Spam Quarantine Enable |
        | ... | interface=Management |
        | ... | port=6500 |
        """

        self._open_page()

        if self._is_isq_enabled():
            self._info("Spam Quarantine was already enabled")

        self._open_form()
        self._accept_license()

        if not self._is_checked(ENABLE_CHECKBOX_LOC):
            self.click_element(ENABLE_CHECKBOX_LOC)

        if interface is not None:
            self.select_from_list(INTERFACE_LOC, interface)
        if port is not None:
            self.input_text(PORT_LOC, port)

        self._click_submit_button(wait=False, accept_confirm_dialog=True)


    def spam_quarantine_edit(self, interface=None, port=None,
        primary_server=None, primary_port=None, alternative_server=None,
        alternative_port=None, delete_after=None, send_copy=None, logo=None, login_msg=None,
        local_users=None, ldap_groups=None, custom_roles=None ):
        """ Edit Spam Quarantine general settings.

        Parameters:
            - `interface`:
                Quarantine IP Interface.
            - `port`:
                Quarantine Port.
            - `primary_server`:
                IP adress or hostname of Primary Server of 'Deliver Messages Via'.
            - `primary_port`:
                Port of Primary Server in 'Deliver Messages Via' section.
            - `alternative_server`:
                Alternative Server of 'Deliver Messages Via'.
            - `alternative_port`:
                Port of Alternative Server in 'Deliver Messages Via' section.
            - `delete_after`:
                Number of days to keep spam emails.
                ${False} means 'Do not schedule delete'.
            - `send_copy`:
                Send or not send a copy of released messages to IronPort for analysis.
                Either ${True} or ${False}.
            - `logo`:
                Spam Quarantine logo. Either 'current', 'ironport', or filename.
            - `login_msg`:
                Login Page Message.
            - `local_users`:
                Local users which should have access to Spam Quarantine.
                String of comma-separated usernames.
            - `ldap_groups`:
                LDAP groups which should have access to Spam Quarantine.
                String of comma-separated names.
            - `custom_roles`:
                Custom user roles which should supply access to Spam Quarantine.
                String of comma-separated names.

        Examples:
        | Spam Quarantine Edit |
        | ... | port=6000 |
        | ... | interface=Management |
        | ... | primary_server=192.168.31.10 |
        | ... | primary_port=147 |
        | ... | alternative_server=192.168.31.10 |
        | ... | alternative_port=147 |
        | ... | delete_after=80 |
        | ... | send_copy=${True} |
        | ... | logo=~/work/sarf_centos/tests/testdata/euq_ironport_default_logo.gif |
        | ... | login_msg=test message |
        | Spam Quarantine Edit |
        | ... | local_users=ivan1,ivan2 |
        | ... | ldap_groups=Help Desk Users, Guests |
        | ... | custom_roles=test email role |
        """
        message = ''

        self._open_page()

        if not self._is_isq_enabled():
            raise ValueError("Spam Quarantine was not enabled")

        self._open_form()

        if interface is not None:
            self.select_from_list(INTERFACE_LOC, interface)
        if port is not None:
            self.input_text(PORT_LOC, port)

        if primary_server is not None:
            self.input_text(PRIMARY_SERVER_LOC, primary_server)
        if primary_port is not None:
            self.input_text(PRIMARY_PORT_LOC, primary_port)

        if alternative_server is not None:
            self.input_text(ALTERNATIVE_SERVER_LOC, alternative_server)
        if alternative_port is not None:
            self.input_text(ALTERNATIVE_PORT_LOC, alternative_port)

        if delete_after is not None:
            if delete_after is not False:
                self._click_radio_button(DELETE_AFTER_RB1_LOC)
                self.input_text(DELETE_AFTER_DAYS_LOC, delete_after)
            else:
                self._click_radio_button(DELETE_AFTER_RB2_LOC)

        if send_copy is not None:
            send_copy_checked = self._is_checked(SEND_COPY_LOC)
            if send_copy != send_copy_checked:
                self.click_element(SEND_COPY_LOC, "don't wait")

        if logo is not None:
            logo = logo.lower()
            if logo == 'current':
                self._click_radio_button(LOGO_RB_CURRENT_LOC)
            elif logo == 'ironport':
                self._click_radio_button(LOGO_RB_DEFAULT_LOC)
            else:
                self._click_radio_button(LOGO_RB_CUSTOM_LOC)
                self.input_text(LOGO_INPUT_LOC, logo)

        if login_msg is not None:
            self.input_text(LOGIN_MSG_LOC, login_msg)

        if local_users is not None:
            local_users_list = map(lambda s:s.strip(), local_users.split(','))
            self.click_element(LOCAL_USERS_LINK_LOC, "don't wait")
            message += self._select_on_dialog(local_users_list)

        if ldap_groups is not None:
            ldap_groups_list = map(lambda s:s.strip(), ldap_groups.split(','))
            self.click_element(LDAP_GROUPS_LINK_LOC, "don't wait")
            message += self._select_on_dialog(ldap_groups_list)

        if custom_roles is not None:
            custom_roles_list = map(lambda s:s.strip(), custom_roles.split(','))
            self.click_element(CUSTOM_ROLES_LINK_LOC, "don't wait")
            message += self._select_on_dialog(custom_roles_list)

        self._click_submit_button(wait=False, accept_confirm_dialog=True)

        if len(message) > 0:
            raise ValueError(message)


    def spam_quarantine_edit_enduser_access(self, end_user_access_enable=None,
        end_user_auth=None, end_user_mail_type=None, end_user_mail_server=None,
        end_user_mail_security=None, end_user_mail_port=None, end_user_mail_domain=None,
        end_user_mail_test_user=None, end_user_mail_test_password=None, end_user_mail_test=None,
        end_user_hide_body=None ):
        """ Edit Spam Quarantine End-User Access settings.

        Parameters:
            - `end_user_access_enable`:
                Enable End-User Quarantine Access. Either ${True} or ${False}.
            - `end_user_auth`:
                Authentication method for End-User Quarantine Access.
                Either 'None', 'Mailbox (IMAP/POP)' or 'LDAP'.
                It is available only if 'End-User Quarantine Access' is enabled
            - `end_user_mail_type`:
                Mailbox type for End-User Quarantine Access.
                Either 'POP' or 'IMAP'.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_server`:
                Hostname or IP address of mail server.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_security`:
                Security type of the connection with mail server.
                'None' or 'SSL'.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_port`:
                Port number of the connection with mail server.
                Default value corresponds to selected mail server type and security type.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_domain`:
                Domain for unqualified usernames.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_test_user`:
                Username for testing mailbox settings.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_test_password`:
                Password of specified user for testing mailbox settings.
                It is available only for 'Mailbox' authentication method.
            - `end_user_mail_test`:
                Perform testing of specified mailbox settings (by 'Test' button).
                Either ${True} or ${False}.
                It is available only for 'Mailbox' authentication method.
            - `end_user_hide_body`:
                Do not display message bodies to end-users until message is released.
                Either ${True} or ${False}.

        Examples:
        | Spam Quarantine Edit EndUser Access |
        | ... | end_user_access_enable=${True} |
        | ... | end_user_auth=Mailbox (IMAP/POP) |
        | ... | end_user_mail_type=POP |
        | ... | end_user_mail_server=192.168.31.10 |
        | ... | end_user_mail_security=SSL |
        | ... | end_user_mail_port=980 |
        | ... | end_user_mail_domain=testdomain.com |
        | ... | end_user_mail_test_user=testuser |
        | ... | end_user_mail_test_password=123456 |
        | ... | end_user_hide_body=${True} |
        | Spam Quarantine Edit EndUser Access |
        | ... | end_user_access_enable=${False} |
        """
        self._open_page()
        self._open_form()

        enable_end_user_access_checked = self._is_checked(END_USER_ACCESS_ENABLE_LOC)
        if end_user_access_enable is not None:
            if end_user_access_enable != enable_end_user_access_checked:
                self.click_element(END_USER_ACCESS_ENABLE_LOC, "don't wait")
                for i in range(0, 100):
                    if self._is_checked(END_USER_ACCESS_ENABLE_LOC) == end_user_access_enable:
                        break
                    else:
                        time.sleep(3)
                if self._is_checked(END_USER_ACCESS_ENABLE_LOC) != end_user_access_enable:
                    raise ValueError("End-User Quarantine Access was not enabled.")
        enable_end_user_access_checked = self._is_checked(END_USER_ACCESS_ENABLE_LOC)

        if (end_user_auth is not None) and enable_end_user_access_checked:
            self.select_from_list(END_USER_AUTH_LOC, end_user_auth)

        if (end_user_hide_body is not None) and enable_end_user_access_checked:
            if end_user_hide_body != self._is_checked(END_USER_HIDE_BODIES_LOC):
                self.click_element(END_USER_HIDE_BODIES_LOC, "don't wait")

        if (end_user_mail_type is not None) and enable_end_user_access_checked:
            end_user_mail_type = end_user_mail_type.lower().strip()
            if end_user_mail_type == 'pop':
                self._click_radio_button(END_USER_POP_LOC)
            elif end_user_mail_type == 'imap':
                self._click_radio_button(END_USER_IMAP_LOC)
            else:
                raise ValueError("Mail method '%s' was not found in 'End-User Authentication' form." % end_user_mail_method)

        if (end_user_mail_server is not None) and enable_end_user_access_checked:
            self.input_text(END_USER_SERVER_LOC, end_user_mail_server)

        if (end_user_mail_security is not None) and enable_end_user_access_checked:
            self.select_from_list(END_USER_SECUR_LOC, end_user_mail_security)

        if (end_user_mail_port is not None) and enable_end_user_access_checked:
            self.input_text(END_USER_PORT_LOC, end_user_mail_port)

        if (end_user_mail_domain is not None) and enable_end_user_access_checked:
            self.input_text(END_USER_DOMAIN_LOC, end_user_mail_domain)

        if (end_user_mail_test_user is not None) and enable_end_user_access_checked:
            self.input_text(END_USER_TEST_USER_LOC, end_user_mail_test_user)

        if (end_user_mail_test_password is not None) and enable_end_user_access_checked:
            self.input_text(END_USER_TEST_PASSW_LOC, end_user_mail_test_password)

        if (end_user_mail_test is True) and enable_end_user_access_checked:
            self.click_button(END_USER_TEST_BUTTON_LOC)
            self._check_action_result()

        self._click_submit_button(wait=False, accept_confirm_dialog=True)


    def spam_quarantine_edit_notification(self,
                                          spam_notif_enable=None,
                                          spam_notif_fname=None,
                                          spam_notif_username=None,
                                          spam_notif_domain=None,
                                          spam_notif_subject=None,
                                          spam_notif_title=None,
                                          spam_notif_lang=None,
                                          spam_notif_body=None,
                                          spam_notif_enable_login=None,
                                          spam_notif_format=None,
                                          spam_notif_baddr=None,
                                          spam_notif_consolidate=None,
                                          spam_notif_freq=None,
                                          spam_notif_week_day=None,
                                          spam_notif_days=None,
                                          spam_notif_hours=None,
                                          submit=True):
        """ Edit Spam Quarantine Notification settings.

        Parameters:
            - `spam_notif_enable`:
                Enable Spam Notification. Either ${True} or ${False}.
            - `spam_notif_fname`:
                Friendly name for "From" address.
                It is available only if Spam Notification is enabled.
            - `spam_notif_username`:
                Username for "From" address.
                It is available only if Spam Notification is enabled.
            - `spam_notif_domain`:
                Domain for "From" address.
                It is available only if Spam Notification is enabled.
            - `spam_notif_subject`:
                Subject for notification email.
                It is available only if Spam Notification is enabled.
            - `spam_notif_title`:
                Title for notification email.
                It is available only if Spam Notification is enabled.
            - `spam_notif_lang`:
                Language of notification email.
                It is available only if Spam Notification is enabled.
            - `spam_notif_body`:
                String for template of message body.
                Such variables can be used in the template:
                %new_message_count%, %total_message_count%,
                %days_until_expire%, %quarantine_url%,
                %username%, %new_quarantine_messages%.
                It is available only if Spam Notification is enabled.
            - `spam_notif_enable_login`:
                Enable Login Without Credentials For Quarantine Access
                It is available only if Spam Notification is enabled.
                Either ${True} or ${False}.
            - `spam_notif_format`:
                Format for notification email. Either 'HTML', 'Text' or 'HTML/Text'.
                It is available only if Spam Notification is enabled.
            - `spam_notif_baddr`:
                Email address for deliver bounce message.
                It is available only if Spam Notification is enabled.
            - `spam_notif_consolidate`:
                Consolidate notifications sent to the same LDAP user
                at different addresses.
                Either ${True} or ${False}.
                It is available only if Spam Notification is enabled.
            - `spam_notif_freq`:
                Frequency for sending Spam Notification.
                Either 'monthly', 'weekly' or 'daily'.
                It is available only if Spam Notification is enabled.
            - `spam_notif_week_day`:
                Week day for sending Spam Notification.
                It is available only if 'weekly' frequency was selected
                for Spam Notification.
            - `spam_notif_days`:Select weekday.
                Correct values are Mon, Tue, Wed, Thu, Fri, Sat, Sun.
                List or CSV.
                It is available only if 'daily' frequency was selected
                for Spam Notification.
            - `spam_notif_hours`: Hours.
                Correct values are: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10,... 23.
                List or CSV.
                It is available only if 'daily' frequency was selected
                for Spam Notification.
            - `submit`: Submit changes. Boolean.

        Examples:
        | Spam Quarantine Edit Notification |
        | ... | spam_notif_enable=${True} |
        | ... | spam_notif_fname=Tester Testerovich |
        | ... | spam_notif_username=testuser |
        | ... | spam_notif_domain=test.com |
        | ... | spam_notif_subject=Test Subject |
        | ... | spam_notif_title=Test title |
        | ... | spam_notif_lang=[ru] |
        | ... | spam_notif_body=Test body\r\ntest. |
        | ... | spam_notif_enable_login=${True} |
        | ... | spam_notif_format=HTML/Text |
        | ... | spam_notif_baddr=test@qa.qa |
        | ... | spam_notif_consolidate=${True} |
        | ... | spam_notif_freq=daily |
        | ... | spam_notif_week_day=${None} |
        | ... | spam_notif_days=Mon, Tue, Fri |
        | ... | spam_notif_hours=03,15,21 |
        | Spam Quarantine Edit Notification |
        | ... | spam_notif_enable=${False} |
        """
        self._open_page()
        self._open_form()

        spam_notif_enable_checked = self._is_checked(SPAM_NOTIF_ENABLE_LOC)
        if spam_notif_enable is not None:
            if spam_notif_enable != spam_notif_enable_checked:
                self.click_element(SPAM_NOTIF_ENABLE_LOC, "don't wait")
                for i in range(0, 100):
                    if self._is_checked(SPAM_NOTIF_ENABLE_LOC) == spam_notif_enable:
                        break
                    else:
                        time.sleep(3)
                if self._is_checked(SPAM_NOTIF_ENABLE_LOC) != spam_notif_enable:
                    raise ValueError("Spam Notification was not enabled.")
            spam_notif_enable_checked = self._is_checked(SPAM_NOTIF_ENABLE_LOC)

        if (spam_notif_fname is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_FROM_FNAME_LOC, spam_notif_fname)

        if (spam_notif_username is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_FROM_USERNAME_LOC, spam_notif_username)

        if (spam_notif_domain is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_FROM_DOMAIN_LOC, spam_notif_domain)

        if (spam_notif_subject is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_SUBJECT_LOC, spam_notif_subject)

        if (spam_notif_title is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_TITLE_LOC, spam_notif_title)

        if (spam_notif_lang is not None) and spam_notif_enable_checked:
            self._select_item_from_list(SPAM_NOTIF_LANG_LOC, spam_notif_lang, "Spam Notification Language")

        if (spam_notif_body is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_BODY_LOC, spam_notif_body)

        if (spam_notif_enable_login is not None) and spam_notif_enable_checked:
                self._select_checkbox(SPAM_NOTIF_ENABLE_LOGIN_LOC)

        if (spam_notif_format is not None) and spam_notif_enable_checked:
            self._select_item_from_list(SPAM_NOTIF_FORMAT_LOC, spam_notif_format, "Spam Notification Format")

        if (spam_notif_baddr is not None) and spam_notif_enable_checked:
            self.input_text(SPAM_NOTIF_BOUNCE_ADDR_LOC, spam_notif_baddr)

        if (spam_notif_consolidate is not None) and spam_notif_enable_checked:
            if spam_notif_consolidate != self._is_checked(SPAM_NOTIF_CONSOLID_LOC):
                self.click_element(SPAM_NOTIF_CONSOLID_LOC, "don't wait")

        if (spam_notif_freq is not None) and spam_notif_enable_checked:
            spam_notif_freq = spam_notif_freq.lower().strip()
            if spam_notif_freq == 'monthly':
                self._click_radio_button(SPAM_NOTIF_MONTHLY_LOC)
            elif spam_notif_freq == 'weekly':
                self._click_radio_button(SPAM_NOTIF_WEEKLY_LOC)
            elif spam_notif_freq == 'daily':
                self._click_radio_button(SPAM_NOTIF_DAILY_LOC)
                self._set_daily_notification_schedule\
                (spam_notif_days, spam_notif_hours)
            else:
                raise ValueError("Spam Notification Frequency '%s' was not found in 'Spam Notification' form." % spam_notif_freq)

        if (spam_notif_week_day is not None) and spam_notif_enable_checked:
            self._select_item_from_list(SPAM_NOTIF_WEEK_DAY_LOC, spam_notif_week_day, "Spam Notification Weekly Day")

        if submit:
            self._click_submit_button(wait=False, accept_confirm_dialog=True)


    def _convert_str_to_list(self, value, separator=","):
        if isinstance(value, basestring):
            value = map(lambda x: x.strip(), value.split(separator))
        return value

    def _set_daily_notification_schedule(self,
                                         notification_schedule_weekdays,
                                         notification_schedule_hours ):

        notification_schedule_weekdays = self._convert_str_to_list(
                                            notification_schedule_weekdays)
        notification_schedule_hours    = self._convert_str_to_list(
                                            notification_schedule_hours)
        notification_schedule_weekdays =\
            [day.lower() for day in notification_schedule_weekdays]
        days  = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                 '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17', '18', '19', '20', '21', '22', '23')

        #Clear previous schedule
        for day in days:
            self._unselect_checkbox\
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS(day))
        for hour in hours:
            self._unselect_checkbox\
                (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR(hour))

        #Set new for days
        for day in notification_schedule_weekdays:
            if day in days:
                self._select_checkbox\
                    (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS(day))
            else:
                raise ValueError\
                ('Incorrect day parameter: %s. Should be one from: %s ' %\
                    (day, ','.join(days)))

        #For hours
        if notification_schedule_hours is not None:
            for hour in notification_schedule_hours:
                if hour in hours:
                    self._select_checkbox\
                        (SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR(hour))
                else:
                    raise ValueError\
                    ('Incorrect hour parameter: %s. Should be one from: %s ' %\
                        (hour, ','.join(hours)))


    def spam_quarantine_disable(self):
        """ Disable Spam Quarantine feature.

        Examples:
        | Spam Quarantine Disable |
        """
        self._open_page()
        if self._is_isq_enabled():
            self._open_form()
            self.click_element(ENABLE_CHECKBOX_LOC, "don't wait")
            self._click_submit_button(wait=False, accept_confirm_dialog=True)
        else:
            self._info("'Spam Quarantine' was already disabled.")


    def spam_quarantine_slbl_enable(self):
        """ Enable Safelist/Blocklist settings.

        Examples:
        | Spam Quarantine SlBl Enable |
        """
        self._open_page()

        if not self._is_isq_enabled():
            raise ValueError("Spam Quarantine was not enabled. Safelist/Blocklist settings are not available.")

        if self._is_element_present(SLBL_ENABLE_BUTTON_LOC):
            self.click_button(SLBL_ENABLE_BUTTON_LOC)
        else:
            self._info("Safelist/Blocklist settings were already enabled.")


    def spam_quarantine_slbl_edit(self, max_items=None, update_frequency=None):
        """ Edit Safelist/Blocklist settings.

        Parameters:
            - `max_items`:
                    Maximum List Items Per User.
            - `update_frequency`:
                    Update Frequency. Either 'Every 10 minutes', 'Every 15 minutes', 'Every 20 minutes',
                    'Every 30 minutes', 'Every hour', 'Every 2 hours', 'Every 3 hours', 'Every 4 hours',
                    'Every 6 hours', 'Every 12 hours', 'Every 24 hours'.

        Examples:
        | Spam Quarantine SlBl Edit |
        | ... | max_items=300 |
        | ... | update_frequency=10 minutes |
        """
        self._open_page()

        if (not self._is_isq_enabled()) or self._is_element_present(SLBL_ENABLE_BUTTON_LOC):
            raise ValueError("Spam Quarantine Safelist/Blocklist settings were\
            not enabled. Editing of Safelist/Blocklist settings are not available.")

        self.click_button(SLBL_EDIT_BUTTON_LOC)

        if max_items is not None:
            self.input_text(SLBL_MAX_ITEMS_LOC, max_items)

        if update_frequency is not None:
            self._select_item_from_list(SLBL_UPDATE_FREQ_LOC, update_frequency, "SLBL Update Frequency")

        self._click_submit_button(wait=False, accept_confirm_dialog=True)


    def spam_quarantine_slbl_disable(self):
        """ Disable Safelist/Blocklist settings.

        Examples:
        | Spam Quarantine Slbl Disable |
        """
        self._open_page()

        if not self._is_isq_enabled():
            raise ValueError("Spam Quarantine was not enabled. Safelist/Blocklist settings are not available.")

        if not self._is_element_present(SLBL_ENABLE_BUTTON_LOC):
            self.click_button(SLBL_EDIT_BUTTON_LOC)
            self.click_element(SLBL_ENABLE_CHECKBOX_LOC, "don't wait")
            self._click_submit_button(wait=False, accept_confirm_dialog=True)
        else:
            self._info("Safelist/Blocklist settings were already disabled.")

    def spam_quarantine_sync_appliances(self):
        """ File Transfer - Synchronize All Appliances.

        Examples:
        | Spam Quarantine Sync Appliances |
        """
        self._open_page()
        if (not self._is_isq_enabled()) or self._is_element_present(SLBL_ENABLE_BUTTON_LOC):
            raise GuiValueError("Spam Quarantine Safelist/Blocklist settings were not enabled.")
        if not self._is_element_present(SYNC_ALL_APPLIANCES_BUTTON_LOC):
            raise GuiValueError("Can't synchronize appliances. Are there any appliances available?")
        self.click_button(SYNC_ALL_APPLIANCES_BUTTON_LOC)
        return self._get_result()
