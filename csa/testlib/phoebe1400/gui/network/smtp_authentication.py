#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/network/smtp_authentication.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $
import time

from common.gui.decorators import go_to_page, set_speed
from common.gui.guiexceptions import ConfigError
from common.gui.guicommon import GuiCommon

from smtp_authentication_def.certificate_profile_settings import CertificateProfileAddSettings
from smtp_authentication_def.forward_profile_settings import ForwardProfileAddSettings
from smtp_authentication_def.ldap_profile_settings import LDAPProfileAddSettings
from smtp_authentication_def.outgoing_profile_settings import OutgoingProfileAddSettings


ADD_PROFILE_BUTTON = "//input[@value='Add Profile...']"
PROFILES_TABLE = "//table[@class='cols']"
PROFILE_NAME_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                        (PROFILES_TABLE, name)
PROFILE_NAMES = "%s//tr[td]" % (PROFILES_TABLE,)
PROFILE_NAME_BY_IDX = lambda idx: "xpath=(%s)[%d]/td" % (PROFILE_NAMES, idx)
PROFILE_TYPE_BY_IDX = lambda idx: "xpath=(%s)[%d]/td[2]" % (PROFILE_NAMES, idx)
PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']"\
               "/following-sibling::td[2]/img" % (PROFILES_TABLE, name)
CLEAR_ALL_BUTTON = "//input[@value='Clear All Profiles']"


PAGE_PATH = ('Network', 'SMTP Authentication')

PROFILE_ADD_CLASS_MAPPING = {'outgoing': OutgoingProfileAddSettings,
                             'forward': ForwardProfileAddSettings,
                             'ldap': LDAPProfileAddSettings,
                             'certificate': CertificateProfileAddSettings}

