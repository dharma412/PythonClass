#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/ldap.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools
import re
import traceback

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from ldap_def.ldap_chained_query import LDAPChainedQuery
from ldap_def.ldap_domain_assignments import LDAPDomainAssignments
from ldap_def.ldap_global_settings import LDAPGlobalSettings
from ldap_def.ldap_profile import LDAPProfile

# Main page
ADD_PROFILE_BTN = "//input[@value='Add LDAP Server Profile...']"
PROFILES_TABLE = "//table[@class='cols']"
EDIT_SETTINGS_BTN = "//input[@value='Edit Settings...']"
FLUSH_CACHE_BTN = "//input[@value='Flush Cache']"
PROFILE_EDIT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                                 (PROFILES_TABLE, name)
PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                   "/following-sibling::td[4]/img" % \
                                   (PROFILES_TABLE, name)
# Profile settings
PROFILE_SETTINGS_ADVANCED_OPENED_LINK = "//div[@id='advancedLinkOpen']"
PROFILE_SETTINGS_ADVANCED_CLOSED_LINK = "//div[@id='advancedLinkClosed']"
CANCEL_BTN = "//input[@value='Cancel']"
TEST_OK_MARK = 'Result: succeeded'
# Advanced section of main page
ADVANCED_LINK = "//div[@id='arrow_closed']"
ADVANCED_SECTION_TABLE = "//table[@id='advanced_section']"
ADD_DOMAIN_ASSIGNMENTS_BTN = "//input[@value='Add Domain Assignments...']"
EDIT_DOMAIN_ASSIGNMENT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                                           (ADVANCED_SECTION_TABLE, name)
DELETE_DOMAIN_ASSIGNMENT_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                             "/following-sibling::td[2]/img" % \
                                             (ADVANCED_SECTION_TABLE, name)
ADD_CHAINED_QUERY_BTN = "//input[@value='Add Chained Query...']"
EDIT_CHAINED_QUERY_LINK = EDIT_DOMAIN_ASSIGNMENT_LINK
DELETE_CHAINED_QUERY_LINK = DELETE_DOMAIN_ASSIGNMENT_LINK

PAGE_PATH = ('System Administration', 'LDAP')


def check_any_ldap_profile_exist(func):
    """Decorator is used for LDAP class methods
    for checking if there is at least one LDAP
    profile

    *Exceptions:*
    - `ConfigError`: if there is no LDAP server profiles configured
    """

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        # if self._is_element_present(ADVANCED_LINK):
        if self._is_visible(ADVANCED_LINK):
            self.click_element(ADVANCED_LINK, "don't wait")
        if not self._is_element_present(ADD_DOMAIN_ASSIGNMENTS_BTN):
            raise guiexceptions.ConfigError('There should be at least ' \
                                            'one LDAP server profile configured')

        return func(self, *args, **kwargs)

    return decorator


class ProfileTestFailed(Exception):
    pass


class QueryTestFailed(Exception):
    pass


