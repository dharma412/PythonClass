#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/quarantine_config.py#1 $
# $ $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class QuarantineConfig(CliKeywordBase):
    """
    Configure system quarantines.
    CLI command: quarantineconfig
    """

    def get_keyword_names(self):
        return ['quarantine_config_new',
                'quarantine_config_edit',
                'quarantine_config_delete',
                'quarantine_config_outbreak_manage_release',
                'quarantine_config_outbreak_manage_delete',
                'quarantine_config_get_list',
                'quarantine_config_get_space_available', ]

    def quarantine_config_new(self, *args):
        """Create a new quarantine.

        CLI command: quarantineconfig > new

        *Parameters:*
        - `name`: The name for the quarantine.
        - `period`: Retention period for the quarantine.
        Use _d_ for days or _h_ for hours or _m_ for minutes.
        - `action`: Default action for quarantine.
        | 1 | Delete |
        | 2 | Release |
        - `modify_subj`: If `action` is _Release_ - modify the subject of messages that are released because quarantine overflows. YES or NO.
        - `text_pos`: If `modify_subj` is _Yes_ - position of text.
        | 1 | Prepend |
        | 2 | Append |
        - `text_to_add`: If `modify_subj` is _Yes_ - enter the text to add.
        - `add_header`: If `action` is _Release_ - add a custom header to messages that are released because quarantine overflows. YES or NO.
        - `header_name`: If `add_header` is _Yes_ - the header name.
        - `header_content`: The header content, or the word _DELETE_ to clear the content.
        - `strip_attachments`: Strip all attachments from messages that are released because of quarantine overflows. YES or NO.
        - `edit_user_roles`: Assign/Edit any user roles to access the quarantine. YES or NO.
        - `add_roles`: If `edit_user_roles` is _Yes_ - assign a user role(s). Select one or more user role names, separated by a comma.
        - `delete_roles`: If `edit_user_roles` is _Yes_ - un-assign a user role(s). Select one or more user role names, separated by a comma.
        - `apply_quarantines`: Apply rules automatically when quarantine space fills up. YES or NO

        *Return:*
        None

        *Examples:*
        | Quarantine Config New |
        | ... | name=${q1} |
        | ... | period=15m |
        | ... | action=release |
        | ... | modify_subj=yes |
        | ... | text_pos=append |
        | ... | text_to_add=[Quarantined to ${q1}] |
        | ... | add_header=yes |
        | ... | header_name=X-Quarantined |
        | ... | header_content=In-${q1} |
        | ... | strip_attachments=yes |

        | Quarantine Config New |
        | ... | name=${q2} |
        | ... | period=10h |
        | ... | action=delete |

        | Quarantine Config New |
        | ... | name=${q3} |
        | ... | period=1d |
        | ... | action=delete |
        | ... | edit_user_roles=yes |
        | ... | add_roles=${r1},${r2} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.quarantineconfig().new(**kwargs)

    def quarantine_config_edit(self, *args):
        """Modify a quarantine.

        CLI command: quarantineconfig > edit

        *Parameters:*
        - `name`: The name for the quarantine.
        - `period`: Retention period for the quarantine.
        Use _d_ for days or _h_ for hours or _m_ for minutes.
        - `action`: Default action for quarantine.
        | 1 | Delete |
        | 2 | Release |
        - `modify_subj`: If `action` is _Release_ - modify the subject of messages that are released because quarantine overflows. YES or NO.
        - `text_pos`: If `modify_subj` is _Yes_ - position of text.
        | 1 | Prepend |
        | 2 | Append |
        - `text_to_add`: If `modify_subj` is _Yes_ - enter the text to add.
        - `add_header`: If `action` is _Release_ - add a custom header to messages that are released because quarantine overflows. YES or NO.
        - `header_name`: If `add_header` is _Yes_ - the header name.
        - `header_content`: The header content, or the word _DELETE_ to clear the content.
        - `strip_attachments`: Strip all attachments from messages that are released because of quarantine overflows. YES or NO.
        - `edit_user_roles`: Assign/Edit any user roles to access the quarantine. YES or NO.
        - `add_roles`: If `edit_user_roles` is _Yes_ - assign a user role(s). Select one or more user role names, separated by a comma.
        - `delete_roles`: If `edit_user_roles` is _Yes_ - un-assign a user role(s). Select one or more user role names, separated by a comma.
        - `apply_quarantines`: Apply rules automatically when quarantine space fills up. YES or NO

        *Return:*
        None

        *Examples:*
        | Quarantine Config Edit |
        | ... | name=${q3} |
        | ... | period=2d |
        | ... | action=release |
        | ... | modify_subj=no |
        | ... | add_header=yes |
        | ... | header_name=X-Quarantined |
        | ... | header_content=In-${q3} |
        | ... | strip_attachments=no |
        | ... | edit_user_roles=yes |
        | ... | delete_roles=${r2} |

        | Quarantine Config Edit |
        | ... | name=${q1} |
        | ... | period=8h |
        | ... | action=release |
        | ... | modify_subj=yes |
        | ... | text_pos=prepend |
        | ... | text_to_add=[In ${q1}] |
        | ... | add_header=no |
        | ... | strip_attachments=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.quarantineconfig().edit(**kwargs)

    def quarantine_config_delete(self, *args):
        """Remove a quarantine.

        CLI command: quarantineconfig > delete

        *Parameters:*
        - `name`: The name of the quarantine.
        - `confirm`: Confirm delete operation. YES or NO. YES by default.

        *Return:*
        None

        *Examples:*
        | Quarantine Config Delete |
        | ... | name=${q1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.quarantineconfig().delete(**kwargs)

    def quarantine_config_get_list(self, *args):
        """Get list of configured quarantines.

        CLI command: quarantineconfig

        *Parameters:*
        - `as_dictionary`: Format result as dictioanry. Else return raw output.

        *Return:*
        Dictionary(CfgHolder) or raw output.
        Dictionary's keys are names of quarantines.
        May look like:
        Dictionary size is 5 and it contains following items:
        Outbreak: {'retention': 'Varies', 'full': 'empty', 'messages': '0', 'size': '3,072'}
        Policy: {'retention': '10d', 'full': 'empty', 'messages': '0', 'size': '1,024'}
        Virus: {'retention': '30d', 'full': 'empty', 'messages': '0', 'size': '2,048'}
        quarantine1: {'retention': '5d', 'full': 'N/A', 'messages': 'N/A', 'size': '500'}
        quarantine2: {'retention': '10h', 'full': 'N/A', 'messages': 'N/A', 'size': '300'}

        Each dictionary has following keys:
        * _retention_
        * _full_
        * _messages_
        * _size_

        *Examples:*
        | ${quarantines}= | Quarantine Config Get List |
        | Log Dictionary | ${quarantines} |
        | Should Be Equal | ${quarantines.${q1}.size} | 333 |
        | Should Be Equal | ${quarantines.${q1}.retention} | 1d |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.quarantineconfig(). \
            get_list_of_configured_quarantines(**kwargs)

    def quarantine_config_get_space_available(self):
        """Get space available for quarantine allocation.

        CLI command: quarantineconfig

        *Parameters:*
        None

        *Return:*
        String.

        *Examples:*
        | ${res}= | Quarantine Config Get Space Available |
        | Log | ${res} |
        """
        return self._cli.quarantineconfig().get_space_available()

    def quarantine_config_outbreak_manage_release(self, *args):
        """Manage the Outbreak Filters quarantine.

        CLI command: quarantineconfig > outbreakmanage > release

        *Parameters:*
        - `indicator`: Release all messages with a particular indicator.

        *Return:*
        None

        *Examples:*
        | Quarantine Config Outbreak Manage Release | indicator=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.quarantineconfig().vofmanage().release(**kwargs)

    def quarantine_config_outbreak_manage_delete(self, *args):
        """Manage the Outbreak Filters quarantine.

        CLI command: quarantineconfig > outbreakmanage > delete

        *Parameters:*
        - `indicator`: Delete all messages with a particular indicator.

        *Return:*
        None

        *Examples:*
        | Quarantine Config Outbreak Manage Delete | indicator=STOVE_MANUAL |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.quarantineconfig().vofmanage().delete(**kwargs)
