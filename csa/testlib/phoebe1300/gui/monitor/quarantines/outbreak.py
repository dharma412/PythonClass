#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/monitor/quarantines/outbreak.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from locators import *
from sal.containers.cfgholder import CfgHolder
from quarantine import Quarantine
from search import Search
from qexceptions import NoSuchRuleId, QuarantineIsNotEnabled
from common.gui.decorators import set_speed

OUTBREAK = 'Outbreak'


class OutbreakQuarantine(Quarantine):
    """
    Class to work with Outbreak Quarantine.
    """

    def quarantines_outbreak_edit(self,
                                  retain_time=None,
                                  retain_action=None,
                                  free_up_space=None,
                                  subject_tag=None,
                                  subject_tag_value=None,
                                  header=None,
                                  header_value=None,
                                  strip_attachments=None,
                                  local_users=None,
                                  ext_auth_groups=None,
                                  custom_roles=None,
                                  confirm=True):
        """
        Edit Outbreak quarantine.
        The same can be done with `Quarantines Edit` keyword.

        *Parameters*:
        - `retain_time`: Time to wait before action applied.
        Values like 15 minutes, 40Hours, 5 days are correct.
        Case insensitive. Options are:
        | Minutes |
        | Hours |
        | Days |
        - `retain_action`: Action to apply for messages.
        Case insensitive. Options are:
        | Release |
        | Delete |
        - `free_up_space`:  Free up space by applying default action on messages upon
                            space overflow. Boolean
        - `subject_tag`: Tag subject. Case insensitive. Options are:
        | Prepend |
        | Append |
        - `subject_tag_value`: Tag subject value.
        - `header`: Header of message.
        - `header_value`: Value of header.
        - `strip_attachments`: Strip attachments or not. Boolean.
        - `local_users`: Local users. String of comma separated values.
        ${EMPTY} to clear settings.
        - `ext_auth_groups`: External groups. String of comma separated values.
        ${EMPTY} to clear settings.
        - `custom_roles`: Custom roles. String of comma separated values.
        ${EMPTY} to clear settings.
        - `confirm`: Confirm applies to users/groups/roles settings dialog. Boolean.

        *Return*:
        None

        *Examples*:
        | Quarantines Outbreak Edit |
        | ... | retain_time=80 hours |
        | ... | retain_action=release |
        | ... | subject_tag=append |
        | ... | subject_tag_value=[OF] |
        | ... | header=X-OF |
        | ... | header_value=Quarantined |
        | ... | strip_attachments=${True} |
        | ... | local_users=${EMPTY} |
        | ... | ext_auth_groups=operators |

        *Exceptions*:
        `NoSuchQuarantine`: If there is no such quarantine.
        `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).
        """
        self._info('Edit quarantine: %s' % OUTBREAK)
        self._open_edit_quarantine_page(quarantine_name=OUTBREAK)
        self._add_edit_quarantine(retain_time=retain_time,
                                  retain_action=retain_action,
                                  free_up_space=free_up_space,
                                  subject_tag=subject_tag,
                                  subject_tag_value=subject_tag_value,
                                  header=header,
                                  header_value=header_value,
                                  strip_attachments=strip_attachments,
                                  local_users=local_users,
                                  ext_auth_groups=ext_auth_groups,
                                  custom_roles=custom_roles,
                                  confirm=confirm)

    def quarantines_outbreak_get_settings(self):
        """
        Not implemented. Should parse page...
        """
        self._not_impl(self.quarantine_policy_get_settings)
        self._info('Get quarantine settings: %s' % OUTBREAK)
        self._open_page()

    def quarantines_outbreak_is_active(self):
        """
        Check if Outbreak quarantine is active.
        It is active if it is click-able.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Outbreak Is Active |
        | Should Not Be True | ${res} |
        """
        self._info('Check if quarantine is active: %s' % OUTBREAK)
        self._open_page()
        return self._is_active(OUTBREAK)


