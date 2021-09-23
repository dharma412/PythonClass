#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/ldap_def/ldap_queries.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import inspect
import os
import sys

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import Wait
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

from ldap_query_test import get_query_test_dialog_class_by_type

TEST_QUERY_FINISHED_MARK = 'Action: match'
TEST_QUERY_BTN = lambda query_id: \
    "//input[@id='{0}_testbtn']".format(query_id)
TEST_QUERY_RUN_BTN = lambda query_id: \
    "//input[@id='test_{0}_start']".format(query_id)
TEST_QUERY_RESULTS_DIV = lambda query_id: \
    "//div[@id='{0}_test_results']".format(query_id)
TEST_QUERY_CANCEL_BTN = lambda query_id: \
    "{0}/following::button[normalize-space()='Cancel']".format(
        TEST_QUERY_RESULTS_DIV(query_id))
TEST_QUERY_DIALOG = \
    "//div[@id='test_panel_c' and contains(@style, 'visibility: visible')]"
TEST_QUERY_DIALOG_TIMEOUT = 5


def get_all_query_classes():
    base_class = LDAPQuery
    return [v for k, v in inspect.getmembers(sys.modules[__name__]) \
            if inspect.isclass(v) and issubclass(v, base_class) and v != base_class]


def get_query_class_by_name(query_type):
    """Return LDAPQuery descendant class by its name
    received from get_type classmethod

    *Parameters:*
    - `query_type`: the name of existing LDAPQuery descendant

    *Return*
    Searched class or None if nothing is found
    """
    all_subclasses = get_all_query_classes()
    searched_class = filter(lambda x: x.get_type() == query_type, all_subclasses)
    if searched_class:
        return searched_class[0]


