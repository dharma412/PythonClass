#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/monitor/quarantines/qcommon.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from locators import *
from common.gui.guiexceptions import GuiValueError
from common.gui.guicommon import GuiCommon
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
import time
from qexceptions import NoSuchQuarantine, QuarantineIsNotEnabled, QuarantinesAcceesDenied


class QuarantinesCommon(GuiCommon):
    """
    Class that has common methods to manage quarantines.
    """

    def _open_page(self):
        self._navigate_to('Monitor', 'Policy, Virus and Outbreak Quarantines')
        text = 'You do not have access to any Quarantines'
        if self._is_text_present(text):
            raise QuarantinesAcceesDenied(text)

    def _not_impl(self, name):
        _self = getattr(name, '__name__')
        msg = "%s: can't get settings yet!" % _self
        raise NotImplementedError(msg)

    def _is_quarantine_present(self,
                               name,
                               strict_match=False,
                               only_clickable=False):
        """
        Shared method to check quarantine presence.
        """
        self._debug('Checking quarantine presence: %s' % name)
        try:
            return self._get_element_index_by_name(QUARANTINES_TABLE,
                                                   name,
                                                   strict_match=strict_match,
                                                   only_clickable=only_clickable)
        except ValueError as err:
            self._debug(err)
            raise NoSuchQuarantine(name)

    def _click_submit_button_custom(self,
                                    ok_text,
                                    cancel_text,
                                    need_confirm=True,
                                    confirm=True):
        """
        Need this instead of _click_submit_button from guicommon.py because
        1. it has wrong locators
        2. very long delay on confirm dialog with/without timer. don't know why???
        This method works match faster than _click_submit_button from guicommon.py
        """
        if need_confirm:
            tmr = CountDownTimer(15).start()
            while tmr.is_active():
                time.sleep(1)
                if self._is_visible(COMMON_CONFIRM_DIALOG):
                    if confirm:
                        self.click_button \
                            (COMMON_CONFIRM_OK_CANCEL_BUTTON(ok_text))
                    else:
                        self.click_button \
                            (COMMON_CONFIRM_OK_CANCEL_BUTTON(cancel_text), "don't wait")
                    self._debug \
                        ("Time elapsed while waiting for confirm dialog: %s" % \
                         tmr.time_elapsed())
                    break
        else:
            self._click_submit_button()

    def _get_edit_quarantine_link(self, name):
        """
        Return edit link if possible.
        """
        self._debug('Getting edit link for quarantine: %s' % name)
        row_idx, col_idx = self._is_quarantine_present(name)
        return "%s//tr[%s]/td[1]/a[text()='%s']" % (QUARANTINES_TABLE, row_idx, name)

    def _open_edit_quarantine_page(self, quarantine_name=None):
        """
        Open quarantine to edit, does not matter - active or not.
        """
        self._debug('Opening Edit quarantine page: %s' % quarantine_name)
        if quarantine_name:
            self._open_page()
            link = self._get_edit_quarantine_link(quarantine_name)
            self.click_element(link)

    def _is_enabled(self, idx):
        """
        Check if quarantine is enabled.
        """
        st = self.get_text("%s//tr[%s]/td[1]/a" % (QUARANTINES_TABLE, idx))
        if st.lower() == 'enable':
            return False
        else:
            return True

    def _is_active(self, name, strict_match=True, only_clickable=True):
        """
        Check if quarantine is active.
        """
        self._debug('Checking if quarantine is active: %s' % name)
        try:
            self._get_element_index_by_name(QUARANTINES_TABLE,
                                            name,
                                            strict_match=strict_match,
                                            only_clickable=only_clickable)
            return True
        except ValueError:
            return False

    def _get_status(self, idx):
        """
        Get status - % full.
        """
        self._debug('Getting percentage of space used')

        return self.get_text \
            ("%s//tr[%s]/td[4]/div[2]" % (QUARANTINES_TABLE, idx))

    def _get_type(self, idx):
        """
        Get type of the quarantine.
        """
        self._debug('Getting type of the quarantine')

        return self.get_text("%s//tr[%s]/td[2]" % (QUARANTINES_TABLE, idx))

    def _get_messages(self, idx):
        """
        Get num of messages.
        """
        self._debug('Getting number of messages in quarantine')
        return self.get_text("%s//tr[%s]/td[3]" % (QUARANTINES_TABLE, idx))

    def _get_def_action(self, idx):
        """
        Get default action.
        """
        self._debug('Getting default action used by quarantine')
        return self.get_text("%s//tr[%s]/td[4]" % (QUARANTINES_TABLE, idx))

    def _get_last_message_quarantined_on(self, idx):
        """
        Get default action.
        """
        self._debug('Getting Last Message Quarantined On')
        return self.get_text("%s//tr[%s]/td[5]" % (QUARANTINES_TABLE, idx))

    def _get_size(self, idx):
        """
        Get default action.
        """
        self._debug('Getting Last Message Quarantined On')
        return self.get_text("%s//tr[%s]/td[6]" % (QUARANTINES_TABLE, idx))

    def _get_quarantine_row_in_table(self, name):
        """
        Gather all data from row for given quarantine.
        """
        row_idx, col_idx = self._is_quarantine_present(name)
        quarantine = CfgHolder()
        quarantine.enabled = self._is_enabled(row_idx)
        quarantine.messages = self._get_messages(row_idx)
        quarantine.action = self._get_def_action(row_idx)
        quarantine.type = self._get_type(row_idx)
        quarantine.last_quarantined = self._get_last_message_quarantined_on(row_idx)
        quarantine.size = self._get_size(row_idx)
        return quarantine

    def _clear_all_checkboxes_in_dialog(self, dialog):
        """
        Clear all checkboxes in users/groups/roles dialog.
        """
        self._debug('Clearing all checkboxes in: %s' % dialog)
        rows = \
            int(self.get_matching_xpath_count("%s//*[@type='checkbox']" % dialog))
        for row in xrange(2, rows + 2):
            self._unselect_checkbox \
                ("%s//tr[%s]//*[@type='checkbox']" % (dialog, row))
        return rows

    def _do_confirm(self, dialog, confirm):
        if confirm:
            self.click_button \
                (QUARANTINE_DIALOGS_OK_BUTTON(dialog), "don't wait")
        else:
            self.click_button \
                (QUARANTINE_DIALOGS_CANCEL_BUTTON(dialog), "don't wait")

    def _set_items(self,
                   link,
                   dialog,
                   checkbox_identity,
                   items,
                   err_mess,
                   not_found,
                   confirm):
        """
        Common method to set users/groups.
        """
        if not self._is_element_present(link):
            raise ValueError(err_mess)
        self.click_element(link, "don't wait")
        self._clear_all_checkboxes_in_dialog(dialog)
        # allow to pass ${EMPTY} to clear all items
        if items == '':
            self._do_confirm(dialog, confirm)
            return
        for item in self._convert_to_tuple(items):
            _item = "%s//*[@id='%s_%s_checkbox']" % \
                    (dialog, checkbox_identity, item)
            # (dialog, checkbox_identity, item.lower())
            if self._is_element_present(_item):
                self._select_checkbox(_item)
            else:
                raise ValueError('%s: %s' % (not_found, item))
        self._do_confirm(dialog, confirm)

    def _set_local_users(self, local_users, confirm):
        """
        Use _set_items to set users.
        """
        if local_users is None:
            return None
        self._debug('Set local users allowed to access the quarantine')
        err = 'No Local Users found for assignment'
        not_found = 'User not found for assignment'
        self._set_items(QUARANTINE_USERS_LINK,
                        QUARANTINE_USERS_DIALOG,
                        'users',
                        local_users,
                        err,
                        not_found,
                        confirm)

    def _set_ext_groups(self, ext_groups, confirm):
        """
        Use _set_items to set groups.
        """
        if ext_groups is None:
            return None
        self._debug('Set external auth groups allowed to access the quarantine')
        err = 'No External Groups found for assignment'
        not_found = 'External Group not found for assignment'
        self._set_items(QUARANTINE_EXT_GROUPS_LINK,
                        QUARANTINE_EXT_GROUPS_DIALOG,
                        'groups',
                        ext_groups,
                        err,
                        not_found,
                        confirm)

    def _set_custom_roles_common(self, link, dialog, custom_roles, confirm):
        """
        Common method to set roles.
        """
        if custom_roles is None:
            return None
        self._debug('Set custom roles allowed to access the quarantine')
        if not self._is_element_present(link):
            raise ValueError("No Custom Roles found for assignment")
        ROLE_NAME = lambda row: "%s//tr[%d]/td[2]/label" % (dialog, row)
        ROLE_CHECKBOX = lambda row: "%s//tr[%d]/td/input" % (dialog, row)
        self.click_element(QUARANTINE_CUSTOM_ROLES_LINK, "don't wait")
        rows = self._clear_all_checkboxes_in_dialog(dialog)
        # allow to pass ${EMPTY} to clear all items and return
        if custom_roles == '':
            self._do_confirm(dialog, confirm)
            return
        for role in self._convert_to_tuple(custom_roles):
            found = False
            for row in range(2, rows + 2):
                if str(self.get_text(ROLE_NAME(row))) == role:
                    self._select_checkbox(ROLE_CHECKBOX(row))
                    found = True
            if not found:
                raise ValueError("%s role not found for assignment" % role)
        self._do_confirm(dialog, confirm)

    def _set_custom_roles(self, custom_roles, confirm):
        """
        Use _set_custom_roles_common to set roles.
        """
        self._set_custom_roles_common(QUARANTINE_CUSTOM_ROLES_LINK,
                                      QUARANTINE_CUSTOM_ROLES_DIALOG,
                                      custom_roles,
                                      confirm)

    def _get_result(self):
        try:
            res, msg = self._check_action_result()
            result = '%s: %s' % (res, msg)
        except GuiValueError as err:
            result = err
        return result
