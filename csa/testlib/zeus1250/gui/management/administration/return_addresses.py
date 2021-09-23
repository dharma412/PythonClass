#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/management/administration/return_addresses.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.gui.guicommon import GuiCommon


BOUNCE_DISPLAY_TEXTBOX = 'name=BOUNCEFROM_friendlyname'
BOUNCE_USERNAME_TEXTBOX = 'name=BOUNCEFROM_username'
BOUNCE_HOSTNAME_TEXTBOX = 'name=BOUNCEFROM_hostname'
BOUNCE_LOCATORS = (BOUNCE_DISPLAY_TEXTBOX, BOUNCE_USERNAME_TEXTBOX,
                   BOUNCE_HOSTNAME_TEXTBOX)
REPORTS_DISPLAY_TEXTBOX = 'name=REPORTSFROM_friendlyname'
REPORTS_USERNAME_TEXTBOX = 'name=REPORTSFROM_username'
REPORTS_HOSTNAME_TEXTBOX = 'name=REPORTSFROM_hostname'
REPORTS_LOCATORS = (REPORTS_DISPLAY_TEXTBOX, REPORTS_USERNAME_TEXTBOX,
                    REPORTS_HOSTNAME_TEXTBOX)
OTHER_DISPLAY_TEXTBOX = 'name=ZZZOTHERFROM_friendlyname'
OTHER_USERNMAE_TEXTBOX = 'name=ZZZOTHERFROM_username'
OTHER_HOSTNAME_TEXTBOX = 'name=ZZZOTHERFROM_hostname'
OTHER_LOCATORS = (OTHER_DISPLAY_TEXTBOX, OTHER_USERNMAE_TEXTBOX,
                  OTHER_HOSTNAME_TEXTBOX)


class ReturnAddresses(GuiCommon):

    """
	Keyword library for menu Managment Appliance -> SystemAdministration ->
        Return Addresses
    """

    def get_keyword_names(self):
           return ['return_addresses_edit_bounce',
                   'return_addresses_edit_reports',
                   'return_addresses_edit_other',
                  ]

    def _open_page(self):
          self._navigate_to('Management', 'System Administration',
                               'Return Addresses')

    def _fill_address_row(self, locators, values):
        for method, locator, value in\
                 zip((self._fill_display_name,
                     self._fill_username,
                     self._fill_hostname),
                      locators, values):
              method(locator, value)

    def _fill_display_name(self, locator, name):
        if name != None:
            self.input_text(locator, name)
            self._info('Set display name to "%s".' % (name,))

    def _fill_username(self, locator, username):
        if username != None:
           self.input_text(locator, username)
           self._info('Set username to "%s".' % (username,))

    def _fill_hostname(self, locator, hostname):
        if hostname != None:
            self.input_text(locator, hostname)
            self._info('Set hostname to "%s".' % (hostname,))

    def return_addresses_edit_bounce(self, display_name=None, username=None,\
            hostname=None):
        """Edit return addresses for bounce message.

        *Parameters*
            - `display_name`: subject in generated mail for bounce messages.
                        String. If None, field will be left unchanged. Default
                        value is None.
            - `username`: username of sender in bounce mail message . String.
                        If None, field will be left unchanged. Default value in
                        None.
            - `hostname`: hostname of sender in bounce mail message. String. If
                        None, field will be left unchanged. Default value is
                        None.

        *Return*
            None.

	*Exceptions*
            None.

	*Examples*
            | Return Addresses Edit Bounce | display_name=bonce message |
            | ... | username=deamon | hostname=anyhost.com |
            | Return Addresses Edit Bounce | hostname=myhost.com |
            | Return Addresses Edit Bounce | bonce message | deamon |
            | ... | anyhost.com |
        """
        self._info('Editing return addresses for bounce.')

        self._open_page()

        self._click_edit_settings_button()

        self._fill_address_row(BOUNCE_LOCATORS, [display_name, username,\
            hostname])

        self._click_submit_button()

        self._info('Edited return addresses for bounce.')

    def return_addresses_edit_reports(self, display_name=None, username=None,\
            hostname=None):
        """Edit return addresses for reports message.

        *Parameters*
            - `display_name`: subject in generated mail for reports messages.
                        String. If None, field will be left unchanged. Default
                        value is None.
            - `username`: username of sender in reports mail message . String.
                        If None, field will be left unchanged. Default value in
                        None.
            - `hostname`: hostname of sender in reports mail message. String. If
                        None, field will be left unchanged. Default value is
                        None.

        *Return*
            None.

	*Exceptions*
            None.

	*Examples*
            | Return Addresses Edit Reports | display_name=reports message |
            | ... | username=deamon | hostname=anyhost.com |
            | Return Addresses Edit Reports | hostname=myhost.com |
            | Return Addresses Edit Reports | reports message | deamon |
            | ... | anyhost.com |
        """
        self._info('Editing return addresses for reports.')

        self._open_page()

        self._click_edit_settings_button()

        self._fill_address_row(REPORTS_LOCATORS, [display_name, username,\
            hostname])

        self._click_submit_button()

        self._info('Edited return addresses for repotrs.')

    def return_addresses_edit_other(self, display_name=None, username=None,\
            hostname=None):
        """Edit return addresses for others message.

        *Parameters*
            - `display_name`: subject in generated mail for others messages.
                        String. If None, field will be left unchanged. Default
                        value is None.
            - `username`: username of sender in other mail message . String.
                        If None, field will be left unchanged. Default value in
                        None.
            - `hostname`: hostname of sender in other mail message. String. If
                        None, field will be left unchanged. Default value is
                        None.

        *Return*
            None.

	*Exceptions*
            None.

	*Examples*
            | Return Addresses Edit Other | display_name=other message |
            | ... | username=deamon | hostname=anyhost.com |
            | Return Addresses Edit Other | hostname=myhost.com |
            | Return Addresses Edit Other | other message | deamon |
            | ... | anyhost.com |
        """
        self._info('Editing return addresses for Other.')

        self._open_page()

        self._click_edit_settings_button()

        self._fill_address_row(OTHER_LOCATORS, [display_name, username,\
            hostname])

        self._click_submit_button()

        self._info('Edited return addresses for Other.')
