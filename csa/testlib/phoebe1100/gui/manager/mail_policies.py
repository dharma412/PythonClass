#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/mail_policies.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import functools
from itertools import izip

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import ConfigError
from common.util.ordered_dict import OrderedDict

from mail_policies_def.policy_settings import AddPolicySettings, \
    EditPolicySettings
from mail_policies_def.antispam_entry_settings import AntispamEntrySettings
from mail_policies_def.antivirus_entry_settings import AntivirusEntrySettings
from mail_policies_def.advanced_malware_protection_entry_settings import \
    AdvancedMalwareProtectionEntrySettings
from mail_policies_def.graymail_entry_settings import GraymailEntrySettings
from mail_policies_def.content_filters_entry_settings import \
    ContentFiltersEntrySettings
from mail_policies_def.outbreak_filters_entry_settings import \
    OutbreakFiltersEntrySettings
from mail_policies_def.dlp_entry_settings import DLPEntrySettings

ADD_POLICY_BUTTON = "//input[@value='Add Policy...']"

POLICIES_TABLE = "//table[@class='cols']"
EDIT_POLICY_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                (POLICIES_TABLE, name)
EDIT_POLICY_ENTRY_LINK = lambda name, col_idx: \
    "%s//td[normalize-space()='%s']/following-sibling::td[%d]/a" % \
    (POLICIES_TABLE, name, col_idx)
DELETE_POLICY_BUTTON = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]" \
    "/following-sibling::td/img[@title='Delete...']" % \
    (POLICIES_TABLE, name)
POLICIES_HEADING_ROWS = "%s//tr[th]/th" % (POLICIES_TABLE,)
POLICIES_HEADER_BY_IDX = lambda idx: "%s[%d]" % (POLICIES_HEADING_ROWS, idx)
POLICIES_DATA_ROWS = "%s//tr[td]" % (POLICIES_TABLE,)
POLICIES_DATA_BY_IDX = lambda row_idx, col_idx: "xpath=(%s)[%d]/td[%d]" % \
                                                (POLICIES_DATA_ROWS, row_idx, col_idx)

FIND_BY_RADIOGROUP = {'Recipient': "//input[@id='findR']",
                      'Sender': "//input[@id='findS']", }
FIND_POLICIES_BUTTON = "//input[@value='Find Policies']"
FIND_EMAIL_PATTERN = "//input[@name='findEmail']"
SEARCH_RESULTS_LIST_ROWS = "//th[normalize-space()='Results:']/following::ul/li"
SEARCH_RESULTS_LIST_ROW_BY_IDX = lambda idx: "%s[%d]" % (SEARCH_RESULTS_LIST_ROWS,
                                                         idx)


def go_to_policies(func):
    @functools.wraps(func)
    def worker(self, listener_type, *args, **kwargs):
        if listener_type.lower() == 'incoming':
            PAGE_PATH = ('Mail Policies', 'Incoming Mail Policies')
        elif listener_type.lower() == 'outgoing':
            PAGE_PATH = ('Mail Policies', 'Outgoing Mail Policies')
        else:
            raise ValueError('Unknown listener type "%s". Available ' \
                             'types are "Incoming" and "Outgoing"' % \
                             (listener_type,))
        self.navigate_to(*PAGE_PATH)

        return func(self, listener_type, *args, **kwargs)

    return worker


