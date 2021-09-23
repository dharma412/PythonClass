#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/monitor/quarantines/virus.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from quarantine import Quarantine


class VirusQuarantine(Quarantine):
    """
    Class to work with Virus Quarantine.
    """
    virus = 'Virus'

    def quarantines_virus_edit(self,
                               retain_time=None,
                               retain_action=None,
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
        Edit Virus quarantine.
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
        - `free_up_space`:  Free up space by applying default action on messages upon space overflow
                            Boolean
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
        | Quarantines Edit |
        | ... | name=Virus |
        | ... | retain_time=2 days |
        | ... | retain_action=delete |
        | ... | local_users=oper1, guest1 |

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.
        - `QuarantineIsNotEnabled`: If quarantine is not enabled (no edit link).
        """
        self._info('Edit quarantine: %s' % self.virus)
        self._open_edit_quarantine_page(quarantine_name=self.virus)
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

    def quarantines_virus_get_settings(self):
        """
        Not implemented. Should parse page...
        """
        self._not_impl(self.quarantine_policy_get_settings)
        self._info('Get quarantine settings: %s' % self.virus)
        self._open_page()

    def quarantines_virus_is_active(self):
        """
        Check if Virus quarantine is active.
        It is active if it is click-able.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Exceptions*:
        - `NoSuchQuarantine`: If there is no such quarantine.

        *Examples*:
        | ${res}= | Quarantines Virus Is Active |
        | Should Be True | ${res} |
        """
        self._info('Check if quarantine is active: %s' % self.virus)
        self._open_page()
        return self._is_active(self.virus)
