#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/ldap_def/ldap_query_test.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import inspect
import sys

from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs


def get_all_query_classes():
    base_class = LdapQueryTest
    return [v for k, v in inspect.getmembers(sys.modules[__name__]) \
            if inspect.isclass(v) and issubclass(v, base_class) and v != base_class]


def get_query_test_dialog_class_by_type(query_type):
    all_subclasses = get_all_query_classes()
    searched_class = filter(lambda x: x.get_parent_query_type() == query_type,
                            all_subclasses)
    if searched_class:
        return searched_class[0]


class LdapQueryTest(InputsOwner):
    @classmethod
    def get_parent_query_type(cls):
        """*Return:*
        The type of connected LDAP Query class, string
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)


class SMTPAuthenticationQueryTest(LdapQueryTest):
    QUERY_STRING = ('Query String',
                    "//input[@id='test_smtpauth_query']")
    AUTH_METHOD_RADIOGROUP = ('Authentication Method',
                              {'Authenticate via LDAP BIND': \
                                   "//input[@id='test_smtpauth_query_bind']",
                               'Authenticate by fetching the password as an attribute': \
                                   "//input[@id='test_smtpauth_query_default']"})
    MAX_CONNECTIONS = ('Maximum Number of Simultaneous Connections',
                       "//input[@id='test_smtpauth_query_max_connections']")
    PASSWORD_ATTRIB = ('SMTP Authentication Password Attribute',
                       "//input[@id='test_smtpauth_pass_attr']")
    ALLOWANCE_QUERY = ('Allowance Query String',
                       "//input[@id='test_smtpauth_allowance']")
    USER_IDENTITY = ('User Identity',
                     "//input[@id='test_smtpauth_user']")
    SMTP_AUTH_PASSWORD = ('SMTP Authentication Password',
                          "//input[@id='test_smtpauth_pass']")

    @classmethod
    def get_parent_query_type(cls):
        return 'SMTP Authentication Query'

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.AUTH_METHOD_RADIOGROUP)
        self._set_edits(new_value,
                        self.QUERY_STRING,
                        self.MAX_CONNECTIONS,
                        self.PASSWORD_ATTRIB,
                        self.ALLOWANCE_QUERY,
                        self.USER_IDENTITY,
                        self.SMTP_AUTH_PASSWORD)


class CertificateAuthenticationQuery(LdapQueryTest):
    SERIAL_NUMBER = ('Serial Number',
                     "//input[@id='test_certauth_subst_for_sn']")
    SUBJECT = ('Subject', "//input[@id='test_certauth_subst_for_dn']")
    COMMON_NAME = ('Common Name',
                   "//input[@id='test_certauth_subst_for_cn']")
    ORGANIZATION_NAME = ('Organization Name',
                         "//input[@id='test_certauth_subst_for_o']")
    ORGANIZATION_UNIT_NAME = ('Organization Unit Name',
                              "//input[@id='test_certauth_subst_for_ou']")
    COUNTRY_NAME = ('Country Name',
                    "//input[@id='test_certauth_subst_for_c']")
    CERTIFICATE_NAME = ('Certificate Name',
                        "//input[@id='test_certauth_subst_for_n']")
    QUERY_STRING = ('LDAP Query String', "//input[@id='test_certauth_query']")
    USER_ID_ATTRIBUTE_NAME = ('UserID Attribute Name',
                              "//input[@id='test_certauth_user_id_attr']")

    @classmethod
    def get_parent_query_type(cls):
        return 'Certificate Authentication Query'

    def set(self, new_value):
        self._set_edits(new_value,
                        self.SERIAL_NUMBER,
                        self.SUBJECT,
                        self.COMMON_NAME,
                        self.ORGANIZATION_NAME,
                        self.ORGANIZATION_UNIT_NAME,
                        self.COUNTRY_NAME,
                        self.CERTIFICATE_NAME,
                        self.QUERY_STRING,
                        self.USER_ID_ATTRIBUTE_NAME)


class SpamQuarantineEndUserAuthQuery(LdapQueryTest):
    QUERY_STRING = ('Query String', "//input[@id='test_isqauth_query']")
    EMAIL_ATTRIBUTES = ('Email Attributes',
                        "//input[@id='test_isqauth_mailattr']")
    USER_LOGIN = ('User Login', "//input[@id='test_isqauth_user']")
    USER_PASSWORD = ('User Password', "//input[@id='test_isqauth_pass']")

    @classmethod
    def get_parent_query_type(cls):
        return 'Spam Quarantine End-User Authentication Query'

    def set(self, new_value):
        self._set_edits(new_value,
                        self.QUERY_STRING,
                        self.EMAIL_ATTRIBUTES,
                        self.USER_LOGIN,
                        self.USER_PASSWORD)