class MailPolicies(GuiCommon):
    """Interaction class for ESA WUI Mail Policies -> Incoming Mail
       Policies/Outgoing Mail Policies pages.
    """

    def get_keyword_names(self):
        return ['mail_policies_add',
                'mail_policies_edit',
                'mail_policies_edit_antivirus',
                'mail_policies_edit_antispam',
                'mail_policies_edit_advanced_malware_protection',
                'mail_policies_edit_graymail',
                'mail_policies_edit_content_filters',
                'mail_policies_edit_outbreak_filters',
                'mail_policies_edit_dlp',
                'mail_policies_delete',
                'mail_policies_is_policy_exist',
                'mail_policies_get_all',
                'mail_policies_find']

    def _get_cached_controller(self, controller_class, entry_name):
        entry_name = entry_name.lower()
        attr_name = '_mail_policies_%s_controller' % (entry_name,)
        if not hasattr(self, attr_name):
            setattr(self, attr_name, controller_class(self))
        return getattr(self, attr_name)

    @go_to_policies
    def mail_policies_is_policy_exist(self, listener_type, name):
        """Check whether mail policy exists

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy

        *Return:*
        ${True} or ${False} depending on policy existence

        *Examples:*
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Add | ${listener_type} | ${policy_name} | ${settings} |
        | \ | ${is_exist}= | Mail Policies Is Policy Exist | ${listener_type} | ${policy_name} |
        | \ | Should Be True | ${is_exist} |
        """
        return self._is_element_present(EDIT_POLICY_LINK(name))

    def mail_policies_add(self, listener_type, name, settings):
        """Add new mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy to be added
        - `settings`: dictionary whose items can be:
        | `Insert Before` | the name of existing policy to insert after this one |
        | `Sender Option`| sender's option to select. values are:
               Any Sender (default)
               Following Senders
               Following Senders are Not |
        | `Senders to Add` | list of senders to be added to this policy.
        Each sender could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Senders to Delete` | list of senders to be deleted from the existing sender list.
        Each sender could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipient Option` | recipient's option to select. values are:
               Any Recipient (default)
               Following Recipients
               Following Recipients are Not |
        | `Recipients to Add` | list of recipients to be added to this policy.
        Each recipient could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipients to Exclude` | list of recipients to be excluded from this policy.
        Each excluded recipient could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipients to Delete` | list of recipients to be deleted from the existing
        recipient list. Each recipient could be email address or its pattern including
        the '@' symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Excluded Recipients to Delete` | list of recipients to be deleted from
        the existing excluded recipient list. Each recipient could be email address
        or its pattern including the '@' symbol. List items should be separated by
        comma. Also, it is possible to add existing LDAP group in format
        <ldap_group_query_name>:<group_name> |

        *Exceptions:*
        `ConfigError`: if mail policy having the same name already exists under
        this listener
        `ValueError`: if any of the settings has incorrect name/format

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ...  | Insert Before         | Default Policy |
        | ...  | Sender Option         | Following Senders |
        | ...  | Senders to Add        | a@d.com, b@, vm30bsd0149.ibqa.group:sender_group1 |
        | ...  | Recipient Option      |  Following Recipient |
        | ...  | Recipients to Add     | rcpt@d.com, rcpt2@d.com, b@, vm30bsd0149.ibqa.group:rcpt_group1 |
        | ...  | Recipients to Exclude | a@d.com, test@d.com, vm30bsd0149.ibqa.group:rcpt_group2 |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ...  | incoming | ${IN_POLICY_NAME} |
        | ...  | outgoing | ${OUT_POLICY_NAME} |
        | \    | Mail Policies Add | ${listener_type} | ${policy_name} | ${settings} |
        """
        if self.mail_policies_is_policy_exist(listener_type, name):
            raise ConfigError('Mail Policy named "%s" already exists' % \
                              (name,))
        self.click_button(ADD_POLICY_BUTTON)
        controller = self._get_cached_controller(AddPolicySettings, 'add')
        settings.update({controller.NAME[0]: name})
        controller.set(settings)
        self._click_submit_button()

    def mail_policies_edit(self, listener_type, name, settings={}):
        """Edit an existing mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy to be added
        - `settings`: dictionary whose items can be:
        | `Insert Before` | the name of existing policy to insert after this one |
        | `Sender Option`| sender's option to select. values are:
               Any Sender (default)
               Following Senders
               Following Senders are Not |
        | `Senders to Add` | list of senders to be added to this policy.
        Each sender could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Senders to Delete` | list of senders to be deleted from the existing sender list.
        Each sender could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipient Option` | recipient's option to select. values are:
               Any Recipient (default)
               Following Recipients
               Following Recipients are Not |
        | `Recipients to Add` | list of recipients to be added to this policy.
        Each recipient could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipients to Exclude` | list of recipients to be excluded from this policy.
        Each excluded recipient could be email address or its pattern including the '@'
        symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Recipients to Delete` | list of recipients to be deleted from the existing
        recipient list. Each recipient could be email address or its pattern including
        the '@' symbol. List items should be separated by comma. Also, it is possible to
        add existing LDAP group in format <ldap_group_query_name>:<group_name> |
        | `Excluded Recipients to Delete` | list of recipients to be deleted from
        the existing excluded recipient list. Each recipient could be email address
        or its pattern including the '@' symbol. List items should be separated by
        comma. Also, it is possible to add existing LDAP group in format
        <ldap_group_query_name>:<group_name> |

        *Exceptions:*
        - `ConfigError`: if mail policy having the same name does not exist under
        this listener
        - `ValueError`: if any of the settings has incorrect name/format

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Insert Before                 | Default Policy |
        | ... | Senders to Delete             | vm30bsd0149.ibqa.group:sender_group1 |
        | ... | Recipients to Delete          | rcpt2@d.com, vm30bsd0149.ibqa.group:rcpt_group1 |
        | ... | Excluded Recipients to Delete | vm30bsd0149.ibqa.group:rcpt_group2 |
        | ... | Sender Option                 | Following Senders |
        | ... | Senders to Add                | c@, vm30bsd0149.ibqa.group:sender_group2 |
        | ... | Recipient Option              | Following Recipient |
        | ... | Recipients to Add             | @d.com, vm30bsd0149.ibqa.group:rcpt_group2 |
        | ... | Recipients to Exclude         | test@d.com, vm30bsd0149.ibqa.group:rcpt_group3 |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ...  | incoming | ${IN_POLICY_NAME} |
        | ...  | outgoing | ${OUT_POLICY_NAME} |
        | \    | Mail Policies Edit  | ${listener_type} | ${policy_name}  | ${settings} |
        """
        if not self.mail_policies_is_policy_exist(listener_type, name):
            raise ConfigError('Mail Policy named "%s" does not exist or ' \
                              'it is not available for edit' % \
                              (name,))
        self.click_button(EDIT_POLICY_LINK(name))
        controller = self._get_cached_controller(EditPolicySettings, 'edit')
        controller.set(settings)
        self._click_submit_button()

    def _edit_mail_policy_entry_settings(self, name, listener_type, entry_name, settings):
        print name, listener_type, entry_name, settings
        if name.lower() == 'default':
            name = 'Default Policy'
        if listener_type.lower() == 'incoming':
            if entry_name == "antispam":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 1))
            elif entry_name == "antivirus":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 2))
            elif entry_name == "advanced_malware_protection":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 3))
            elif entry_name == "graymail":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 4))
            elif entry_name == "content_filters":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 5))
            elif entry_name == "outbreak_filters":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 6))
            else:
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 7))
        elif listener_type.lower() == 'outgoing':
            if entry_name == "antispam":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 1))
            elif entry_name == "antivirus":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 2))
            elif entry_name == "advanced_malware_protection":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 3))
            elif entry_name == "graymail":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 4))
            elif entry_name == "content_filters":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 5))
            elif entry_name == "outbreak_filters":
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 6))
            else:
                self.click_button(EDIT_POLICY_ENTRY_LINK(name, 7))
        else:
            raise ValueError('Unknown listener type "%s". Available ' \
                             'types are "Incoming" and "Outgoing"' % \
                             (listener_type,))

        ENTRY_CONTROLLERS_MAPPING = {'antispam': AntispamEntrySettings,
                                     'antivirus': AntivirusEntrySettings,
                                     'advanced_malware_protection': AdvancedMalwareProtectionEntrySettings,
                                     'graymail': GraymailEntrySettings,
                                     'content_filters': ContentFiltersEntrySettings,
                                     'outbreak_filters': OutbreakFiltersEntrySettings,
                                     'dlp': DLPEntrySettings}
        controller = self._get_cached_controller(
            ENTRY_CONTROLLERS_MAPPING[entry_name.lower()],
            entry_name.lower())
        controller.set(settings)
        controller.submit_changes()

    @go_to_policies
    def mail_policies_edit_antispam(self, listener_type, name, settings={}):
        """Edit Anti-Spam entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `Anti-Spam Scanning` | anti-spam scanning mode for this policy.
        Either 'Use Default Settings' (available in non-default policy),
        'Use selected Anti-Spam services' (available if IMS or Cloudmark
        services are enabled), 'Use IronPort Intelligent Multi-Scan'
        (available if IMS is enabled), 'Use IronPort Anti-Spam service'
        (available if only CASE is enabled (default behavior)), 'Disabled'.
        All other settings will not be available if this option is set to
        'Disabled' |
        | `Use IronPort Anti-Spam` | Whether to use CASE engine
        on this policy. Available if `Anti-Spam Scanning` is set to
        'Use selected Anti-Spam services'. Either ${True} or ${False} |
        | `Use Cloudmark Service Provider` |Whether to use Clodmark engine
        on this policy. Available if `Anti-Spam Scanning` is set to
        'Use selected Anti-Spam services'. Either ${True} or ${False} |
        | `Enable Suspected Spam Scanning` | Whether to enable suspected
        messages scanning. Either 'Yes' or 'No' |

        The following settings are common for their categories and available
        only if `Enable Suspected Spam Scanning` are set to 'Yes'.
        Category names are:
        | *Positive Spam* |
        | *Suspected Spam* |

        In order to set any of these settings simply prepend its category
        name to its name and put a space in between:

        | `Apply Action` | What action should be applied to a message. Either
        'Deliver' or 'Drop' or 'Bounce' |
        | Alternate Host | Alternate host address. Available if `Apply Action`
        is set to 'Deliver' |
        | `Subject Text Action` | Subject text action. Either 'No', 'Prepend'
        or 'Append' |
        | `Add Subject Text` | a text, which will be added to message subject.
        Available if `Subject Text Action` is not set to 'No' |
        | `Add Custom Header Name` | Custom message header name. Available if
        `Apply Action` is set to 'Deliver' |
        | `Add Custom Header Text` | Custom Header Text. Available if
        `Apply Action` is set to 'Deliver' |
        | `Alternate Envelope Recipient` | alternate envelope recipient email
        address. Available if `Apply Action` is set to 'Deliver' |
        | `Archive Message` | Wether to archive message. Either 'Yes' or 'No' |

        The following settings are common for their categories and available
        only if CASE/Cloudmark antispam services are enabled.
        Category names are:
        | *CASE* |
        | *Cloudmark* |

        In order to set any of these settings simply prepend its category
        name to its name and put a space in between:

        | `Spam Thresholds` | Whether to set custom or predefined Spam Thresholds.
        available values are 'Use the Default Thresholds' or 'Use Custom Settings' |
        | `Positive Spam Score` | Positive spam score threshold value (integer 0-100).
        Available if `Spam Thresholds` is set to 'Use Custom Settings' |
        | `Suspected Spam Score ` | Suspected spam score threshold value (integer 0-100).
        Available if `Spam Thresholds` is set to 'Use Custom Settings' |

        *Exceptions*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Anti-Spam Scanning | Use selected Anti-Spam services |
        | ... | Use IronPort Anti-Spam | ${True} |
        | ... | Use Cloudmark Service Provider | ${True} |
        | ... | Enable Suspected Spam Scanning | Yes |
        | ... | Positive Spam Apply Action | Deliver |
        | ... | Positive Spam Alternate Host | example.com |
        | ... | Positive Spam Subject Text Action | Prepend |
        | ... | Positive Spam Add Subject Text | [SPAM] |
        | ... | Positive Spam Add Custom Header Name | X-Custom-Header |
        | ... | Positive Spam Add Custom Header Text | header_value |
        | ... | Positive Spam Alternate Envelope Recipient | test@example.com |
        | ... | Positive Spam Archive Message | Yes |
        | ... | CASE Spam Thresholds | Use Custom Settings |
        | ... | CASE Positive Spam Score | 90 |
        | ... | CASE Suspected Spam Score | 50 |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Edit Antispam | ${listener_type} | ${policy_name} | ${settings} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'antispam', settings)

    @go_to_policies
    def mail_policies_edit_antivirus(self, listener_type, name, settings={}):
        """Edit Anti-Virus entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `Anti-Virus Scanning` | anti-virus scanning mode for this policy.
        Either: 'Yes', 'Use Default Settings' (available for non-default policies),
        'No'. If this setting is set to 'No' then all other settings will
        be unavailable |
        | `Use Sophos Anti-Virus` | Either ${True} or ${False}. Available if
        Sophos antivirus service has been previously enabled |
        | `Use McAfee Anti-Virus` | Either ${True} or ${False}. Available if
        MvcAfee antivirus service has been previously enabled |
        | `Message Scanning Action` | An action to perform while scanning
        messages. Either 'Scan and Repair viruses' or 'Scan for Viruses only' |
        | `Drop Attachments` | Whether to drop infected attachments if a
        virus is found (${True} or ${False}) |
        | `Include X-header` | Whether to include an X-header with the
        Anti-Virus scanning results in messages (${True} or ${False}) |

        The following settings are common for their categories and available
        only if `Message Scanning Action` is set to 'Scan and Repair viruses'.
        Category names are:
        | *Repaired Messages* |
        | *Encrypted Messages* |
        | *Unscannable Messages* |
        | *Virus Infected Messages* |

        In order to set any of these settings simply prepend its category
        name to its name and put a space in between:

        | `Apply Action` | An action to apply to a message. Either
        'Deliver As Is' or 'Deliver as Attachment (text/plain) to New Message'
        or 'Deliver as Attachment (message/rfc822) to New Message' |
        | `Archive Original` | Whther to archive original message. Either 'Yes'
        or 'No' |
        | `Modify Subject` | How to modify message's subject: Either 'No',
        'Prepend' or 'Append' |
        | `Add Subject Text` | Modification text. Available if `Modify Subject`
        is not set to 'No' |
        | `Add Custom Header` | Whether to add custom message header. Either
        'Yes' or 'No' |
        | `Add Custom Header Name` | The name of new custom header. Available
        if `Add Custom Header` is set to 'Yes' |
        | `Add Custom Header Value` | Value of new custom header. Available
        if `Add Custom Header` is set to 'Yes' |
        | `Container Notification` | The name of existing notification template
        created under Mail Policies > Text Resources > Anti-Virus Container Template |
        | `Other Notification Rcpt Sender` | Whether to send notification
        to message sender. Either ${True} or ${False} |
        | `Other Notification Rcpt Recipient` | Whether to send notification
        to message recipient. Either ${True} or ${False} |
        | `Other Notification Rcpt Others` | Whether to send notification
        to other people. Either ${True} or ${False} |
        | `Other Notification Rcpt Others Emails` | Email addresses list. Each
        item should be separated by comma. available if `Other Notification Rcpt Others`
        is set to ${True} |
        | `Other Notification Template` | The name of existing notification template
        created under see Mail Policies > Text Resources > Anti-Virus Notification |
        | `Other Notification Subject` | Notification subject. Available if
        `Other Notification Template` is set |
        | `Modify Recipient` | Whether to modify original recipient. Not available for
        *Repaired Messages* category. Either 'Yes' or 'No' |
        | `Modified Recipient Address` | Modified recipient email address. Available if
        `Modify Recipient` is set to 'Yes' |
        | `Send To Alternate Host` | Whether to send message to alternate host.
        Not available for *Repaired Messages* category. Either 'Yes' or 'No' |
        | `Alternate Host` | Alternate host name. Available if `Send To Alternate Host`
        is set to 'Yes' |

        *Exceptions*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Anti-Virus Scanning | Yes |
        | ... | Use Sophos Anti-Virus | ${True} |
        | ... | Use McAfee Anti-Virus | ${True} |
        | ... | Message Scanning Action | Scan and Repair viruses |
        | ... | Drop Attachments | ${True} |
        | ... | Include X-header | ${True} |
        | ... | Encrypted Messages Apply Action | Deliver As Is |
        | ... | Encrypted Messages Archive Original | Yes |
        | ... | Encrypted Messages Modify Subject | Prepend |
        | ... | Encrypted Messages Add Subject Text | [WARNING: MESSAGE ENCRYPTED] |
        | ... | Encrypted Messages Add Custom Header | Yes |
        | ... | Encrypted Messages Add Custom Header Name |  X-My-Custom-Header |
        | ... | Encrypted Messages Add Custom Header Value | custom_value |
        | ... | Encrypted Messages Container Notification | blabla |
        | ... | Encrypted Messages Other Notification Rcpt Sender | ${True} |
        | ... | Encrypted Messages Other Notification Rcpt Recipient | ${True} |
        | ... | Encrypted Messages Other Notification Rcpt Others | ${True} |
        | ... | Encrypted Messages Other Notification Rcpt Others Emails | a@example.com |
        | ... | Encrypted Messages Other Notification Template | blabla |
        | ... | Encrypted Messages Other Notification Subject | Test Subject |
        | ... | Encrypted Messages Modify Recipient | Yes |
        | ... | Encrypted Messages Modified Recipient Address | test@example.com |
        | ... | Encrypted Messages Send To Alternate Host | Yes |
        | ... | Encrypted Messages Alternate Host | example.com |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Edit Antivirus | ${listener_type} | ${policy_name} | ${settings} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'antivirus', settings)

    @go_to_policies
    def mail_policies_edit_advanced_malware_protection(self, listener_type, name, settings={}):
        """Edit Advanced Malware Protection entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `Advanced Malware Protection` | Advanced Malware Protection mode for this policy.
        Either: 'Yes', 'Use Default Settings' (available for non-default policies),
        'No'. If this setting is set to 'No' then all other settings will
        be unavailable |
        | `Enable File Analysis` | Either ${True} or ${False}. Available if
        File Analysis service has been previously enabled |
        | `Include an X-header` | Whether to include an X-header with the
        Advanced Malware Protection results in messages (${True} or ${False}) |

        The following settings are common for their categories'.
        Category names are:
        | *Unscannable Attachments* |
        | *Messages with Malware Attachments* |
        | *Messages with File Analysis Pending* |

        In order to set any of these settings simply prepend its category
        name to its name and put a space in between:

        | `Apply Action` | An action to apply to a message. Either
        'Deliver As Is' or 'Drop Message' or 'Quarantine' |
        | `Archive Original` | Whether to archive original message. Either 'Yes'
        or 'No' |
        | `Drop Malware` | Whether to drop malware message. Either 'Yes'
        or 'No' |
        | `Modify Subject` | How to modify message's subject: Either 'No',
        'Prepend' or 'Append' |
        | `Add Subject Text` | Modification text. Available if `Modify Subject`
        is not set to 'No' |
        | `Add Custom Header` | Whether to add custom message header. Either
        'Yes' or 'No' |
        | `Add Custom Header Name` | The name of new custom header. Available
        if `Add Custom Header` is set to 'Yes' |
        | `Add Custom Header Value` | Value of new custom header. Available
        if `Add Custom Header` is set to 'Yes' |

        *Exceptions*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Advanced Malware Protection | Yes |
        | ... | Enable File Analysis | ${True} |
        | ... | Include an X-header | ${False} |
        | ... | Messages with File Analysis Pending Apply Action | Quarantine |
        | ... | Messages with File Analysis Pending Archive Original | No |
        | ... | Messages with File Analysis Pending Modify Subject | Append |
        | ... | Messages with File Analysis Pending Add Subject Text | [WARNING: MESSAGE ENCRYPTED] |
        | ... | Messages with File Analysis Pending Add Custom Header | Yes |
        | ... | Messages with File Analysis Pending Add Custom Header Name |  X-My-Custom-Header |
        | ... | Messages with File Analysis Pending Add Custom Header Value | custom_value |
        | ... | Unscannable Attachments Apply Action | Deliver As Is |
        | ... | Unscannable Attachments Archive Original | No |
        | ... | Unscannable Attachments Modify Subject | Append |
        | ... | Unscannable Attachments Add Subject Text | [WARNING: MESSAGE ENCRYPTED] |
        | ... | Unscannable Attachments Add Custom Header | Yes |
        | ... | Unscannable Attachments Add Custom Header Name |  X-My-Custom-Header |
        | ... | Unscannable Attachments Add Custom Header Value | custom_value |
        | ... | Messages with Malware Attachments Apply Action | Deliver As Is |
        | ... | Messages with Malware Attachments Archive Original | Yes |
        | ... | Messages with Malware Attachments Drop Malware | Yes |
        | ... | Messages with Malware Attachments Modify Subject | Prepend |
        | ... | Messages with Malware Attachments Add Subject Text | [WARNING: MESSAGESSS ENCRYPTED] |
        | ... | Messages with Malware Attachments Add Custom Header | Yes |
        | ... | Messages with Malware Attachments Add Custom Header Name |  X-My-Custom-Header1 |
        |...  | Messages with Malware Attachments Add Custom Header Value | custom_value1 |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Edit Advanced Malware Protection | ${listener_type} | ${policy_name} | ${settings} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'advanced_malware_protection', settings)

    @go_to_policies
    def mail_policies_edit_graymail(self, listener_type, name, settings={}):
        """Edit GrayMail Settings for the given mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: name of the mail policy whose entry is going to be edited
        or 'default' to edit the default policy

        - `settings`: dictionary whose items can be:
        | `Graymail Detection` | Graymail detection mode for this policy.
        Either: 'Use Default Settings' (available for non-default policies),
        'Use Graymail Detection' or 'Disable Graymail Detection'.
        If this setting is set to 'Disable Graymail Detection' then all other settings will
        be unavailable |
        | `Graymail Un-subscription` | Either 'Use Graymail Un-subscription'
        or 'Disable Graymail Un-subscription'. Available if
        Graymail Detection service has been enabled |
        | `Perform this action for` | Either 'All Messages' or 'Unsigned Messages' |

        The following settings are common for their categories and available
        only if `Graymail Detection`is set to 'Use Graymail Detection'.
        | `Enable Marketing Email Scanning` | Whether to use Marketing email scanning
        on this policy. Available if 'Graymail Detection' is set to 'Use Graymail Detection' |
        | `Enable Social Networking Email Scanning` | Whether to use Social Networking
        email scanning on this policy. Available if 'Graymail Detection' is set to 'Use Graymail Detection' |
        | `Enable Bulk Email Scanning` | Whether to use Bulk email scanning on this policy.
        Available if 'Graymail Detection' is set to 'Use Graymail Detection' |

        In order to set any of these settings simply prepend its category
        name to its name and put a space in between:

        | `Apply Action` | What action should be applied to a message. Either
        'Deliver' or 'Drop' or 'Bounce' |
        | Alternate Host | Alternate host address. Available if `Apply Action`
        is set to 'Deliver' |
        | `Subject Text Action` | Subject text action. Either 'No', 'Prepend'
        or 'Append' |
        | `Add Subject Text` | a text, which will be added to message subject.
        Available if `Subject Text Action` is not set to 'No' |
        | `Add Custom Header Name` | Custom message header name. Available if
        `Apply Action` is set to 'Deliver' |
        | `Add Custom Header Text` | Custom Header Text. Available if
        `Apply Action` is set to 'Deliver' |
        | `Alternate Envelope Recipient` | alternate envelope recipient email
        address. Available if `Apply Action` is set to 'Deliver' |
        | `Archive Message` | Wether to archive message. Either 'Yes' or 'No' |

        *Exceptions*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${gm_settings}= | Create Dictionary                         |
        | ... | Graymail Detection                                    | Use Graymail Detection |
        | ... | Enable Marketing Email Scanning                       | ${True} |
        | ... | Marketing Email Apply Action                          | Deliver |
        | ... | Marketing Email Alternate Host                        | ${CLIENT_IP} |
        | ... | Marketing Email Subject Text Action                   | Prepend |
        | ... | Marketing Email Add Subject Text                      | [GM Marketing Test Policy] |
        | ... | Marketing Email Add Custom Header Name                | X-GM-Sub-Prepend |
        | ... | Marketing Email Add Custom Header Text                | True |
        | ... | Marketing Email Alternate Envelope Recipient          | gm_test_pol@cisco.com |
        | ... | Marketing Email Archive Message                       | Yes |
        | ... | Enable Social Networking Email Scanning               | Yes |
        | ... | Social Networking Email Apply Action                  | Deliver |
        | ... | Social Networking Email Alternate Host                | ${CLIENT_IP} |
        | ... | Social Networking Email Subject Text Action           | Append |
        | ... | Social Networking Email Add Subject Text              | [GM Social Networking Test Policy] |
        | ... | Social Networking Email Add Custom Header Name        | X-GM-Sub-Append |
        | ... | Social Networking Email Add Custom Header Text        | True |
        | ... | Social Networking Email Alternate Envelope Recipient  | gm_test_pol@cisco.com |
        | ... | Social Networking Email Archive Message               | No |
        | ... | Enable Bulk Email Scanning                            | Yes |
        | ... | Bulk Email Apply Action                               | Deliver |
        | ... | Bulk Email Alternate Host                             | ${CLIENT_IP} |
        | ... | Bulk Email Subject Text Action                        | Append |
        | ... | Bulk Email Add Subject Text                           | [GM Bulk Email Test Policy] |
        | ... | Bulk Email Add Custom Header Name                     | X-GM-Sub-Append |
        | ... | Bulk Email Add Custom Header Text                     | True |
        | ... | Bulk Email Alternate Envelope Recipient               | gm_test_pol@cisco.com |
        | ... | Bulk Email Archive Message                            | Yes |
        | Mail Policies Edit Graymail |
        | ... | incoming  gm_test_pol3 | ${gm_settings} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'graymail', settings)

    @go_to_policies
    def mail_policies_edit_content_filters(self, listener_type, name, settings={}):
        """Edit Content Filters entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `Content Filters` | Whether to apply content filters on this
        policy. Possible values are
        'Enable Content Filters (Inherit default mail policy settings)'
        (available on non-default policies),
        'Enable Content Filters (Customize settings)' or
        'Disable Content Filters'. In case this value is set to
        'Disable Content Filters' then all other options will not be available |
        | `Enable All` | Either ${True} or ${False} to enable/disable all
        available content filters on this mail policy |
        | `<content_filter_name>` | Either ${True} or ${False} to enable/disable
        existing content filter named <content_filter_name> on this mail policy.
        There may be multiple items of such type. |

        *Exceptions:*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Content Filters | Enable Content Filters (Customize settings) |
        | ... | ${FILTER_NAME} | ${True} |
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Edit Content Filters | ${listener_type} | ${policy_name} | ${settings} |
        | \ | ${disable_all}= | Create Dictionary | Enable All | ${False} |
        | \ | Mail Policies Edit Content Filters | ${listener_type} | ${policy_name} | ${disable_all} |
        | \ | ${enable_all}= | Create Dictionary | Enable All | ${True} |
        | \ | Mail Policies Edit Content Filters | ${listener_type} | ${policy_name} | ${enable_all} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'content_filters', settings)

    @go_to_policies
    def mail_policies_edit_outbreak_filters(self, listener_type, name, settings={}):
        """Edit Outbreak Filters entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `Outbreak Filters` | Whether to apply outbreak filtering on this
        policy. Possible values are
        'Enable Outbreak Filtering (Inherit default mail policy settings)'
        (available on non-default policies),
        'Enable Outbreak Filtering (Customize settings)' or
        'Disable Outbreak Filtering'. In case this value is set to
        'Disable Outbreak Filtering' then all other options will not be available |
        | `Quarantine Threat Level` | Number in range 1..5 |
        | `Maximum Quarantine Retention for Viral Attachments` | Duration in format
        '<number> Days/Hours' |
        | `Maximum Quarantine Retention for Other Threats` | Duration in format
        '<number> Days/Hours' |
        | `Bypass Attachment Scanning for` | A List of attachment extensions to bypass
        during scan. This is a string whose items are separated by commas |
        | `Deliver Messages without Quarantining` | Whether to deliver messages without
        adding them to the quarantine Either ${True} or ${False} |
        | `Enable Message Modification` | Whether to enable message modification.
        Either ${True} or ${False}. In case this option is set to ${False} all the
        follwoing options will not be available |
        | `Message Modification Threat Level` | Number in range 1..5 |
        | `Modified Message Subject Action` | Modified message subject action.
        Either 'Prepend', 'No' or 'Append' |
        | `Include the X-IronPort-Outbreak headers` | Whether to include the
        X-IronPort-Outbreak headers. Available values are:
        'Enable only for threat-based outbreak', 'Enable for all messages',
        'Disable' |
        | `Include the X-IronPort-Outbreak-Description header` | Whether to include the
        X-IronPort-Outbreak-Description header. Available values are:
        'Enable', 'Disable' |
        | `Alternate Destination Mail Host` | Enter the Alternate Destination Mail Host |
        | `Modified Message Subject` | Available if `Modified Message Subject Action`
        is not set to 'No' |
        | `URL Rewriting` | Cisco Security proxy scans and rewrites all URLs
        contained in malicious outbreak emails. Available values are:
        'Enable only for unsigned messages', 'Enable for all messages' or
        'Disable' |
        | `Bypass Domain Scanning for` | A list of domain names/IP addresses
        on which scanning has to be bypassed. Each list item is sperated by comma |
        | `Threat Disclaimer` | The name of existing disclaimer template defined under
        Mail Policies > Text Resources > Disclaimers |

        *Exceptions:*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Outbreak Filters | Enable Outbreak Filtering (Customize settings) |
        | ... | Quarantine Threat Level | 3 |
        | ... | Maximum Quarantine Retention for Viral Attachments | 1 days |
        | ... | Maximum Quarantine Retention for Other Threats | 4 Hours |
        | ... | Deliver Messages without Quarantining | ${True} |
        | ... | Bypass Attachment Scanning for | exe, com, bat |
        | ... | Enable Message Modification | ${True} |
        | ... | Message Modification Threat Level | 3 |
        | ... | Modified Message Subject Action | Prepend |
        | ... | Modified Message Subject | [SUSPICIOUS MESSAGE] |
        | ... | Include the X-IronPort-Outbreak headers | Enable for all messages |
        | ... | Include the X-IronPort-Outbreak-Description header | Enable |
        | ... | Alternate Destination Mail Host | example.com |
        | ... | URL Rewriting | Enable for all messages |
        | ... | Bypass Domain Scanning for | example.com, test.example.com |
        | ... | Threat Disclaimer | System Generated |
        | :FOR | ${listener_type} | IN | incoming | outgoing |
        | \ | Mail Policies Edit Outbreak Filters | ${listener_type} | default | ${settings} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'outbreak_filters', settings)

    @go_to_policies
    def mail_policies_edit_dlp(self, listener_type, name, settings={}):
        """Edit DLP entry of the particular mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Since DLP
        is available on outgoing policy only then only value available
        is outgoing
        - `name`: the name of mail policy whose entry is going to be edited
        or 'default' to edit the default policy
        - `settings`: dictionary whose items can be:
        | `DLP Policies` | Whether to apply DLP policies on this
        policy. Possible values are
        'Enable DLP (Inherit default mail policy settings)
        (available on non-default policies),
        'Enable DLP (Customize settings)' and 'Disable DLP'.
        In case this value is set to
        'Disable DLP' then all other options will not be available |
        | `Enable All` | Either ${True} or ${False} to enable/disable all
        available DLP policies on this mail policy |
        | `<dlp_policy_name>` | Either ${True} or ${False} to enable/disable
        existing DLP policy named <dlp_policy_name> on this mail policy.
        There may be multiple items of such type. |

        *Exceptions:*
        - `ConfigError`: if there is not such mail policy or no such editable entry
        in this policy
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ...  DLP Policies | Enable DLP (Customize settings) |
        | ...  ${DLP_POLICY_NAME} | ${True} |
        | Mail Policies Edit DLP | outgoing | ${OUT_POLICY_NAME}  ${settings}
        | ${disable_all}= | Create Dictionary | Enable All  ${False}
        | Mail Policies Edit DLP | outgoing | ${OUT_POLICY_NAME} | ${disable_all} |
        | ${enable_all}= | Create Dictionary | Enable All  ${True}
        | Mail Policies Edit DLP | outgoing | ${OUT_POLICY_NAME} | ${enable_all} |
        """
        self._edit_mail_policy_entry_settings(name, listener_type, 'dlp', settings)

    @go_to_policies
    def mail_policies_delete(self, listener_type, name):
        """Delete existing mail policy

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `name`: the name of existing mail policy to be deleted

        *Exceptions:*
        - `ConfigError`: if there is no mail policy named `name` or
        the policy cannot be deleted

        *Examples:*
        | :FOR | ${listener_type} | ${policy_name} | IN |
        | ... | incoming | ${IN_POLICY_NAME} |
        | ... | outgoing | ${OUT_POLICY_NAME} |
        | \ | Mail Policies Delete | ${listener_type} | ${policy_name} |
        | \ | ${is_exist}= | Mail Policies Is Policy Exist | ${listener_type} | ${policy_name} |
        | \ | Should Not Be True | ${is_exist} |
        """
        if not self._is_element_present(DELETE_POLICY_BUTTON(name)):
            raise ConfigError('Mail Policy named "%s" does not exist or ' \
                              'cannot be deleted' % (name,))
        self.click_button(DELETE_POLICY_BUTTON(name), 'don\'t wait')
        self.click_button("//button[normalize-space()='Delete']")
        self._check_action_result()

    @go_to_policies
    def mail_policies_get_all(self, listener_type):
        """Get current mail policies

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing

        *Return:*
        Dictionary whose keys are corresponding column headers in mail policies table
        and values are lists with corresponding column cells. This keyword will
        return default policy only if no other policies are configured.

        *Examples:*
        | ${existing_policies}= | Mail Policies Get All | incoming |
        | Log | ${existing_policies} |
        | @{names_list}= | Get From Dictionary | ${existing_policies} | Policy Name |
        | List Should Contain Value | ${names_list} | ${IN_POLICY_NAME} |
        """
        cols_count = int(self.get_matching_xpath_count(POLICIES_HEADING_ROWS))
        # Remove the "Delete" column
        cols_count -= 1
        result = OrderedDict()
        for col_idx in xrange(1, 1 + cols_count):
            header_name = self.get_text(POLICIES_HEADER_BY_IDX(col_idx)).strip()
            result[header_name] = []
        policies_count = int(self.get_matching_xpath_count(POLICIES_DATA_ROWS))
        for policy_idx in xrange(1, 1 + policies_count):
            for col_idx, col_name in izip(range(1, 1 + len(result.keys())),
                                          result.keys()):
                data = self.get_text(POLICIES_DATA_BY_IDX(policy_idx,
                                                          col_idx)).strip()
                result[col_name].append(data)
        return result

    @go_to_policies
    def mail_policies_find(self, listener_type, settings):
        """Find mail polices by senders/recipients

        *Parameters:*
        - `listener_type`: type of a destination listener. Either incoming
        outgoing
        - `settings`: dictionary. Available items are:
        | `Sender` | email address of sender to look for |
        | `Recipient` | email address of recipient to look for |
        Only one entry should be present in dictionary at the same time

        *Return:*
        List of found policies names or empty list if nothing is found (
        since Default Policy includes all entries by default
        it may be present in this list)

        *Exceptions:*
        - `ValueError`: if `settings` dictionary contains icorrect items

        *Examples:*
        | ${find_settings}= | Create Dictionary |
        | ... | Sender | me_sender@cisco.com |
        | @{matching_policies}= | Mail Policies Find | incoming | ${find_settings} |
        | List Should Contain Value | ${matching_policies} | ${IN_POLICY_NAME} |
        """
        try:
            self._click_radio_button(FIND_BY_RADIOGROUP[settings.keys()[0]])
        except KeyError:
            raise ValueError('Unknown setting "%s". Available key names: "%s"' % \
                             (settings.keys()[0], FIND_BY_RADIOGROUP.keys()))
        self.input_text(FIND_EMAIL_PATTERN, settings.values()[0])
        self.click_button(FIND_POLICIES_BUTTON)

        result = []
        results_count = int(self.get_matching_xpath_count(SEARCH_RESULTS_LIST_ROWS))
        for idx in xrange(1, 1 + results_count):
            data = self.get_text(SEARCH_RESULTS_LIST_ROW_BY_IDX(idx)).strip()
            result.append(data)
        return result
