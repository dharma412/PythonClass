#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/monitor/quarantines/policy.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from locators import *
from quarantine import Quarantine


class PolicyQuarantine(Quarantine):
    """
    Class to work with Policy Quarantine.
    """
    policy = 'Policy'

    def quarantines_policy_edit(self,
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
        Edit Policy quarantine.
        The same can be done with `Quarantines Edit` keyword.

        *Parameters*:
        - `retain_time`: Time to wait before action applied.
        Values like 15 minutes, 40Hours, 5 days are correct.
        Case insensitive. Options are:
        | Minutes |
        | Hours |
        | Days |
        - `retain_action`: Action to apply for messages. Case insensitive. Options are:
        | Release |
        | Delete |
        - `free_up_space`:  Free up space by applying default action on messages upon
                            space overflow. Boolean
        - `subject_tag`: Tag subject. Case insensitive. Options are:
        | Prepend |
        | Append |
        Pass ${False} if you want to un-select this option.
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
        | Quarantines Policy Edit |
        | ... | retain_time=200 hours |
        | ... | retain_action=release |
        | ... | subject_tag=prepend |
        | ... | subject_tag_value=PolicyQ |
        | ... | header=X-Policy |
        | ... | header_value=Quarantined |
        | ... | strip_attachments=${False} |
        | ... | local_users=oper1 |
        | ... | ext_auth_groups=operators |
        | ... | custom_roles=role2 |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).
        """
        self._info('Edit quarantine: %s' % self.policy)
        self._open_edit_quarantine_page(quarantine_name=self.policy)
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

    def quarantines_policy_delete(self, confirm=True):
        """
        Delete Policy quarantine.
        The same can be done with `Quarantines Delete` keyword.

        *Parameters*:
        None

        *Return*:
        None

        *Examples*:
        | Quarantines Policy Delete |

        | Quarantines Policy Delete | confirm=${False} |
        """
        self._info('Delete quarantine: %s' % self.policy)
        self._open_page()
        row_idx, col_idx = self._is_quarantine_present(self.policy)
        self.click_element(QUARANTINE_DELETE_LINK(row_idx), "don't wait")
        if confirm:
            self.click_button(QUARANTINE_DELETE_CONFIRM_BUTTON, "don't wait")
        else:
            self.click_button(QUARANTINE_DELETE_CONFIRM_BUTTON, "don't wait")

    def quarantines_policy_get_settings(self):
        """
        Not implemented. Should parse page...
        """
        self._not_impl(self.quarantine_policy_get_settings)
        self._info('Get quarantine settings: %s' % self.policy)
        self._open_page()

    def quarantines_policy_is_active(self):
        """
        Check if Policy quarantine is active.
        It is active if it is click-able.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        None

        *Examples*:
        | ${res} | Quarantines Policy Is Active |
        | Should Be True | ${res} |
        """
        self._info('Check if quarantine is active: %s' % self.policy)
        self._open_page()
        return self._is_active(self.policy)
