#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/monitor/quarantines/quarantine.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from locators import *
from qcommon import QuarantinesCommon
from common.gui.decorators import set_speed
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon, Wait
import common.gui.guiexceptions as guiexceptions
import re


class Quarantine(QuarantinesCommon):
    """
    Class to manage all quarantines excluding Spam Quarantine.
    """

    def _add_edit_quarantine(self,
                             name=None,
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
        retain_actions = ('delete', 'release')
        self._input_text_if_not_none(QUARANTINE_NAME, name)
        # expect correct order when 1st is digit and 2nd are units
        # allow user to provide
        # a) only digit(retain number) b) only units c) number and units
        retain_time_value = retain_time_units = None
        if retain_time is not None:
            retain_time_value = \
                re.split('\D+', retain_time)[0].strip() or None  # get retain time
            retain_time_units = \
                re.split('\d+', retain_time)[1].strip() or None  # get retain time units
        self._input_text_if_not_none \
            (QUARANTINE_RETAIN_PERIOD, retain_time_value)
        retain_time_units = retain_time_units.lower().title()
        self.click_element(QUARANTINE_RETAIN_PERIOD_UNITS(retain_time_units))
        if retain_action is not None:
            if retain_action not in retain_actions:
                raise ValueError \
                    ("Invalid retain action: %s. Must be one from: %s" % \
                     (retain_action, ', '.join(retain_actions)))
            self._click_radio_button \
                (QUARANTINE_DEFAULT_ACTION(retain_action))
        self._select_unselect_checkbox \
            (QUARANTINE_FREE_UP_SPACE, free_up_space)
        if self._is_checked(QUARANTINE_DEFAULT_ACTION("release")) \
                and self._is_checked(QUARANTINE_FREE_UP_SPACE):
            if subject_tag is not None:
                self._select_unselect_checkbox \
                    (QUARANTINE_MOD_SUBJ_ENABLE, subject_tag)
                if self._is_checked(QUARANTINE_MOD_SUBJ_ENABLE):
                    self.click_element(QUARANTINE_MOD_SUBJ_TAG(subject_tag.lower()))
                    self._input_text_if_not_none \
                        (QUARANTINE_TAG_SUBJ_ON_RELEASE, subject_tag_value)
            if header is not None:
                self._select_unselect_checkbox(QUARANTINE_X_HEADER_ENABLE, header)
                if self._is_checked(QUARANTINE_X_HEADER_ENABLE):
                    self._input_text_if_not_none \
                        (QUARANTINE_X_HEADER_NAME, header)
                    self._input_text_if_not_none \
                        (QUARANTINE_X_HEADER_VALUE, header_value)
            self._select_unselect_checkbox \
                (QUARANTINE_STRIP_ATTACHMENTS_ON_RELEASE, strip_attachments)

        self._set_local_users(local_users, confirm)
        self._set_ext_groups(ext_auth_groups, confirm)
        self._set_custom_roles(custom_roles, confirm)
        self._click_submit_button()

    def quarantines_add(self,
                        name=None,
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
        Add quarantine.

        *Parameters*:
        - `name`: The name of the quarantine.
        - `retain_time`: Time to wait before action applied. Values like 40Hours, 5 days are correct.
        Case insensitive. Options are:
        | Hours |
        | Days |
        - `retain_action`: Action to apply for messages.
        Case insensitive. Options are:
        | Release |
        | Delete |
        - `free_up_space`:  Free up space by applying default action on messages upon space overflow. Boolean.
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
        | Quarantines Add |
        | ... | name=${q1} |
        | ... | retain_time=5 days |
        | ... | retain_action=release |
        | ... | subject_tag=append |
        | ... | subject_tag_value=[From${q1}] |
        | ... | header=WasQuarantined |
        | ... | header_value=${q1} |
        | ... | strip_attachments=${True} |
        | ... | local_users=guest1, help1 |
        | ... | ext_auth_groups=operators |
        | ... | custom_roles=role1, role2 |

        | Quarantines Add |
        | ... | name=${q3} |
        | ... | size=333 |
        | ... | retain_time=13 hours |
        | ... | retain_action=delete |
        """
        self._info('Add new quarantine: %s' % name)
        self._open_page()
        self.click_button(QUARANTINE_ADD_BUTTON)
        self._add_edit_quarantine(name=name,
                                  retain_time=retain_time,
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

    def quarantines_edit(self,
                         name=None,
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
        Edit quarantine.

        *Parameters*:
        - `name`: The name of the quarantine to edit.
        - `size`: Space allocated for quarantine.
        - `retain_time`: Time to wait before action applied.
        Values like 40Hours, 5 days are correct.
        Case insensitive. Options are:
        | Hours |
        | Days |
        - `retain_action`: Action to apply for messages. Case insensitive. Options are:
        | Release |
        | Delete |
        - `free_up_space`:  Free up space by applying default action on messages upon space overflow. Boolean.
        - `subject_tag`: Tag subject. Case insensitive. Options are:
        | Prepend |
        | Append |
        Pass ${False} if you want to un-select this option.
        - `subject_tag_value`: Tag subject value.
        - `header`: Header of message. Pass ${False} if you want to un-select this option.
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
        | Quarantines Edit |
        | ... | name=${q3} |
        | ... | size=555 |
        | ... | retain_time=3 days |
        | ... | retain_action=release |
        | ... | subject_tag=append |
        | ... | subject_tag_value=[From${q3}] |
        | ... | header=WasQuarantined |
        | ... | header_value=${q3} |
        | ... | strip_attachments=${False} |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).
        """
        self._info('Edit quarantine: %s' % name)
        self._open_edit_quarantine_page(quarantine_name=name)
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

    def quarantines_delete(self, name=None, confirm=True):
        """
        Delete quarantine.

        *Parameters*:
        - `name`: The name of the quarantine to be deleted.

        *Return*:
        None

        *Examples*:
        | Quarantines Delete |
        | ... | name=SomeQ |
        """
        self._info('Delete quarantine: %s' % name)
        self._open_page()
        row_idx, col_idx = self._is_quarantine_present(name)
        self.click_element(QUARANTINE_DELETE_LINK(row_idx), "don't wait")
        if confirm:
            self.click_button(QUARANTINE_DELETE_CONFIRM_BUTTON)
        else:
            self.click_button(QUARANTINE_DELETE_CONFIRM_BUTTON, "don't wait")

    def _get_settings_from_dialog_link(self, locator, text_marker):
        if self._is_element_present(locator):
            text = self.get_text(locator)
            if text_marker in text.lower():
                return []
            else:
                return text.split(',')

    @set_speed(0)
    def _get_settings(self):
        # have to use such 'hard-coded' method because:
        # 1. different classes/attributes are set to rows in settings table
        # 2. there are different html tags that represent options
        # (checkboxes, radio-buttons, dropdown etc)
        # 3. not all rows have same attributes set.
        # 4. the ui is horror, for example, tables are done using </br> tags.
        self.wait_until_page_loaded(timeout=10)
        # TODO need this sleep because can't track page loaded event
        import time
        time.sleep(5)
        settings = CfgHolder()
        row_loc = lambda lookup_text: \
            "//*[@id='form']//table[@class='pairs']//tr[contains(.,'%s')]/td" % (lookup_text)
        settings.quarantine_name = self.get_text(row_loc('Quarantine Name'))
        created_on_by_size = \
            [val.strip() for val in self.get_text(row_loc('Created On')).split('\n')]
        settings.created_on, settings.created_by, settings.size = created_on_by_size
        settings.retention_period = self.get_value(QUARANTINE_RETAIN_PERIOD)
        settings.retention_period_units = \
            self._get_selected_label(QUARANTINE_RETAIN_PERIOD_UNITS_GETVAL)
        if self._is_element_present \
                    ("//input[@id='defaultAction_delete' and @checked='checked']"):
            settings.default_action = 'delete'
        elif self._is_element_present \
                    ("//input[@id='defaultAction_release' and @checked='checked']"):
            settings.default_action = 'release'

        settings.free_up_sapce = False
        if self._is_element_present \
                    ("//input[@id='automatic_action' and @checked='checked']"):
            settings.free_up_sapce = True

        settings.modify_subject = False
        settings.modify_subject_option = None
        settings.modify_subject_text = None
        if self._is_element_present \
                    ("//input[@id='modify_subj' and @checked='checked']"):
            settings.modify_subject = True
            settings.modify_subject_option = \
                self._get_selected_label(QUARANTINE_MOD_SUBJ_ON_RELEASE)
            settings.modify_subject_text = \
                self.get_value(QUARANTINE_TAG_SUBJ_ON_RELEASE)

        settings.add_xheader = False
        settings.xheader_name = None
        settings.xheader_text = None
        if self._is_element_present \
                    ("//input[@id='add_xheader' and @checked='checked']"):
            settings.add_xheader = True
            settings.xheader_name = self.get_value(QUARANTINE_X_HEADER_NAME)
            settings.xheader_text = self.get_value(QUARANTINE_X_HEADER_VALUE)

        settings.strip_attachments = False
        if self._is_element_present \
                    ("//input[@id='strip_attachments' and @checked='checked']"):
            settings.strip_attachments = True

        settings.local_users = self._get_settings_from_dialog_link \
            (QUARANTINE_USERS_LINK, 'no users selected')
        settings.external_users = self._get_settings_from_dialog_link \
            (QUARANTINE_EXT_GROUPS_LINK, 'no users selected')
        settings.custom_roles = self._get_settings_from_dialog_link \
            (QUARANTINE_CUSTOM_ROLES_LINK, 'no roles selected')

        filters_and_actions_loc = \
            "//*[@id='references']//table/tbody[@class='yui-dt-data']"
        settings.filters_and_actions = {}
        timer = CountDownTimer(10).start()
        while timer.is_active():
            try:
                rows_num = int(self.get_matching_xpath_count("%s/tr" % filters_and_actions_loc))
                break
            except Exception as e:
                rows_num = 0
        if not rows_num:
            return settings
        for row in xrange(1, rows_num + 1):
            rloc = "%s/tr[%s]" % (filters_and_actions_loc, row)
            filter_action_name = self.get_text("%s/td[1]" % (rloc,))
            filter_action_type = self.get_text("%s/td[2]" % (rloc,))
            settings.filters_and_actions[filter_action_name] = filter_action_type
        return settings

    def quarantines_get_settings(self, name):
        """
        Return settings of Quarantine.

        *Parameters*:
        - `name`: The name of the Quarantine.

        *Return*:
        Dictionary(CfgHolder).
        | Key | Value type |
        | quarantine_name | String |
        | created_on | String |
        | created_by | String |
        | size | String |
        | retention_period | String |
        | retention_period_units | String |
        | default_action | String |
        | free_up_sapce | Boolean |
        | modify_subject | Boolean |
        | modify_subject_option | String or None |
        | add_xheader | Boolean |
        | xheader_name | String or None |
        | xheader_text | String or None |
        | strip_attachments | Boolean |
        | local_users | List |
        | external_users | List |
        | custom_roles | List |
        | filters_and_actions | Dictionary or None |

        *Examples*:
        | ${settings}= | Quarantines Get Settings | ${TEST_ID} |
        | Should Be Equal | ${settings.quarantine_name} | ${TEST_ID} |
        | Should Be Equal | ${settings.created_by} | ${DUT_ADMIN} |
        | Should Be Equal | ${settings.size} | 0B |
        | Should Be Equal | ${settings.local_users} | ${None} |
        | Should Be Equal | ${settings.external_users} | ${None} |
        | Should Contain | ${settings.filters_and_actions.keys()} | ${TEST_ID} |
        """
        self._info('Get settings of quarantine: %s' % name)
        self._open_edit_quarantine_page(quarantine_name=name)
        return self._get_settings()

    def quarantines_is_active(self, name=None):
        """
        Check if quarantine is active.
        It is active if it is click-able.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        None

        *Examples*:
        | ${res} | Quarantines Spam Is Active |
        | Log | ${res} |
        """
        self._info('Check if quarantine is active: %s' % name)
        self._open_page()
        return self._is_active(name)