class SMTPAuthentication(GuiCommon):
    """Keywords for GUI interaction with Network -> SMTP Authentication
    page"""

    def get_keyword_names(self):
        return ['smtp_authentication_add_profile',
                'smtp_authentication_edit_profile',
                'smtp_authentication_delete_profile',
                'smtp_authentication_is_profile_exist',

                'smtp_authentication_get_all_profiles']

    def _get_profile_add_settings_controller(self, profile_type):
        profile_type = profile_type.lower()
        if profile_type not in PROFILE_ADD_CLASS_MAPPING:
            raise ValueError('Unknown profile type "%s". '\
                             'Available profile types are %s' % \
                             (profile_type, PROFILE_ADD_CLASS_MAPPING.keys()))
        attr_name = '_%s_profile_add_settings_controller' % (profile_type,)
        if not hasattr(self, attr_name):
            setattr(self, attr_name,
                    PROFILE_ADD_CLASS_MAPPING[profile_type](self))
        return getattr(self, attr_name)

    @go_to_page(PAGE_PATH)
    def smtp_authentication_add_profile(self, profile_name, profile_type,
                                        settings):
        """Add new SMTP authentication profile

        *Parameters:*
        - `profile_name`: the name of profile to be added
        - `profile_type`: profile type. Can be one of:
        | Outgoing |
        | Forward |
        | LDAP |
        | Certificate |
        - `settings`: dictionary containing new profile settings. Depending
        on profile type the following settings are available:

        *Outgoing:*
        | Authentication Username | usrname for outgoing SMTP auth, mandatory |
        | Authentication Password | password for outgoing SMTP auth, mandatory |

        *Forward:*
        | Hostname | hostname or IP address of remote host, mandatory |
        | Port | port number on remote host, 25 by default |
        | Interface | ESA interface name to be used for connection, 'Auto' by default |
        | Maximum Simultaneous Connections | number of simultaneous connections |
        | Require TLS | whether to require secure TLS connection, ${True} by default |
        | Use SASL LOGIN mechanism | whether to use SASL LOGIN mechanism, ${True} by default |
        | Use SASL PLAIN mechanism | whether to use SASL PLAIN mechanism, ${True} by default |

        *LDAP:*
        | LDAP Query | name of existing SMTP Authentication LDAP query |
        | Default Encryption Method | possible values are: None (by default), Plain, SHA,
        Salted SHA, Crypt, MD5 |
        | Check with LDAP if user is allowed to use SMTP AUTH | whether to check
        if user is allowed to use SMTP AUTH mechanism, ${False} by default |
        | If user is found to be not allowed to use SMTP AUTH | available if
        `Check with LDAP if user is allowed to use SMTP AUTH ` is set to ${True}.
        Possible values are Monitor or Reject. Monitor is the default setting. |
        | Custom SMTP response | whether to use custom SMTP response on Reject.
        Available if `If user is found to be not allowed to use SMTP AUTH` is set
        to ${True}. ${False} by default |
        | SMTP Code | Custom SMTP response code. Available if `Custom SMTP response`
        is set to ${True} |
        | Custom SMTP Response Text | custom SMTP response text. Available if
        Custom SMTP response` is set to ${True} |

        *Certificate:*
        | LDAP Query to Use | the name of existing LDAP certauth query |
        | Allow SMTP AUTH Command if no Certificate | whether to allow SMTP auth if
        client certificate is not available, ${False} by default |
        | LDAP or Forward Type SMTP Auth Profile | the name of LDAP or Forward Type
        SMTP Auth Profile. Available if `Allow SMTP AUTH Command if no Certificate`
        is set to ${True} |

        *Exceptions:*
        - `ConfigError`: if profile with the same name already exists

        *Examples:*
        | ${ldapauth_profile_settings}= | Create Dictionary |
        | ... | LDAP Query | ${LDAP_PROFILE_NAME}.smtpauth |
        | ... | Default Encryption Method | Plain |
        | ... | Check with LDAP if user is allowed to use SMTP AUTH | ${True} |
        | ... | If user is found to be not allowed to use SMTP AUTH | Reject |
        | ... | Custom SMTP response | ${True} |
        | ... | SMTP Code | 525 |
        | ... | Custom SMTP Response Text | 5.7.13 SMTP AUTH disallowed for this user |
        | ${outgoingauth_profile_settings}= | Create Dictionary |
        | ... | Authentication Username | test |
        | ... | Authentication Password | test |
        | ${forwardauth_profile_settings}= | Create Dictionary |
        | ... | Hostname | 1.1.1.1 |
        | ... | Port | 25 |
        | ... | Interface | Auto |
        | ... | Maximum Simultaneous Connections | 10 |
        | ... | Require TLS | ${True} |
        | ... | Use SASL LOGIN mechanism | ${True} |
        | ... | Use SASL PLAIN mechanism | ${True} |
        | ${certauth_profile_settings}= | Create Dictionary |
        | ... | LDAP Query to Use | ${LDAP_PROFILE_NAME}.certauth |
        | ... | Allow SMTP AUTH Command if no Certificate | ${True} |
        | ... | LDAP or Forward Type SMTP Auth Profile | ${LDAP_SMTPAUTH_PROFILE_NAME} |
        | @{profiles_data}= | Create List |
        | ... | ${LDAP_SMTPAUTH_PROFILE_NAME} | LDAP | ${ldapauth_profile_settings} |
        | ... | ${OUTGOING_SMTPAUTH_PROFILE_NAME} | Outgoing | ${outgoingauth_profile_settings} |
        | ... | ${FORWARD_SMTPAUTH_PROFILE_NAME} | Forward | ${forwardauth_profile_settings} |
        | ... | ${CERTIFICATE_SMTPAUTH_PROFILE_NAME} | Certificate | ${certauth_profile_settings} |
        | :FOR | ${profile_name} | ${profile_type} | ${profile_settings} | IN | @{profiles_data} |
        | \ | ${is_exist}= | SMTP Authentication Is Profile Exist  ${profile_name} |
        | \ | Run Keyword If | not ${is_exist} |
        | \ | ... | SMTP Authentication Add Profile | ${profile_name} | ${profile_type} |
        | \ | ... | ${profile_settings} |
        """
        if self._is_element_present(PROFILE_NAME_LINK(profile_name)):
            raise ConfigError('SMTP Authentication profile named "%s" is '\
                        'already present in profiles list' % (profile_name,))

        self.click_button(ADD_PROFILE_BUTTON)
        time.sleep(5)
        controller = self._get_profile_add_settings_controller(profile_type)
        settings.update({controller.NAME[0]: profile_name,
                         controller.TYPE_RADIO_GROUP[0]: profile_type.lower()})
        controller.set(settings)
        controller.finish()

    @go_to_page(PAGE_PATH)
    def smtp_authentication_edit_profile(self, profile_name, settings={}):
        """Edit existing SMTP Authentication profile

        *NOT IMPLEMENTED YET*
        """
        if not self._is_element_present(PROFILE_NAME_LINK(profile_name)):
            raise ValueError('SMTP Authentication profile named "%s" is not '\
                             'present in profiles list' % (profile_name,))

        self.click_button(PROFILE_NAME_LINK(profile_name))
        raise NotImplementedError('This keyword is not implemented yet')

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_authentication_delete_profile(self, profile_name):
        """Delete existing SMTP Authentication profile

        *Parameters:*
        - `profile_name`: existing auth profile name or 'all'
        to clear all existing SMTP authentication profiles.
        If there are no profiles and the keyword was invoked with
        'all' parameter then it will return silently.

        *Exceptions:*
        - `ValueError`: if profile with given name does not exist

        *Examples:*
        | :FOR | ${profile_name} | IN | @{ALL_PROFILE_NAMES} |
        | \ | SMTP Authentication Delete Profile | ${profile_name} |
        | \ | Verify Profile Existence | ${profile_name} | ${False} |
        | SMTP Authentication Delete Profile | all |
        """
        if profile_name.lower() == 'all':
            if self._is_element_present(CLEAR_ALL_BUTTON):
                self.click_button(CLEAR_ALL_BUTTON, 'don\'t wait')
                self._click_continue_button()
            else:
                self._info('No SMTP Authentication profiles are present. '\
                           'Ignoring "Clear All Profiles" action.')
            return

        if not self._is_element_present(PROFILE_DELETE_LINK(profile_name)):
            raise ValueError('SMTP Authentication profile named "%s" is not '\
                             'present in profiles list' % (profile_name,))
        self.click_button(PROFILE_DELETE_LINK(profile_name), 'don\'t wait')
        self._click_continue_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_authentication_is_profile_exist(self, profile_name):
        """Return whether auth profile with given name exists on appliance

        *Parameters:*
        - `profile_name`: existing auth profile name

        *Return:*
        ${True} if profile exists and ${False} otherwise

        *Examples:*
        | Verify Profile Existence |
        |  | [Arguments] | ${profile_name} | ${should_exist}=${True} |
        |  | ${is_exist}= | SMTP Authentication Is Profile Exist | ${profile_name} |
        |  | ${verifier_kw}= | Set Variable If | ${should_exist} |
        |  | ... | Should Be True | Should Not Be True |
        |  | Run Keyword | ${verifier_kw} | ${is_exist} |
        """
        return self._is_element_present(PROFILE_NAME_LINK(profile_name))

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def smtp_authentication_get_all_profiles(self):
        """Return all existing SMTP auth profiles

        *Return:*
        Dictionary. Keys are *Profile Name* and *Profile Type*. Corresponding
        values contain lists of strings with profile name and profile types.

        *Examples:*
        | ${profiles_info}= | SMTP Authentication Get All Profiles |
        | Log | ${profiles_info} |
        | ${profile_names}= | Get From Dictionary | ${profiles_info} | Profile Name |
        | :FOR | ${profile_name} | IN | @{ALL_PROFILE_NAMES} |
        | \ | List Should Contain Value | ${profile_names} | ${profile_name} |
        """
        result = {'Profile Name': [],
                  'Profile Type': []}
        profiles_count = int(self.get_matching_xpath_count(PROFILE_NAMES))
        for profile_idx in xrange(1, 1 + profiles_count):
            profile_name = self.get_text(PROFILE_NAME_BY_IDX(profile_idx)).strip()
            result['Profile Name'].append(profile_name)
            profile_type = self.get_text(PROFILE_TYPE_BY_IDX(profile_idx)).strip()
            result['Profile Type'].append(profile_type)
        return result