class LDAP(GuiCommon):
    """Keywords for interaction with System Administration -> LDAP
    page
    """

    def get_keyword_names(self):
        return ['ldap_add_profile',
                'ldap_edit_profile',
                'ldap_delete_profile',
                'ldap_test_profile',
                'ldap_test_query',

                'ldap_edit_settings',

                'ldap_flush_cache',

                'ldap_add_domain_assignments',
                'ldap_edit_domain_assignments',
                'ldap_delete_domain_assignments',

                'ldap_add_chained_query',
                'ldap_edit_chained_query',
                'ldap_delete_chained_query']

    def _get_profile_controller(self):
        if not hasattr(self, '_ldap_profile_controller'):
            self._ldap_profile_controller = LDAPProfile(self)
        return self._ldap_profile_controller

    def _get_settings_controller(self):
        if not hasattr(self, '_ldap_settings_controller'):
            self._ldap_settings_controller = LDAPGlobalSettings(self)
        return self._ldap_settings_controller

    def _get_domain_assignments_controller(self):
        if not hasattr(self, '_ldap_domain_assignments_controller'):
            self._ldap_domain_assignments_controller = LDAPDomainAssignments(self)
        return self._ldap_domain_assignments_controller

    def _get_chained_query_controller(self):
        if not hasattr(self, '_ldap_chained_query_controller'):
            self._ldap_chained_query_controller = LDAPChainedQuery(self)
        return self._ldap_chained_query_controller

    @go_to_page(PAGE_PATH)
    def ldap_add_profile(self, name, settings, queries={}):
        """Add LDAP server profile

        *Parameters:*
        - `name`: the name of a new LDAP server profile
        - `settings`: LDAP server profile settings.
        This is dictionary whose keys are setting names
        and values are corresponding setting values.
        Valid items are:
        | `LDAP Server Profile Name` | name of the LDAP server profile, mandatory |
        | `Host Name` | LDAP host name, mandatory |
        | `Base DN` | base DN, for example dc=qa19, dc=qa. Mandatory |
        | `Authentication Method` | LDAP auth method, either "Anonymous" or
        "Use Password" |
        | `Username` | user name. Mandatory if `Authentication Method` is set
        to "Use Password" |
        | `Password` | password. Mandatory if `Authentication Method` is set
        to "Use Password" |
        | `Server Type` | type of the LDAP server. Either "Active Directory" or
        "OpenLDAP" or "Unknown or Other" |
        | `Port` | LDAP server port number |
        | `Connection Protocol` | whether to use SSL connection proto, either
        ${True} or ${False} |
        | `Cache TTL` | cache TTL in seconds |
        | `Maximum Retained Cache Entries` | maximum retained cache entries
        number |
        | `Maximum Number of Simultaneous Connections for Each Host` | count
        of connections |
        | `Multiple Host Options` | Either "Load-Balance Connections Among All
        Hosts Listed" or "Failover Connections in the Order Listed" |
        - `queries`: dictionary containing possible LDAP server profile queries.
        Keys are query types and values are corresponding query settings.
        Also, value can be ${True} or ${False} to simply enable/disable
        corresponding query without setting any option.

        Key `Accept Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |

        Key `Routing Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Recipient Email to Rewrite the Envelope Recipient` | name of the
        attribute containing recipient email for rewrite |
        | `Alternative Mailhost Attribute` | name of the attribute containing
        alternative mailhost |
        | `SMTP Call-Ahead Server Attribute` | name of the attribute containing
        SMTP call-ahead server |

        Key `Certificate Authentication Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string, mandatory |
        | `Serial Number` | whether to include 'sn' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Subject` | whether to include 'dn' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Common Name` | whether to include 'cn' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Organization Name` | whether to include 'o' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Organization Unit Name` | whether to include 'ou' certificate attribute
        into this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Country Name` | whether to include 'c' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `Certificate Name` | whether to include 'n' certificate attribute into
        this LDAP query. Either ${True} or ${False}. ${False} by default |
        | `UserID Attribute Name` | LDAP attribute name containing the
        User ID for SMTP authentication ('uid' by default) |

        Key `Masquerade Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Externally Visible Full Email Address Attribute` | externally visible
        full email address attribute |
        | `Replace Friendly Portion of the Original Recipient` | whether to
        replace friendly portion of the original recipient. Either "Yes" or
        "No" |

        Key `Group Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |

        Key `SMTP Authentication Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Authentication Method` | authentication method. Either "Authenticate
        via LDAP BIND" or "Authenticate by fetching the password as an attribute" |
        | `Maximum Number of Simultaneous Connections` | maximum number
        of simultaneous connections. Available only if `Authentication Method` is
        set to "Authenticate via LDAP BIND" |
        | `SMTP Authentication Password Attribute` | SMTP authentication password
        attribute. Available only if `Authentication Method` is set to
        "Authenticate by fetching the password as an attribute" |
        | `Allowance Query String` | SMTP authentication allowance query string |

        Key `External Authentication Queries`. Value can contain items
        | `Name` | query name |
        | `User Accounts Base DN` | user accounts base DN |
        | `User Accounts Query String` | user accounts query string |
        | `Attribute Containing User's Full Name` | attribute containing
        user's full name |
        | `Deny Login to Expired Accounts` | whether to deny login to expired
        accounts. Either ${True} or ${False} |
        | `Group Membership Base DN` | group membership base DN |
        | `Group Membership Query String` | group membership query string |
        | `Member Username Attribute` | member username attribute |
        | `Group Name Attribute` | group name attribute |

        Key `Spam Quarantine End-User Authentication Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Designate as the Active Query` | whether to designate this query as
        the active query. Either ${True} or ${False} |
        | `Email Attribute` | email attribute(s) |

        Key `Spam Quarantine Alias Consolidation Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Designate as the Active Query` | whether to designate this query as
        the active query. Either ${True} or ${False} |
        | `Email Attribute` | email attribute(s) |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Host Name | qa19.qa |
        | ... | Base DN | dc=qa19, dc=qa |
        | ... | Authentication Method | Anonymous |
        | ... | Server Type | OpenLDAP |
        | ... | Port | 389 |
        | ... | Connection Protocol | ${False} |
        | ... | Cache TTL | 900 |
        | ... | Maximum Retained Cache Entries | 10000 |
        | ... | Maximum Number of Simultaneous Connections for Each Host | 10 |
        | ... | Multiple Host Options | Load-Balance Connections Among All Hosts Listed |
        | ${accept_query}= | Create Dictionary |
        | ... | Name | qa19.qa.accept |
        | ... | Query String | (mail={a}) |
        | ${routing_query}= | Create Dictionary |
        | ... | Name | qa19.qa.routing |
        | ... | Query String | (mailLocalAddress={a}) |
        | ... | Recipient Email to Rewrite the Envelope Recipient | mailRoutingAddress |
        | ... | Alternative Mailhost Attribute | mailHost |
        | ${cert_auth_query}= | Create Dictionary |
        | ... | Name | ${LDAP_AUTH_SERVER}.certauth |
        | ... | Query String | (caccn={cn}) |
        | ... | Serial Number | ${True} |
        | ... | Subject | ${True} |
        | ... | Common Name | ${True} |
        | ... | Organization Name | ${True} |
        | ... | Organization Unit Name | ${True} |
        | ... | Country Name | ${True} |
        | ... | Certificate Name | ${True} |
        | ... | UserID Attribute Name | uid |
        | ${masquerade_query}= | Create Dictionary |
        | ... | Name | qa19.qa.masquerade |
        | ... | Query String | (mailRoutingAddress={a}) |
        | ... | Externally Visible Full Email Address Attribute | mailLocalAddress |
        | ... | Replace Friendly Portion of the Original Recipient | Yes |
        | ${group_query}= | Create Dictionary |
        | ... | Name | qa19.qa.group |
        | ... | Query String | (&(objectClass=posixGroup)(cn={g})(memberUid={u})) |
        | ${smtpauth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.smtpauth |
        | ... | Query String | (uid={u}) |
        | ... | Authentication Method | Authenticate by fetching the password as an attribute |
        | ... | SMTP Authentication Password Attribute | userPassword |
        | ${ext_auth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.externalauth |
        | ... | User Accounts Base DN | dc=qa19, dc=qa |
        | ... | User Accounts Query String | (&(objectClass=posixAccount)(uid={u})) |
        | ... | Attribute Containing User\'s Full Name | gecos |
        | ... | Deny Login to Expired Accounts | ${True} |
        | ... | Group Membership Base DN | dc=qa19, dc=qa |
        | ... | Group Membership Query String | (&(objectClass=posixGroup)(memberUid={u})) |
        | ... | Member Username Attribute | memberUid |
        | ... | Group Name Attribute | cn |
        | ${isq_auth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.isq_user_auth |
        | ... | Query String | (uid={u}) |
        | ... | Designate as the Active Query | ${True} |
        | ... | Email Attribute | mail |
        | ${isq_alias_query}= | Create Dictionary |
        | ... | Name | qa19.qa.isq_alias |
        | ... | Query String | (mail={a}) |
        | ... | Designate as the Active Query | ${True} |
        | ... | Email Attribute | mail |
        | ${queries}= | Create Dictionary |
        | ... | Accept Query | ${accept_query} |
        | ... | Routing Query | ${routing_query} |
        | ... | Certificate Authentication Query | ${cert_auth_query} |
        | ... | Masquerade Query | ${masquerade_query} |
        | ... | Group Query | ${group_query} |
        | ... | SMTP Authentication Query | ${smtpauth_query} |
        | ... | External Authentication Queries | ${ext_auth_query} |
        | ... | Spam Quarantine End-User Authentication Query | ${isq_auth_query} |
        | ... | Spam Quarantine Alias Consolidation Query | ${isq_alias_query} |
        | LDAP Add Profile | ${settings} | ${queries} |
        """
        self.click_button(ADD_PROFILE_BTN)
        self.click_element(PROFILE_SETTINGS_ADVANCED_CLOSED_LINK, "don't wait")

        controller = self._get_profile_controller()
        settings.update({'LDAP Server Profile Name': name})
        controller.set(settings, queries)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def ldap_edit_profile(self, name, settings={}, queries={}):
        """Edit existing LDAP server profile

        *Parameters:*
        - `name`: name of existing LDAP server profile to be edited
        - `settings`: LDAP server profile settings.
        This is dictionary whose keys are setting names
        and values are corresponding setting values.
        Valid items are:
        | `LDAP Server Profile Name` | name of the LDAP server profile, mandatory |
        | `Host Name` | LDAP host name, mandatory |
        | `Base DN` | base DN, for example dc=qa19, dc=qa. Mandatory |
        | `Authentication Method` | LDAP auth method, either "Anonymous" or
        "Use Password" |
        | `Username` | user name. Mandatory if `Authentication Method` is set
        to "Use Password" |
        | `Password` | password. Mandatory if `Authentication Method` is set
        to "Use Password" |
        | `Server Type` | type of the LDAP server. Either "Active Directory" or
        "OpenLDAP" or "Unknown or Other" |
        | `Port` | LDAP server port number |
        | `Connection Protocol` | whether to use SSL connection proto, either
        ${True} or ${False} |
        | `Cache TTL` | cache TTL in seconds |
        | `Maximum Retained Cache Entries` | maximum retained cache entries
        number |
        | `Maximum Number of Simultaneous Connections for Each Host` | count
        of connections |
        | `Multiple Host Options` | Either "Load-Balance Connections Among All
        Hosts Listed" or "Failover Connections in the Order Listed" |
        - `queries`: dictionary containing possible LDAP server profile queries.
        Keys are query types and values are corresponding query settings.
        Also, value can be ${True} or ${False} to simply enable/disable
        corresponding query without setting any option.

        Key `Accept Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |

        Key `Routing Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Recipient Email to Rewrite the Envelope Recipient` | name of the
        attribute containing recipient email for rewrite |
        | `Alternative Mailhost Attribute` | name of the attribute containing
        alternative mailhost |
        | `SMTP Call-Ahead Server Attribute` | name of the attribute containing
        SMTP call-ahead server |

        Key `Masquerade Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Externally Visible Full Email Address Attribute` | externally visible
        full email address attribute |
        | `Replace Friendly Portion of the Original Recipient` | whether to
        replace friendly portion of the original recipient. Either "Yes" or
        "No" |

        Key `Group Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |

        Key `SMTP Authentication Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Authentication Method` | authentication method. Either "Authenticate
        via LDAP BIND" or "Authenticate by fetching the password as an attribute" |
        | `Maximum Number of Simultaneous Connections` | maximum number
        of simultaneous connections. Available only if `Authentication Method` is
        set to "Authenticate via LDAP BIND" |
        | `SMTP Authentication Password Attribute` | SMTP authentication password
        attribute. Available only if `Authentication Method` is set to
        "Authenticate by fetching the password as an attribute" |

        Key `External Authentication Queries`. Value can contain items
        | `Name` | query name |
        | `User Accounts Base DN` | user accounts base DN |
        | `User Accounts Query String` | user accounts query string |
        | `Attribute Containing User's Full Name` | attribute containing
        user's full name |
        | `Deny Login to Expired Accounts` | whether to deny login to expired
        accounts. Either ${True} or ${False} |
        | `Group Membership Base DN` | group membership base DN |
        | `Group Membership Query String` | group membership query string |
        | `Member Username Attribute` | member username attribute |
        | `Group Name Attribute` | group name attribute |

        Key `Spam Quarantine End-User Authentication Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Designate as the Active Query` | whether to designate this query as
        the active query. Either ${True} or ${False} |
        | `Email Attribute` | email attribute(s) |

        Key `Spam Quarantine Alias Consolidation Query`. Value can contain items
        | `Name` | query name |
        | `Query String` | LDAP query string |
        | `Designate as the Active Query` | whether to designate this query as
        the active query. Either ${True} or ${False} |
        | `Email Attribute` | email attribute(s) |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct or
        LDAP server profile with given name does not exist

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | LDAP Server Profile Name | qa19.qa |
        | ... | Host Name | qa19.qa |
        | ... | Base DN | dc=qa19, dc=qa |
        | ... | Authentication Method | Anonymous |
        | ... | Server Type | OpenLDAP |
        | ... | Port | 389 |
        | ... | Connection Protocol | ${False} |
        | ... | Cache TTL | 900 |
        | ... | Maximum Retained Cache Entries | 10000 |
        | ... | Maximum Number of Simultaneous Connections for Each Host | 10 |
        | ... | Multiple Host Options | Load-Balance Connections Among All Hosts Listed |
        | ${accept_query}= | Create Dictionary |
        | ... | Name | qa19.qa.accept |
        | ... | Query String | (mail={a}) |
        | ${routing_query}= | Create Dictionary |
        | ... | Name | qa19.qa.routing |
        | ... | Query String | (mailLocalAddress={a}) |
        | ... | Recipient Email to Rewrite the Envelope Recipient | mailRoutingAddress |
        | ... | Alternative Mailhost Attribute | mailHost |
        | ${masquerade_query}= | Create Dictionary |
        | ... | Name | qa19.qa.masquerade |
        | ... | Query String | (mailRoutingAddress={a}) |
        | ... | Externally Visible Full Email Address Attribute | mailLocalAddress |
        | ... | Replace Friendly Portion of the Original Recipient | Yes |
        | ${group_query}= | Create Dictionary |
        | ... | Name | qa19.qa.group |
        | ... | Query String | (&(objectClass=posixGroup)(cn={g})(memberUid={u})) |
        | ${smtpauth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.smtpauth |
        | ... | Query String | (uid={u}) |
        | ... | Authentication Method | Authenticate by fetching the password as an attribute |
        | ... | SMTP Authentication Password Attribute | userPassword |
        | ${ext_auth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.externalauth |
        | ... | User Accounts Base DN | dc=qa19, dc=qa |
        | ... | User Accounts Query String | (&(objectClass=posixAccount)(uid={u})) |
        | ... | Attribute Containing User\'s Full Name | gecos |
        | ... | Deny Login to Expired Accounts | ${True} |
        | ... | Group Membership Base DN | dc=qa19, dc=qa |
        | ... | Group Membership Query String | (&(objectClass=posixGroup)(memberUid={u})) |
        | ... | Member Username Attribute | memberUid |
        | ... | Group Name Attribute | cn |
        | ${isq_auth_query}= | Create Dictionary |
        | ... | Name | qa19.qa.isq_user_auth |
        | ... | Query String | (uid={u}) |
        | ... | Designate as the Active Query | ${True} |
        | ... | Email Attribute | mail |
        | ${isq_alias_query}= | Create Dictionary |
        | ... | Name | qa19.qa.isq_alias |
        | ... | Query String | (mail={a}) |
        | ... | Designate as the Active Query | ${True} |
        | ... | Email Attribute | mail |
        | ${queries}= | Create Dictionary |
        | ... | Accept Query | ${accept_query} |
        | ... | Routing Query | ${routing_query} |
        | ... | Masquerade Query | ${masquerade_query} |
        | ... | Group Query | ${group_query} |
        | ... | SMTP Authentication Query | ${smtpauth_query} |
        | ... | External Authentication Queries | ${ext_auth_query} |
        | ... | Spam Quarantine End-User Authentication Query | ${isq_auth_query} |
        | ... | Spam Quarantine Alias Consolidation Query | ${isq_alias_query} |
        | LDAP Edit Profile | my_profile | ${settings} | ${queries} |
        """
        if self._is_element_present(PROFILE_EDIT_LINK(name)):
            self.click_link(PROFILE_EDIT_LINK(name))
            if self._is_visible(PROFILE_SETTINGS_ADVANCED_CLOSED_LINK):
                self.click_element(PROFILE_SETTINGS_ADVANCED_CLOSED_LINK, "don't wait")
        else:
            raise ValueError('There is no LDAP server profile ' \
                             'named "%s"' % (name,))

        controller = self._get_profile_controller()
        controller.set(settings, queries)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def ldap_delete_profile(self, name):
        """Delete existing LDAP server profile

        *Parameters:*
        - `name`: the name of existing LDAP server profile

        *Exceptions:*
        - `ValueError`: if there is no LDAP server profile with
        given name

        *Examples:*
        | LDAP Delete Profile | my_profile |
        """
        if self._is_element_present(PROFILE_DELETE_LINK(name)):
            self.click_element(PROFILE_DELETE_LINK(name), 'don\'t wait')
        else:
            raise ValueError('There is no LDAP server profile ' \
                             'named "%s"' % (name,))
        self._click_continue_button('Delete')

    @go_to_page(PAGE_PATH)
    def ldap_test_profile(self, name, should_raise_exception=False):
        """Test given LDAP server profile

        *Parameters:*
        - `name`: existing LDAP server profile name
        - `should_raise_exception`: whether to raise an exception if
        profile test was unsuccessful, either ${True} or ${False}

        *Exceptions:*
        - `ValueError`: if LDAP server profile with given name does not exist
        - `ProfileTestFailed`: if should_raise_exception is set to True and
        the test was failed

        *Return:*
        True or False depending on the testing result and  should_raise_exception
        setting

        *Examples:*
        | ${test_result}= | LDAP Test Profile | my_ldap_profile |
        # This will raise an exception if failed:
        | LDAP Test Profile | my_ldap_profile | ${True } |
        """
        if self._is_element_present(PROFILE_EDIT_LINK(name)):
            self.click_link(PROFILE_EDIT_LINK(name))
        else:
            raise ValueError('There is no LDAP server profile ' \
                             'named "%s"' % (name,))

        controller = self._get_profile_controller()
        txt_result = ''
        try:
            txt_result = controller.get_test_result()
        except Exception as e:
            traceback.print_exc()
        if should_raise_exception and txt_result.find(TEST_OK_MARK) < 0:
            raise ProfileTestFailed('LDAP server profile "%s" test ' \
                                    'has failed' % (name,))
        return (txt_result.find(TEST_OK_MARK) >= 0)

    @go_to_page(PAGE_PATH)
    def ldap_test_query(self, profile_name,
                        query_name,
                        settings,
                        should_raise_exception=False):
        """Test given LDAP server profile's query

        *Parameters:*
        - `profile_name`: existing LDAP server profile name
        - `query_name`: existing LDAP query name in this profile
        - `should_raise_exception`: whether to raise an exception if
        query test was unsuccessful, either ${True} or ${False}
        - `settings`: dictionary containing query test parameters.

        By default every query dialog will have same settings you specified
        while creating LDAP profile by `LDAP Add Profile` keyword.

        There are different setting depending on the given query type:

        *SMTP Authentication Query*:

        | `Query String` | LDAP query string |
        | `Authentication Method` | authentication method. Either "Authenticate
        via LDAP BIND" or "Authenticate by fetching the password as an attribute" |
        | `Maximum Number of Simultaneous Connections` | maximum number
        of simultaneous connections. Available only if `Authentication Method` is
        set to "Authenticate via LDAP BIND" |
        | `SMTP Authentication Password Attribute` | SMTP authentication password
        attribute. Available only if `Authentication Method` is set to
        "Authenticate by fetching the password as an attribute" |
        | `Allowance Query String` | SMTP authentication allowance query string |
        | `User Identity` | LDAP user identity |
        | `SMTP Authentication Password` | SMTP Authentication Password for the
        given user identity |

        *Certificate Authentication Query*

        | `Serial Number` | serial number string. |
        | `Subject` | subject string. |
        | `Common Name` | common name string. |
        | `Organization Name` | organization name string. |
        | `Organization Unit Name` | organization unit name string. |
        | `Country Name` | country name string. |
        | `Certificate Name` | certificate name string. |
        | `LDAP Query String` | LDAP query string. |
        | `UserID Attribute Name` | User ID for SMTP authentication string. |

        *Spam Quarantine End-User Authentication Query*

        | `Query String` | LDAP query string. |
        | `Email Attributes` | email attributes. |
        | `User Login` | LDAP user login. |
        | `User Password` | LDAP user password. |

        *OTHER QUERY TESTS ARE NOT IMPLEMENTED YET*


        *Exceptions:*
        - `ValueError`: if LDAP server profile with given name does not exist
        - `ConfigError`: if query with given name was not enabled before test
        - `QueryTestFailed`: if should_raise_exception is set to True and
        the test was failed

        *Return:*
        True or False depending on the testing result and `should_raise_exception`
        setting

        *Examples:*
        | ${test_result}= | LDAP Test Query | my_ldap_profile |
        | ... | Accept Query |
        # This will raise an exception if failed:
        | LDAP Test Profile | my_ldap_profile |
        | ... | Routing Query | ${True } |
        """
        if self._is_element_present(PROFILE_EDIT_LINK(profile_name)):
            self.click_link(PROFILE_EDIT_LINK(profile_name))
        else:
            raise ValueError('There is no LDAP server profile ' \
                             'named "%s"' % (profile_name,))

        controller = self._get_profile_controller()
        txt_result = ''
        try:
            txt_result = controller.get_query_test_result(query_name,
                                                          settings)
            self._info('"%s" testing result:\n%s' % (query_name,
                                                     txt_result))
        except Exception as e:
            traceback.print_exc()
        is_test_successfull = bool(re.search(r'\bSuccess\b', txt_result))
        if should_raise_exception and not is_test_successfull:
            raise QueryTestFailed('The test of "%s" LDAP query, which belongs '
                                  'to server profile "%s", has failed. ' \
                                  'Test result:\n%s' % \
                                  (query_name, profile_name, txt_result))
        return is_test_successfull

    @go_to_page(PAGE_PATH)
    def ldap_edit_settings(self, **kwargs):
        """Edit global LDAP settings

        *Parameters:*
        - `interface`: interface for LDAP traffic. Can be "Auto"
        for automatic interface selection
        - `certificate`: name of certificate used in settings

        *Examples:*
        | LDAP Edit Settings | interface=Auto | certificate=System Default |
        """
        self.click_button(EDIT_SETTINGS_BTN)

        # kwargs = self._parse_args(args)
        settings_controller = self._get_settings_controller()
        settings_controller.set(kwargs)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def ldap_flush_cache(self):
        """Flush LDAP cache

        *Examples*
        | LDAP Flush Cache |
        """
        self.click_button(FLUSH_CACHE_BTN, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_add_domain_assignments(self, name, new_settings):
        """Add LDAP domain assignment

        *Parameters:*
        - `name`: the name of new domain assignment profile
        - `new_settings`: dictionary whose items are corresponding
        Domain Assignment profile settings:
        | `Query Type` | query type string, mandatory. Either
        "Accept" , "Routing", "Masquerade", "Group",
        "SMTP Authentication", "Spam Quarantine End-User Authentication",
        "Spam Quarantine Alias Consolidation" |
        | `Domain Assignments` | dictionary containing domain
        assignments pairs. Dictionary items are string meaning domain
        or partial domain and values are corresponding query name
        assessments |
        | `Default Query` | one of the query named to be default |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | ${assignments}= | Create Dictionary |
        | ... | .qa | qa19.qa.accept |
        | ... | .sma | qa19.qa.accept |
        | ${settings}= | Create Dictionary |
        | ... | Query Type | Accept |
        | ... | Domain Assignments | ${assignments} |
        | LDAP Add Domain Assignments | my_assignments |
        | ... | ${settings} |
        """
        self.click_button(ADD_DOMAIN_ASSIGNMENTS_BTN)

        controller = self._get_domain_assignments_controller()
        new_settings.update({'Query Name': name})
        controller.set(new_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_edit_domain_assignments(self, name, settings={}):
        """Edit LDAP domain assignment

        *Parameters:*
        - `name`: the name of existing domain assignment profile
        - `new_settings`: dictionary whose items are corresponding
        Domain Assignment profile settings:
        | `Domain Assignments` | dictionary containing domain
        assignments pairs. Dictionary items are string meaning domain
        or partial domain and values are corresponding query name
        assessments |
        | `Default Query` | one of the query named to be default |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        or domain assignment with given name does not exist
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | ${assignments}= | Create Dictionary |
        | ... | .qa | qa19.qa.accept |
        | ... | .sma | qa19.qa.accept |
        | ${settings}= | Create Dictionary |
        | ... | Domain Assignments | ${assignments} |
        | LDAP Edit Domain Assignments | my_assignments |
        | ... | ${settings} |
        """
        if self._is_element_present(EDIT_DOMAIN_ASSIGNMENT_LINK(name)):
            self.click_link(EDIT_DOMAIN_ASSIGNMENT_LINK(name))
        else:
            raise ValueError('There is no domain assignment profile ' \
                             'named "%s"' % (name,))

        controller = self._get_domain_assignments_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_delete_domain_assignments(self, name):
        """Delete LDAP domain assignment

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        or domain assignment with given name does not exist
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | LDAP Delete Domain Assignments | my_assignments |
        """
        if self._is_element_present(DELETE_DOMAIN_ASSIGNMENT_LINK(name)):
            self.click_element(DELETE_DOMAIN_ASSIGNMENT_LINK(name), "don't wait")
        else:
            raise ValueError('There is no domain assignment profile ' \
                             'named "%s"' % (name,))
        self._click_continue_button('Delete')

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_add_chained_query(self, name, new_settings):
        """Add LDAP chained query

        *Parameters:*
        - `name`: the name of new chained query profile
        - `new_settings`: dictionary whose items are corresponding
        chained query profile settings:
        | `Query Name` | query name string |
        | `Query Type` | query type string. Either
        "Accept" , "Routing", "Masquerade", "Group",
        "SMTP Authentication", "Spam Quarantine End-User Authentication",
        "Spam Quarantine Alias Consolidation" |
        | `Chained Query` | list containing chained query order.
        List items are query names |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | ${query}= | Create List |
        | ... | qa19.qa.accept |
        | ... | sully.qa.accept |
        | ${settings}= | Create Dictionary |
        | ... | Query Type | Accept |
        | ... | Chained Query | ${query} |
        | LDAP Add Chained Query | my_chained_query |
        | ... | ${settings} |
        """
        self.click_button(ADD_CHAINED_QUERY_BTN)

        controller = self._get_chained_query_controller()
        new_settings.update({'Query Name': name})
        controller.set(new_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_edit_chained_query(self, name, settings={}):
        """Edit LDAP chained query

        *Parameters:*
        - `name`: the name of existing chained query profile
        - `settings`: dictionary whose items are corresponding
        chained query profile settings:
        | `Chained Query` | list containing chained query order.
        List items are query names |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        or chained query with given name does not exist
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | ${query}= | Create List |
        | ... | qa19.qa.accept |
        | ... | sully.qa.accept |
        | ${settings}= | Create Dictionary |
        | ... | Chained Query | ${query} |
        | LDAP Edit Chained Query | my_chained_query |
        | ... | ${settings} |
        """
        if self._is_element_present(EDIT_CHAINED_QUERY_LINK(name)):
            self.click_link(EDIT_CHAINED_QUERY_LINK(name))
        else:
            raise ValueError('There is no chained query profile ' \
                             'named "%s"' % (name,))

        controller = self._get_chained_query_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    @check_any_ldap_profile_exist
    def ldap_delete_chained_query(self, name):
        """Delete LDAP chained query

        *Parameters:*
        - `name`: the name of existing chained query profile

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        or chained query with given name does not exist
        - `ConfigError`: if there are no LDAP server profiles
        configured

        *Examples:*
        | LDAP Delete Chained Query | my_chained_query |
        """
        if self._is_element_present(DELETE_CHAINED_QUERY_LINK(name)):
            self.click_element(DELETE_CHAINED_QUERY_LINK(name), "don't wait")
        else:
            raise ValueError('There is no chained query profile ' \
                             'named "%s"' % (name,))
        self._click_continue_button('Delete')
