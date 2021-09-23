#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/monitor/quarantines/quarantines.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from locators import *
from spam import SpamQuarantine
from search import Search
from message import QuarantinedMessage, SpamQuarantinedMessage
from policy import PolicyQuarantine
from virus import VirusQuarantine
from outbreak import OutbreakQuarantine, OutbreakQuarantineManageByRule
from quarantine import Quarantine
from slbl import Slbl
from sal.containers.cfgholder import CfgHolder


# NOTE: order of parent classes is important
class Quarantines(SpamQuarantine,
                  OutbreakQuarantineManageByRule,
                  Search,
                  SpamQuarantinedMessage,
                  QuarantinedMessage,
                  PolicyQuarantine,
                  VirusQuarantine,
                  OutbreakQuarantine,
                  Quarantine,
                  Slbl, ):
    """
    Interact with 'Monitor > Quarantines' pages.

    *Quick reference on keywords in this module*\n
    With these keywords end-user can:\n
    * manage quarantines - add/edit/delete/disable/enable;
    * search messages in quarantines;
    * release/delete messages from quarantines;
    * open quarantined message and get detailed info/rescan/release/delete message;
    * get detailed information about all quarantines;
    * get detailed information about separate quarantine;
    * check if quarantine is active/enabled;
    * manage SLBL settings;
    * manage Outbreak quarantine by rule summary.

    *Quarantines management*\n
    To get information about quarantine(s):
    - `Quarantines Get All Names`
    - `Quarantines Get Detailed Info All`
    - `Quarantines Get Detailed Info`
    - `Quarantines Is Active`
    - `Quarantines Get Settings`
    - `Quarantines Policy Get Settings`
    - `Quarantines Policy Is Active`
    - `Quarantines Virus Get Settings`
    - `Quarantines Virus Is Active`
    - `Quarantines Outbreak Get Settings`
    - `Quarantines Outbreak Is Active`
    - `Quarantines Spam Get Settings`
    - `Quarantines Spam Is Active`
    - `Quarantines Spam Is Enabled`

    To add/edit/delete/disable/enable quarantine:
    - `Quarantines Add`
    - `Quarantines Edit`
    - `Quarantines Delete`
    - `Quarantines Policy Edit`
    - `Quarantines Policy Delete`
    - `Quarantines Virus Edit`
    - `Quarantines Outbreak Edit`
    - `Quarantines Spam Edit`
    - `Quarantines Spam Enable`
    - `Quarantines Spam Disable`
    - `Quarantines Spam Edit Main Settings` - can be done with `Quarantines Spam Edit` also.
    - `Quarantines Spam Edit Notifications` - can be done with `Quarantines Spam Edit` also.
    - `Quarantines Spam Edit Users` - can be done with `Quarantines Spam Edit` also.
    - `Quarantines Spam Edit Euq` - can be done with `Quarantines Spam Edit` also.
    - `Quarantines Spam Edit Appearance` - can be done with `Quarantines Spam Edit` also.

    *Search functionality*\n
    Keywords that work with _single_ message:
    - `Quarantines Search Message Open` - finds message and opens Message page.
    - `Quarantines Search Message By Mid` - finds message and opens Message page.
    - `Quarantines Message Get Details` - works with already opened message.
    - `Quarantines Message Send Copy` - works with already opened message.
    - `Quarantines Message Rescan` - works with already opened message.
    - `Quarantines Message Delete` - works with already opened message.
    - `Quarantines Message Release` - works with already opened message.
    - `Quarantines Search Move To` - move messages to another quarantine.
    - `Quarantines Search Send Copy To` - send copy to email address.
    - `Quarantines Search Schedule Exit By` - schedule exit.
    - `Quarantines Spam Message Get Details` - get message details of currently opened message.
    - `Quarantines Spam Message Delete` - delete currently opened message.
    - `Quarantines Spam Message Release` - release currently opened message.
    From the keywords above some do the same but from different locations(pages) in WUI.
    For example, `Quarantines Search Message And Delete` - deletes message using WUI controls
    from search table and does not open message, while `Quarantines Message Delete` does the same
    but from inside opened Message page.

    *Outbreak Manage By Rule*\n
    - `Quarantines Outbreak Manage By Rule Parse Summary Table` - parse Outbreak matched rules summary table.
    - `Quarantines Outbreak Manage By Rule Get Messages` - get all messages matching certain rule.
    - `Quarantines Outbreak Manage By Rule Delete` - delete all messages by rule.
    - `Quarantines Outbreak Manage By Rule Release` - release all messages by rule.
    """

    # Contains methods(keywords) to work with all quarantines.
    # RF tests refer to this class to get keywords.

    def get_keyword_names(self):
        return ['quarantines_get_all_names',
                'quarantines_get_detailed_info_all',
                'quarantines_get_detailed_info',
                'quarantines_add',
                'quarantines_edit',
                'quarantines_delete',
                'quarantines_get_settings',
                'quarantines_is_active',
                'quarantines_policy_edit',
                'quarantines_policy_delete',
                'quarantines_policy_get_settings',
                'quarantines_policy_is_active',
                'quarantines_virus_edit',
                'quarantines_virus_get_settings',
                'quarantines_virus_is_active',
                'quarantines_outbreak_edit',
                'quarantines_outbreak_get_settings',
                'quarantines_outbreak_is_active',
                'quarantines_spam_edit',
                'quarantines_spam_enable',
                'quarantines_spam_disable',
                'quarantines_spam_get_settings',
                'quarantines_spam_is_active',
                'quarantines_spam_is_enabled',
                'quarantines_spam_edit_main_settings',
                'quarantines_spam_edit_notifications',
                'quarantines_spam_edit_users',
                'quarantines_spam_edit_euq',
                'quarantines_spam_edit_appearance',
                'quarantines_spam_delete_existing_ldap_group_queries',
                'quarantines_search',
                'quarantines_search_across',
                'quarantines_search_message_view_tracking_details',
                'quarantines_search_is_empty_quarantine',
                'quarantines_search_open_quarantine',
                'quarantines_search_view_all_messages',
                'quarantines_search_get_messages',
                'quarantines_search_get_all_messages',
                'quarantines_search_message_open',
                'quarantines_search_message_by_mid',
                'quarantines_search_release',
                'quarantines_search_delete',
                'quarantines_search_send_copy_to',
                'quarantines_search_move_to',
                'quarantines_search_schedule_exit_by',
                'quarantines_message_get_details',
                'quarantines_message_send_copy',
                'quarantines_message_rescan',
                'quarantines_message_delete',
                'quarantines_message_release',
                'quarantines_spam_message_get_details',
                'quarantines_spam_message_delete',
                'quarantines_spam_message_release',
                'quarantines_slbl_enable',
                'quarantines_slbl_disable',
                'quarantines_slbl_is_enabled',
                'quarantines_slbl_edit_settings',
                'quarantines_slbl_get_settings',
                'quarantines_outbreak_manage_by_rule_get_messages',
                'quarantines_outbreak_manage_by_rule_parse_summary_table',
                'quarantines_outbreak_manage_by_rule_delete',
                'quarantines_outbreak_manage_by_rule_release', ]

    def quarantines_get_all_names(self, exclude_disabled=False):
        """
        Get list of configured quarantines.
        Note: this list will contain *all* quarantines present in the table,
        including disabled/in-active.

        *Parameters*:
        - `exclude_disabled`: Exclude disabled quarantines. ${True} or ${False}

        *Return*:
        List

        *Examples*:
        | ${qs} | Quarantines Get All Names |
        | Log List | ${qs} |
        | Should Contain | ${qs} | Policy |
        | Should Contain | ${qs} | ${q2} |
        """
        self._info('Get list of configured quarantines')
        self._open_page()
        return self._get_element_list(QUARANTINES_TABLE, only_clickable=exclude_disabled, dont_count_last_nrows=1)

    def quarantines_get_detailed_info_all(self, exclude_disabled=False):
        """
        Get detailed list of configured quarantines.
        Note: this list will contain *all* quarantines present in the table,
        including disabled/in-active.

        *Parameters*:
        - `exclude_disabled`: Exclude disabled quarantines. ${True} or ${False}

        *Return*:
        Dictionary(CfgHolder).
        The names of quarantines are keys of dictionary.
        Each dictionary has such keys:
        | _Keys_ | _Values types_ |
        | messages | String |
        | status | String |
        | action | String |
        | enabled | Boolean |

        *Examples*:
        | ${info} | Quarantines Get Detailed Info All |
        | Log Dictionary | ${info} |
        | ${qa}= | Get Dictionary Keys  ${info} |
        | Log | Quarantines: ${qs} |
        | Log | Messages in Policy Quarantine:${info.Policy.messages} |
        """
        self._info('Get detailed list of configured quarantines')
        self._open_page()
        names = self._get_element_list(QUARANTINES_TABLE, only_clickable=exclude_disabled, dont_count_last_nrows=1)
        quarantines = CfgHolder()
        for name in names:
            quarantines[name] = self._get_quarantine_row_in_table(name)
        return quarantines

    def quarantines_get_detailed_info(self, name=None):
        """
        Get detailed info about quarantine.
        Greps information from the quarantines table.

        *Parameters*:
        - `name`: Name of the quarantine.

        *Return*:
        Dictionary(CfgHolder).
        Dictionary has keys:
        | _Keys_ | _Values types_ |
        | messages | String |
        | status | String |
        | action | String |
        | enabled | Boolean |

        *Examples*:
        | ${res}= | Quarantines Get Detailed Info |
        | ... | name=Policy |
        | Log Dictionary | ${res} |
        | Log | Action: ${res.action} |
        | Log | Messages: ${res.messages} |
        | Log | Status: ${res.status} |
        | Log | Enabled: ${res.enabled} |
        | Should Be True | ${res.enabled} |
        """
        self._info('Get detailed information for quarantine: %s' % name)
        self._open_page()
        return self._get_quarantine_row_in_table(name)