class OutbreakQuarantineManageByRule(Search):

    def _click_manage_by_rule_link(self):
        if self._is_active(OUTBREAK):
            self.click_element(OUTBREAK_MANAGE_BY_RULE_SUMMARY_LINK)
        else:
            raise QuarantineIsNotEnabled(OUTBREAK)

    def _count_rows(self):
        return int(self.get_matching_xpath_count \
                       ("%s//tr[not(contains(th, 'Totals'))]" % QUARANTINES_TABLE))

    def _select_rule_by_name(self, rows, name):
        _found = None
        for row in xrange(1, rows + 1):
            if self._is_element_present("%s//tr[%s]/td[2]/a[text()='%s']" % \
                                        (QUARANTINES_TABLE, row, name)):
                _found = row
                break
        if _found:
            self._select_checkbox \
                ("%s//tr[%s]/td[1]/input" % (QUARANTINES_TABLE, _found))
        else:
            raise NoSuchRuleId(name)

    def _select_rules(self, rule_id=None, all=False):
        if rule_id is not None:
            rows = self._count_rows()
            for rule in self._convert_to_tuple(rule_id):
                self._select_rule_by_name(rows, rule)
        if all:
            self._select_checkbox(QUARANTINE_SEARCH_TABLE_SELECT_ALL_MIDS)

    def _do_action(self, action, rule_id=None, all=False):
        self._handle_no_messages_found(err='No messages were found')
        self._select_rules(rule_id=rule_id, all=all)
        self.select_from_dropdown_list \
            (QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION, action)
        self.click_button(QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_SUBMIT)
        return self._get_result()

    def _grep_single_row(self,
                         row_idx,
                         cols_names,
                         rule_as_key=False):
        data = CfgHolder()
        _grep = lambda row_idx, col_idx: \
            self.get_text("%s//tr[%s]/td[%s]" % (QUARANTINES_TABLE, row_idx, col_idx))
        for col_idx, name in enumerate(cols_names[1:], 2):
            data.__setattr__(self._normalize(name),
                             _grep(row_idx, col_idx))
        if rule_as_key:
            rid = data.pop('rule_id')
            data_by_rule = CfgHolder()
            data_by_rule.__setattr__(rid, data)
            return data_by_rule
        return data

    @set_speed(0)
    def _grep_summary_table(self, rule_as_key=False):
        self._handle_no_messages_found(err='No messages were found')
        res = []
        cols_num = \
            int(self.get_matching_xpath_count("%s//tr[1]/th" % QUARANTINES_TABLE))
        cols_names = [self.get_text("%s//tr[1]/th[%s]" % (QUARANTINES_TABLE, col)) \
                      for col in xrange(1, cols_num + 1)]
        rows = self._count_rows()
        for row in xrange(2, rows + 1):
            res.append(self._grep_single_row \
                           (row, cols_names, rule_as_key=rule_as_key))
        return res

    def quarantines_outbreak_manage_by_rule_release(self,
                                                    rule=None,
                                                    all=False):
        """
        Release all messages matching outbreak rule.
        Action is done from Outbreak Quarantine Summary by action on certain rule.

        *Parameters*:
        - `rule`: Rule Id as it is seen in WUI.
        - `all`: Select all rules. Boolean.

        *Return*:
        Result of action represented as string.

        *Exceptions*:
        - `QuarantineIsNotEnabled`: If outbreak quarantine is disabled.

        *Examples*:
        | ${res}= | Quarantines Outbreak Manage By Rule Release | rule=${stove_manual} |
        | Log | ${res} |
        """
        self._open_page()
        self._click_manage_by_rule_link()
        return self._do_action('Release', rule_id=rule, all=all)

    def quarantines_outbreak_manage_by_rule_delete(self,
                                                   rule=None,
                                                   all=False):
        """
        Delete all messages matching outbreak rule.
        Action is done from Outbreak Quarantine Summary by action on certain rule.

        *Parameters*:
        - `rule`: Rule Id as it is seen in WUI.
        - `all`: Select all rules. Boolean.

        *Return*:
        Result of action represented as string.

        *Exceptions*:
        - `QuarantineIsNotEnabled`: If outbreak quarantine is disabled.

        *Examples*:
        | ${res}= | Quarantines Outbreak Manage By Rule Delete | rule=${adaptive_rule} |
        | Log | ${res} |
        """
        self._open_page()
        self._click_manage_by_rule_link()
        return self._do_action('Delete', rule_id=rule, all=all)

    def quarantines_outbreak_manage_by_rule_parse_summary_table(self, rule_as_key=False):
        """
        Parse Outbreak Quarantine Summary Table.

        *Parameters*:
        - `rule_as_key`: Boolean. If ${True} - result will contain rules as keys.

        *Return*:
        List of dictionaries.
        Each dictionary(CfgHolder) has such keys.
        | _Keys_ |
        | rule_id |
        | rule_description |
        | capacity |
        | total_size |
        | average_message_size |
        | number_of_messages |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Outbreak quarantine is not enabled.

        *Examples*:
        | @{res}= | Quarantines Outbreak Manage By Rule Parse Summary Table | rule_as_key=${True} |
        | :FOR | ${r} | IN  @{res} |
        | \  Log Dictionary | ${r} |
        | \  Log | ${r.${adaptive_rule}.number_of_messages} |
        """
        self._open_page()
        self._click_manage_by_rule_link()
        return self._grep_summary_table(rule_as_key=rule_as_key)

    def quarantines_outbreak_manage_by_rule_get_messages(self,
                                                         rule=None,
                                                         items_per_page=None,
                                                         mid_as_key=False):
        """
        Get all messages matching outbreak rule.

        *Parameters*:
        - `rule`: Rule Id as it is seen in WUI.
        - `items_per_page`: The page size (items per page to display).
        Options are as they seen in WUI.
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        - `mid_as_key`: Each element in result list will be a dictionary.
        Make MID value a key of dictionary or not. Boolean. False by default.

        *Return*:
        List of dictionaries.

        *Exceptions*:
        - `NoMessagesFound`: If there are no messages in quarantine.

        *Examples*:
        | ${res}= | Quarantines Outbreak Manage By Rule Get Messages | rule=${adaptive_rule} |
        | Log List | ${res} |
        """
        self._open_page()
        self._click_manage_by_rule_link()
        link = "%s//a[text()='%s']" % (QUARANTINES_TABLE, rule)
        if self._is_element_present(link):
            self.click_element(link)
            return self._get_all_messages(items_per_page=items_per_page,
                                          mid_as_key=mid_as_key)
        else:
            raise NoSuchRuleId(rule)
