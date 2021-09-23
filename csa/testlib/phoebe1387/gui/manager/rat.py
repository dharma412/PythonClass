#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/rat.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from access_table_def.access_table_base import AccessTableBase, go_to_access_table, \
                LISTENER_DROPDOWN
from access_table_def.recipient_settings import RecipientSettings


ADD_RECIPIENT_BUTTON = "//input[@value='Add Recipient...']"

RAT_TABLE = "//table[@class='cols']"
DELETE_CHECKBOX = lambda recv_domain: "//input[@value='%s']" % (recv_domain,)
DELETE_BUTTON = "//input[@value='Delete']"
CLEAR_ALL_BUTTON = "//input[@value='Clear All Entries']"
IMPORT_BUTTON = "//input[@value='Import RAT...']"
EXPORT_BUTTON = "//input[@value='Export RAT...']"
IMPORT_FILE_DROPBOX = "//select[@id='impexpfile']"
EXPORT_FILE_TEXTBOX = "//input[@name='file_server']"
EDIT_ORDER_BUTTON = "//input[@value='Edit Order...']"
RAT_ORDER_TABLE = "//table[@class='cols']"
RECIPIENT_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                        (RAT_ORDER_TABLE, name)

RECIPIENT_ORDER_EDIT = lambda name: "%s//td[.//a[normalize-space()='%s']]"\
                        "/preceding-sibling::td[1]/input" % \
                        (RAT_ORDER_TABLE, name)

STANDARD_RECIPIENTS_ENTRY = 'All Other Recipients'

RAT_PAGE_PATH = ('Mail Policies', 'Recipient Access Table (RAT)')
LISTENER_OPTS = (LISTENER_DROPDOWN, RAT_TABLE)