class LDAPQuery(InputsOwner):
    NAME_CAPTION = 'Name'
    QUERY_CAPTION = 'Query String'

    def _get_registered_inputs(self):
        all_pairs = get_object_inputs_pairs(self)
        all_pairs.extend([(self.NAME_CAPTION, self._get_name_locator()),
                          (self.QUERY_CAPTION, self._get_query_locator())])
        return all_pairs

    def _get_common_elements_id(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_test_button_locator(self):
        return "//input[@id='%s_testbtn']" % (self._get_common_elements_id(),)

    def _get_main_checkbox_locator(self):
        return "//input[@id='%s_enable']" % (self._get_common_elements_id(),)

    def _get_name_locator(self):
        return "//input[@id='%s_queryname']" % (self._get_common_elements_id(),)

    def _get_query_locator(self):
        return "//input[@id='%s_query']" % (self._get_common_elements_id(),)

    @classmethod
    def get_type(cls):
        raise NotImplementedError('Should be implemented in subclasses')

    def enable(self):
        self.gui._select_checkbox(self._get_main_checkbox_locator())

    def disable(self):
        self.gui._unselect_checkbox(self._get_main_checkbox_locator())

    def is_enabled(self):
        return self.gui._is_checked(self._get_main_checkbox_locator())

    def set(self, new_value):
        if not self.is_enabled():
            self.enable()

        self._set_edits(new_value,
                        (self.NAME_CAPTION,
                         self._get_name_locator()),
                        (self.QUERY_CAPTION,
                         self._get_query_locator()))

    def get(self):
        if not self.is_enabled():
            raise guiexceptions.ConfigError('The "%s" must be enabled before get' \
                                            ' its settings' % (self.get_type(),))
        details = {}
        details[self.NAME_CAPTION] = self.gui.get_value(self._get_name_locator())
        return details

    def get_test_result(self, settings):
        """Return test result

        *Exceptions:*
        - `TimeoutError`: if test result is not received within 60
        seconds timeout
        - `ConfigError`: if corresponding query was not enabled before

        *Return:*
        Test result string
        """
        if not self.is_enabled():
            raise guiexceptions.ConfigError('The "%s" must be enabled before test' % \
                                            (self.get_type(),))

        controller_class = get_query_test_dialog_class_by_type(self.get_type())
        if controller_class is None:
            raise NotImplementedError('The keyword is not implemented for LDAP ' \
                                      'query "%s"' % (self.get_type(),))
        query_id = self._get_common_elements_id()
        self.gui.click_button(TEST_QUERY_BTN(query_id), 'don\'t wait')
        Wait(until=self.gui._is_element_present,
             msg='Failed to detect Test Query dialog within 5 second',
             timeout=TEST_QUERY_DIALOG_TIMEOUT).wait(TEST_QUERY_DIALOG)
        controller = controller_class(self.gui)
        controller.set(settings)

        TIMEOUT = 60
        self.gui.click_button(TEST_QUERY_RUN_BTN(query_id), 'don\'t wait')
        self.gui.wait_until_page_contains(TEST_QUERY_FINISHED_MARK,
                                          TIMEOUT)
        result = self.gui.get_text(TEST_QUERY_RESULTS_DIV(query_id))
        self.gui.click_button(TEST_QUERY_CANCEL_BTN(query_id), 'don\'t wait')
        return result


class AcceptQuery(LDAPQuery):
    @classmethod
    def get_type(cls):
        return 'Accept Query'

    def _get_common_elements_id(self):
        return 'rat'

    def set(self, new_value):
        super(AcceptQuery, self).set(new_value)


class RoutingQuery(LDAPQuery):
    RECIPIENT_EMAIL = ('Recipient Email to Rewrite the Envelope Recipient',
                       "//input[@id='routing_address']")
    ALTERNATIVE_MAILHOST_ATTR = ('Alternative Mailhost Attribute',
                                 "//input[@id='routing_mailhost']")
    CALLAHEAD_HOST = ('SMTP Call-Ahead Server Attribute',
                      "//input[@id='callaheadhost']")

    @classmethod
    def get_type(cls):
        return 'Routing Query'

    def _get_common_elements_id(self):
        return 'reroute'

    def set(self, new_value):
        super(RoutingQuery, self).set(new_value)

        self._set_edits(new_value,
                        self.RECIPIENT_EMAIL,
                        self.ALTERNATIVE_MAILHOST_ATTR,
                        self.CALLAHEAD_HOST)


class CertificateAuthenticationQuery(LDAPQuery):
    SERIAL_NUMBER_CHECKBOX = ('Serial Number',
                              "//input[@name='certauth_query_sub[]' and @value='sn']")
    SUBJECT_CHECKBOX = ('Subject',
                        "//input[@name='certauth_query_sub[]' and @value='dn']")
    COMMON_NAME_CHECKBOX = ('Common Name',
                            "//input[@name='certauth_query_sub[]' and @value='cn']")
    ORGANIZATION_NAME_CHECKBOX = ('Organization Name',
                                  "//input[@name='certauth_query_sub[]' and @value='o']")
    ORGANIZATION_UNIT_NAME_CHECKBOX = ('Organization Unit Name',
                                       "//input[@name='certauth_query_sub[]' and @value='ou']")
    COUNTRY_NAME_CHECKBOX = ('Country Name',
                             "//input[@name='certauth_query_sub[]' and @value='c']")
    CERTIFICATE_NAME_CHECKBOX = ('Certificate Name',
                                 "//input[@name='certauth_query_sub[]' and @value='n']")
    USER_ID_ATTRIBUTE_NAME = ('UserID Attribute Name',
                              "//input[@id='certauth_user_id_attr']")

    @classmethod
    def get_type(cls):
        return 'Certificate Authentication Query'

    def _get_common_elements_id(self):
        return 'certauth'

    def set(self, new_value):
        super(CertificateAuthenticationQuery, self).set(new_value)

        self._set_checkboxes(new_value,
                             self.SERIAL_NUMBER_CHECKBOX,
                             self.SUBJECT_CHECKBOX,
                             self.COMMON_NAME_CHECKBOX,
                             self.ORGANIZATION_NAME_CHECKBOX,
                             self.ORGANIZATION_UNIT_NAME_CHECKBOX,
                             self.COUNTRY_NAME_CHECKBOX,
                             self.CERTIFICATE_NAME_CHECKBOX)
        self._set_edits(new_value,
                        self.USER_ID_ATTRIBUTE_NAME)


class MasqueradeQuery(LDAPQuery):
    LOCAL_MAILADDR = ('Externally Visible Full Email Address Attribute',
                      "//input[@id='maillocaladdress']")

    LOCAL_MAILADDR_FRIENDLY_RADIO_GROUP = ('Replace Friendly Portion of the ' \
                                           'Original Recipient',
                                           {'Yes': "//input[@id='maillocaladdressfriendly_yes']",
                                            'No': "//input[@id='maillocaladdressfriendly_no']"})

    @classmethod
    def get_type(cls):
        return 'Masquerade Query'

    def _get_common_elements_id(self):
        return 'masquerade'

    def set(self, new_value):
        super(MasqueradeQuery, self).set(new_value)

        self._set_edits(new_value, self.LOCAL_MAILADDR)
        self._set_radio_groups(new_value,
                               self.LOCAL_MAILADDR_FRIENDLY_RADIO_GROUP)


class GroupQuery(LDAPQuery):
    @classmethod
    def get_type(cls):
        return 'Group Query'

    def _get_common_elements_id(self):
        return 'group'

    def set(self, new_value):
        super(GroupQuery, self).set(new_value)


class SMTPAuthenticationQuery(LDAPQuery):
    AUTH_METHOD_RADIO_GROUP = ('Authentication Method',
                               {'Authenticate via LDAP BIND': \
                                    "//input[@id='smtpauth_query_bind']",
                                'Authenticate by fetching the password ' \
                                'as an attribute': \
                                    "//input[@id='smtpauth_query_default']"})
    MAX_NUMBER_OF_SIMUL_CONN = ('Maximum Number of Simultaneous Connections',
                                "//input[@id='smtpauth_query_max_connections']")
    PASSWD_ATTRIB_NAME = ('SMTP Authentication Password Attribute',
                          "//input[@id='smtpauth_pass_attr']")
    ALLOWANCE_QUERY_STRING = ('Allowance Query String',
                              "//input[@id='smtpauth_allowance']")

    @classmethod
    def get_type(cls):
        return 'SMTP Authentication Query'

    def _get_common_elements_id(self):
        return 'smtpauth'

    def set(self, new_value):
        super(SMTPAuthenticationQuery, self).set(new_value)

        self._set_radio_groups(new_value, self.AUTH_METHOD_RADIO_GROUP)
        self._set_edits(new_value,
                        self.MAX_NUMBER_OF_SIMUL_CONN,
                        self.PASSWD_ATTRIB_NAME,
                        self.ALLOWANCE_QUERY_STRING)


class ExternalAuthenticationQueries(LDAPQuery):
    # User Accounts
    ACCOUNT_BASE = ('User Accounts Base DN',
                    "//input[@id='externalauth_account_base']")
    ACCOUNT_QUERY = ('User Accounts Query String',
                     "//input[@id='externalauth_user_query']")
    ACCOUNT_FULL_NAME_ATTRIB = ('Attribute Containing User\'s Full Name',
                                "//input[@id='externalauth_gecos_attribute']")
    ACCOUNT_DENY_LOGIN_TO_EXPIRED_CHECKBOX = ('Deny Login to Expired Accounts',
                                              "//input[@id='externalauth_deny_login']")
    # Group Membership
    GROUP_BASE = ('Group Membership Base DN',
                  "//input[@id='externalauth_group_base']")
    GROUP_QUERY = ('Group Membership Query String',
                   "//input[@id='externalauth_membership_query']")
    GROUP_MEMBER_ATTRIB = ('Member Username Attribute',
                           "//input[@id='externalauth_member_attribute']")
    GROUP_NAME_ATTRIB = ('Group Name Attribute',
                         "//input[@id='externalauth_group_name_attribute']")

    @classmethod
    def get_type(cls):
        return 'External Authentication Queries'

    def _get_common_elements_id(self):
        return 'externalauth'

    def set(self, new_value):
        if not self.is_enabled():
            self.enable()

        self._set_edits(new_value,
                        (self.NAME_CAPTION,
                         self._get_name_locator()),
                        self.ACCOUNT_BASE,
                        self.ACCOUNT_QUERY,
                        self.ACCOUNT_FULL_NAME_ATTRIB,
                        self.GROUP_BASE,
                        self.GROUP_QUERY,
                        self.GROUP_MEMBER_ATTRIB,
                        self.GROUP_NAME_ATTRIB)
        self._set_checkboxes(new_value,
                             self.ACCOUNT_DENY_LOGIN_TO_EXPIRED_CHECKBOX)


class SpamQuarantineEndUserAuthQuery(LDAPQuery):
    DESIGNATE_AS_ACTIVE_CHECKBOX = ('Designate as the Active Query',
                                    "//input[@id='isqauth_active']")
    EMAIL_ATTRIB = ('Email Attribute',
                    "//input[@id='isqauth_mailattr']")

    @classmethod
    def get_type(cls):
        return 'Spam Quarantine End-User Authentication Query'

    def _get_common_elements_id(self):
        return 'isqauth'

    def set(self, new_value):
        super(SpamQuarantineEndUserAuthQuery, self).set(new_value)

        self._set_checkboxes(new_value,
                             self.DESIGNATE_AS_ACTIVE_CHECKBOX)
        self._set_edits(new_value, self.EMAIL_ATTRIB)


class SpamQuarantineAliasConsolidationQuery(LDAPQuery):
    DESIGNATE_AS_ACTIVE_CHECKBOX = ('Designate as the Active Query',
                                    "//input[@id='primaryaddress_active']")
    EMAIL_ATTRIB = ('Email Attribute',
                    "//input[@id='primaryaddress_mailattr']")

    @classmethod
    def get_type(cls):
        return 'Spam Quarantine Alias Consolidation Query'

    def _get_common_elements_id(self):
        return 'primaryaddress'

    def set(self, new_value):
        super(SpamQuarantineAliasConsolidationQuery, self).set(new_value)

        self._set_checkboxes(new_value,
                             self.DESIGNATE_AS_ACTIVE_CHECKBOX)
        self._set_edits(new_value, self.EMAIL_ATTRIB)