class rat(AccessTableBase):
    """Interaction class for ESA WUI
       Mail Policies -> Recipient Access Table (RAT) page.
    """

    def get_keyword_names(self):
        return ['rat_recipient_add',
                'rat_recipient_edit',
                'rat_recipient_delete',
                'rat_clear_all',
                'rat_import',
                'rat_export',
                'rat_edit_order',
                'rat_get_all']

    def _get_recipient_settings_controller(self):
        if not hasattr(self, '_recipient_settings_controller'):
            self._recipient_settings_controller = RecipientSettings(self)
        return self._recipient_settings_controller

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_recipient_add(self, listener_name, **kwargs):
        """Add new recipient to RAT

        *Parameters:*
        - `listener_name`: listener name to which this recipient will be added,
        mandatory
        - `address`: new recipient address, mandatory. The following formats
        are allowed:
        | Hostnames such as "example.com", "[1.2.3.4]", "[2001:420:80:1::5]" |
        | Partial hostnames such as ".example.com" |
        | Usernames such as "postmaster@" |
        | Full email addresses such as "joe@example.com", "joe@[1.2.3.4]" or
        "joe@[ipv6:2001:420:80:1::5]" |
        | Multiple addresses separated with commas. |
        - `action`: RAT action for this recipient, either Accept or
        Reject
        - `order`: entry order number, acceptable values are in range 1..5
        - `bypass_ldap_accept`: whether to bypass LDAP Accept Queries
        for this Recipient (accessible only if corresponding LDAP query
        is configured), either ${True} or ${False}
        - `smtp_response`: whether to enable or disable custom SMPT response,
        either ${True} or ${False}
        - `smtp_response_code`: custom SMTP response code (only if smtp_response is
        set to ${True}), number
        - `smtp_response_text`: custom SMTP response text (only if smtp_response is
        set to ${True}), string
        - `bypass`: whether to Bypass Receiving Control, either ${True} or ${False}

        *Examples*:
        | RAT Recipient Add | InBoundMail | address=.auto | action=Accept |
        | RAT Recipient Add | InBoundMail | address=.sma | action=Reject |
        | ... | smtp_response=${True} | smtp_response_code=150 |
        | ... | smtp_response_text=blabla |
        """
        self.click_button(ADD_RECIPIENT_BUTTON)

        controller = self._get_recipient_settings_controller()
        controller.set(kwargs)
        self._click_submit_button()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_recipient_edit(self, listener_name, old_address, **kwargs):
        """Add new recipient to RAT

        *Parameters:*
        - `listener_name`: listener name where this recipient will be edited,
        mandatory
        - `old_address`: existing recipient address, can be 'All' to edit
        STANDARD_RECIPIENTS_ENTRY standard entry
        - `address`: new recipient address. The following formats
        are allowed:
        | Hostnames such as "example.com", "[1.2.3.4]", "[2001:420:80:1::5]" |
        | Partial hostnames such as ".example.com" |
        | Usernames such as "postmaster@" |
        | Full email addresses such as "joe@example.com", "joe@[1.2.3.4]" or
        "joe@[ipv6:2001:420:80:1::5]" |
        | Multiple addresses separated with commas. |
        - `action`: RAT action for this recipient, either Accept or
        Reject
        - `order`: entry order number, acceptable values are in range 1..5
        - `bypass_ldap_accept`: whether to bypass LDAP Accept Queries
        for this Recipient (accessible only if corresponding LDAP query
        is configured), either ${True} or ${False}
        - `smtp_response`: whether to enable or disable custom SMPT response,
        either ${True} or ${False}
        - `smtp_response_code`: custom SMTP response code (only if smtp_response is
        set to ${True}), number
        - `smtp_response_text`: custom SMTP response text (only if smtp_response is
        set to ${True}), string
        - `bypass`: whether to Bypass Receiving Control, either ${True} or ${False}

        *Exceptions:*
        - `ValueError`: if no recipient with given address is found

        *Examples*:
        | RAT Recipient Edit | InBoundMail | .auto | address=.qa | action=Accept |
        | RAT Recipient Edit | InBoundMail | .sma | action=Reject |
        | ... | smtp_response=${True} | smtp_response_code=150 |
        | ... | smtp_response_text=blabla |
        """
        if old_address.lower() == 'all':
            old_address = STANDARD_RECIPIENTS_ENTRY

        if not self._is_element_present(RECIPIENT_EDIT_LINK(old_address)):
            raise ValueError('Recipient "%s" is not found inside listener "%s"' % \
                             (address, listener_name))
        self.click_element(RECIPIENT_EDIT_LINK(old_address))
        controller = self._get_recipient_settings_controller()
        controller.set(kwargs)
        self._click_submit_button()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_recipient_delete(self, listener_name, address):
        """Delete existing recipient address from RAT

        *Parameters:*
        - `listener_name`: listener name where this recipient will be deleted,
        mandatory
        - `address`: Recipient Address to be deleted, mandatory

        *Exceptions:*
        - `ValueError`: if no recipient with given address found
        in RAT

        *Examples:*
        | RAT Recipient Delete | InBoundMail | .sma |
        """
        if not self._is_element_present(DELETE_CHECKBOX(address)):
            raise ValueError("'%s' Recipient Address is not found in listener '%s'" % \
                             (address, listener_name))
        self.select_checkbox(DELETE_CHECKBOX(address))
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_clear_all(self, listener_name):
        """Clear all RAT entries for given listener

        *Parameters:*
        - `listener_name`: listener name where all recipients will be deleted,
        mandatory

        *Examples:*
        | RAT Clear All | InBoundMail |
        """
        self.click_button(CLEAR_ALL_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_import(self, listener_name, filename):
        """Import RAT entries from predefined file name on appliance

        *Parameters:*
        - `listener_name`: listener name where all recipients will be imported,
        mandatory
        - `filename`: filename from which entries are imported

        *Exceptions:*
        - `ValueError`: if no file with given name is present on ESA

        *Examples:*
        | RAT Import | InBoundMail | profanity.txt |
        """
        IMPORT_CONFIRM = "//button[text()='Import']"

        self.click_button(IMPORT_BUTTON)
        try:
            self.select_from_list(IMPORT_FILE_DROPBOX, filename)
        except:
            raise ValueError('"s" file has not been found' % (filename,))
        self._click_submit_button(wait=False)
        if self._is_element_present(IMPORT_CONFIRM):
            self.click_button(IMPORT_CONFIRM)
        self._check_action_result()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_export(self, listener_name, filename):
        """Export RAT entries to file

        *Parameters:*
        - `listener_name`: listener name where all recipients will be exported,
        mandatory
        - `filename`: filename to which entries will be imported

        *Examples:*
        | RAT Export | InBoundMail | myrat.txt |
        """
        OVERWRITE_BUTTON = "//button[text()='Overwrite']"

        self.click_button(EXPORT_BUTTON)
        self.input_text(EXPORT_FILE_TEXTBOX, filename)
        self._click_submit_button(wait=False)
        if self._is_element_present(OVERWRITE_BUTTON):
            self.click_button(OVERWRITE_BUTTON)
        self._check_action_result()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_edit_order(self, listener_name, domain_order_dict):
        """Edit order of receiving domain

        *Parameters:*
        - `listener_name`: listener name where order of all recipients will be
        edited, mandatory
        - `domain_order_dict`: dictionary with domain as key and order as value.
        Domain can be 'All' for STANDARD_RECIPIENTS_ENTRY entry

        *Exceptions:*
        - `ValueError`: if no domain with given name is found inside given listener

        *Examples*:
        | ${new_order}= | Create Dictionary | .sma | 1 | .qa | 2 |
        | RAT Edit Order | InBoundMail | ${new_order} |
        """
        self.click_button(EDIT_ORDER_BUTTON)
        for domain in domain_order_dict.iterkeys():
            if domain.upper() == 'ALL':
                domain = STANDARD_RECIPIENTS_ENTRY
            if not self._is_element_present(RECIPIENT_ORDER_EDIT(domain)):
                raise ValueError('Domain "%s" is not found for listener "%s"' % \
                                 (domain, listener))
            self.input_text(RECIPIENT_ORDER_EDIT(domain),
                            domain_order_dict[domain])
        self.click_button("_click")
        self._check_action_result()

    @go_to_access_table(RAT_PAGE_PATH, LISTENER_OPTS)
    def rat_get_all(self, listener_name):
        """Return list of recipients inside given listener

        *Parameters:*
        - `listener_name`: listener name where all recipients will be
        read, mandatory

        *Return:*
        List of dictionaries. Each dictionary has the next items:
        | address | recipient address |
        | action | RAT action for this recipient, either Accept or
        Reject |
        | order | entry order number, acceptable values are in range 1..5 |
        | bypass_ldap_accept | whether LDAP Accept Queries
        for this Recipient (accessible only if corresponding LDAP query
        is configured) are bypassed, either True or False |
        | smtp_response | whether custom SMPT response is enabled or disabled,
        either True or False |
        | smtp_response_code | custom SMTP response code (only if smtp_response is
        set to ${True}), number |
        | smtp_response_text | custom SMTP response text (only if smtp_response is
        set to ${True}), string |
        | bypass | whether Bypass Receiving Control is enabled,
        either True or False |

        *Examples:*
        | ${all_recipients}= | RAT Get All | InBoundMail |
        | ${item0} | Get From List | ${all_recipients} | 0 |
        | ${address} | Get From Dictionary | ${item0} | address |
        | Log | ${address} |
        """
        CANCEL_BUTTON = "//input[@value='Cancel']"

        rows = int(self.get_matching_xpath_count("%s//tr" % (RAT_TABLE,)))
        rat_entries = []
        while rows > 1:
            target_recipient = '%s//tr[%s]//td/a' % (RAT_TABLE, rows)
            self.click_button(target_recipient)
            recipient_details = self._get_recipient_settings_controller().get()
            rat_entries.append(recipient_details)
            rows -= 1
            self.click_button(CANCEL_BUTTON)
        return rat_entries
