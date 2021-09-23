#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/onbox_dlp_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re

from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

class OnboxDlpPolicies(GuiCommon, PolicyBase):
    """Keywords for Web Security Manager -> IronPort Data Security
    """

    def get_keyword_names(self):
        return [
                'onbox_dlp_policies_add',
                'onbox_dlp_policies_delete',
                'onbox_dlp_policies_edit',
                'onbox_dlp_policies_edit_url_categories',
                'onbox_dlp_policies_edit_content',
                'onbox_dlp_policies_edit_wbrs',
                'onbox_dlp_policies_get_list',
               ]
    def onbox_dlp_policies_get_list(self):
        """
        Returns: dictionary of policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `proxy_ports`
        - `subnets`
        - `time_range`
        - `url_categories`
        - `protocols`
        - `url_filtering`
        - `web_reputation`
        - `content`

        Examples:

        | ${policies}= | Onbox DLP Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['subnets'] == '10.1.1.1, 20.2.2.2' |
        """

        self._open_page()
        return self._get_policies()

    def _open_page(self):
        self._navigate_to \
         ('Web Security Manager', 'Cisco Data Security')

    def onbox_dlp_policies_add(self,
            name,
            description=None,
            order=None,
            identities='Global Identification Profile',
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            match_agents=True):
        """Add new IDS policy.

        Parameters:

        - `name`:  name for the policy group to add. String.

        - `description`: description for the policy. String.

        - `order`: the processing order. Integer or string.

        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>

        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           - .http
           - .ftpoverhttp
           - .nativeftp
           - .others
           - .https

        - `proxy_ports`: The ports where policy is a member.
           String of comma-separated values

        - `subnets`: the nets where policy is member. String of comma-separated
           values in format of IP, IP range or CIDR.

        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst

        - `user_agents`: the user agents where policy is a member. String of
           comma-separated values

        - `match_agents`: match selected user agents. Default to True.

        Example:
        | Onbox DLP Policies Add | three |
        | | description=Adding policy           |
        | | identities=Global Identification Profile   |
        | | protocols=http, ftpoverhttp         |
        | | proxy_ports=1234, 5321              |
        | | subnets=10.1.1.0/24, 1.2.3.44       |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all                  |
        """
        self._info('Adding "%s" IDS policy' % (name,))

        self._open_page()
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

        self._click_submit_button()

    def onbox_dlp_policies_delete(self, name):
        """Delete IDS policy.

        Parameters:

        - `name`: name of the policy to delete.

        Example:
        | Onbox DLP Policies Delete | three |
        """
        COLUMN = 6
        self._info('Deleting "%s" IDS policy' % (name,))

        self._open_page()

        self._delete_policy(name, COLUMN)

    def onbox_dlp_policies_edit(self,
            name,
            new_name=None,
            description=None,
            order=None,
            identities=None,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            url_categories=None,
            user_agents=None,
            match_agents=True):
        """Edit IDS policy.

        Parameters:

        - `name`: name for the policy group to edit. String.

        - `description`: description for the policy. String.

        - `order`: the processing order. Integer or string.

        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>

        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           - .http
           - .ftpoverhttp
           - .nativeftp
           - .others
           - .https

        - `proxy_ports`: The ports where policy is a member.
           String of comma-separated values

        - `subnets`: the nets where policy is member. String of comma-separated
           values in format of IP, IP range or CIDR.

        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst

        - `user_agents`: the user agents where policy is a member. String of
           comma-separated values

        - `match_agents`: match selected user agents. Defaults to ${True}

        Example:
        | Onbox DLP Policies Edit | three |
        | | description=Adding policy          |
        | | identities=Global Identification Profile  |
        | | protocols=http, ftpoverhttp        |
        | | proxy_ports=80                     |
        | | subnets=99.1.1.0/24                |
        | | url_categories=${webcats.CRIMINAL} |
        | | user_agents=ie-all                 |
        """
        COLUMN = 2

        self._info('Editing "%s" IDS policy' % (name,))
        self._open_page()
        self._click_edit_policy_link(name, COLUMN)
        self._fill_policy_page(new_name, description, order)

        if identities is not None:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

        self._click_submit_button()

    def onbox_dlp_policies_edit_url_categories(self,
            name,
            set_custom_all=None,
            custom_url_categories=None,
            set_predefined_all=None,
            url_categories=None,
            uncategorized_action=None):
        """Edit the IDS policy URL categories settings.

        Parameters:

        - `name`: name of the policy to edit

        - `set_custom_all`: action to set to all custom categories.
           Should be 'allow', 'block', 'monitor', or 'global'

        - `custom_url_categories`: String of comma-separated pairs
           <url_category>:<action>
           - .url_category: custom url category
           - .action can be 'block', 'monitor', 'allow', or 'global'

        - `set_predefined_all`: action to set to all predefined categories.
           Should be 'allow', 'block', 'monitor', or 'global'

        - `url_categories`: String of comma-separated pairs
           <url_category>:<action>
           - .url_category; the categories are described here:
             http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
           - .action can be 'block', 'monitor', or 'global'

        - `uncategorized_action`: the action undertaken for uncategorized URLs:
           action can be 'block', 'monitor', 'allow', or 'global'
        Example:
        | Onbox DLP Policies Edit URL Categories  | three |
        |   | url_categories=${webcats.CHAT}:block, ${webcats.ADULT}:block |
        |   | set_predefined_all=monitor   |
        |   | uncategorized_action=global  |
        | Onbox DLP Policies Edit URL Categories | three |
        |   | set_predefined_all=block   |
        |   | url_categories=${webcats.CHAT}:monitor, ${webcats.CHEAT}:monitor |
        |   | uncategorized_action=allow |
        """

        COLUMN = 3

        self._info('Editing URL categories settings for "%s" IDS policy' \
               % (name))
        self._open_page()
        self._click_edit_policy_link(name, COLUMN)

        if set_custom_all is not None:
            self._set_custom_all(set_custom_all.lower())

        if custom_url_categories is not None:
            self._set_custom_url_categories(self._convert_to_dictionary \
            (custom_url_categories))

        if set_predefined_all is not None:
            self._set_predefined_all(set_predefined_all.lower())

        if url_categories is not None:
            self._set_url_categories(self._convert_to_dictionary(url_categories))

        if uncategorized_action is not None:
            self._select_uncategorized_action(uncategorized_action.lower())

        self._click_submit_button()

    def _set_custom_all(self, set_custom_all):
        BUTTON = lambda index: \
        "xpath=//dt[text()='Custom URL Category Filtering']/.." \
        "//span[contains(text(), 'Select all')]/../../../../th[%s]//*[@onclick]"\
         % (index)

        actions = {
                   'global' : BUTTON(1),
                   'allow'  : BUTTON(2),
                   'monitor': BUTTON(3),
                   'block'  : BUTTON(4)
        }

        self._info("Setting all custom categories to '%s'" % \
            (set_custom_all))

        if not actions.has_key(set_custom_all):
            raise ValueError, "action should be in:" + str(actions.keys())

        self.click_element(actions[set_custom_all], "don't wait")

    def _set_custom_url_categories(self, url_categories):
        """set predefined categories
        """
        CHECKBOX = lambda category, column: \
            "xpath=//dt[text()='Custom URL Category Filtering']/.." \
            "//span[contains(text(), '%s')]/../../../td[%s]" \
            % (category, column)

        actions = {
                   'global' : 2,
                   'allow'  : 3,
                   'monitor': 4,
                   'block'  : 5
        }

        for category in url_categories.keys():
            action = url_categories[category].lower()
            self._info("Setting URL category '%s' to '%s'" % \
                (category, action))
            if actions.keys().count(action) == 0:
                raise ValueError, "Action should be one of " + \
                    str(actions.keys())

            self.click_element(CHECKBOX(category, actions[action]), "don't wait")

    def _set_predefined_all(self, set_predefined_all):
        BUTTON = lambda index: \
        "xpath=//dt[text()='Predefined URL Category Filtering']/.." \
        "//span[contains(text(), 'Select all')]/../../../../th[%s]//*[@onclick]"\
         % (index)

        actions = {
                   'global' : BUTTON(1),
                   'monitor': BUTTON(2),
                   'block'  : BUTTON(3)
        }

        self._info("Setting all predefined categories to '%s'" % \
            (set_predefined_all))

        if not actions.has_key(set_predefined_all):
            raise ValueError, "action should be in:" + str(actions.key())

        self.click_element(actions[set_predefined_all], "don't wait")

    def _set_url_categories(self, url_categories):
        """set predefined categories
        """
        CHECKBOX = lambda category, column: \
            "xpath=//dt[text()='Predefined URL Category Filtering']/.." \
            "//span[contains(text(), '%s')]/../../../td[%s]" \
            % (category, column)

        actions = {
                   'global' : 2,
                   'monitor': 3,
                   'block'  : 4
        }

        for category in url_categories.keys():
            action = url_categories[category].lower()
            self._info("Setting URL category '%s' to '%s'" % \
                (category, action))
            if actions.keys().count(action) == 0:
                raise ValueError, "Action should be one of " + \
                    str(actions.keys())

            self.click_element(CHECKBOX(category, actions[action]), "don't wait")

    def _select_uncategorized_action(self, uncategorized_action):
        LIST = 'id=uncategorized_action'
        actions = {
                   'global':'Use Global Setting (Monitor)',
                   'monitor':'Monitor',
                   'block':'Block'
        }

        self._info("Selecting '%s' action for uncategorized URLs" % \
            (uncategorized_action))

        if not actions.has_key(uncategorized_action):
            raise ValueError, "action should be in:" + str(actions.key())

        self.select_from_list(LIST, actions[uncategorized_action])

    def onbox_dlp_policies_edit_content(self,
            name,
            blocking_settings=None,
            http_file_size=None,
            ftp_file_size=None,
            block_types=None,
            mime_types=None,
            file_names=None,
            regexes=None,
            ):
        """Edit content setting for IDS policy.

        Parameters:

        - `name`: name of the policy to edit.

        - `blocking_settings`: settings to use for this policy. Can be one
           of 'global', 'custom', 'disable'. All other parameters are
           applicable only for blocking_settings=custom

        - `http_file_size`: HTTP/HTTPS Maximum File Size.
           Size must be between 4KB and 1GB. Acceptable values:
           - .'no_limit' - No Maximum
           - .'nnn kb'   - set limit in KB
           - .'nnn mb'   - set limit in MB
           - .'nnn gb'   - set limit in GB

        - `ftp_file_size`: FTP Maximum File Size.
           Size must be between 4KB and 1GB.
            Acceptable values:
           - .'no_limit' - No Maximum
           - .'nnn kb'   - set limit in KB
           - .'nnn mb'   - set limit in MB
           - .'nnn gb'   - set limit in GB

        - `block_types`: Object types to be blocked by this policy.
           String of comma-separated pairs: <object_type>:<block>
           - . object_type of file; available types are described here:
             http://eng.ironport.com/docs/qa/sarf/keyword/common/file_types.rst
           - . block-settings for the object_type.
            Acceptable values:
            - . . 'off' - do not block
            - . . 'all' - block all files of this type
            - . . 'nnn kb' - block files of this type if over nnn KB.
               Size must be between 4KB and 256MB
            - . . 'nnn mb' - block files of this type if over nnn MB.
               Size must be between 1MB and 256MB

        - `mime_types`: MIME types to be blocked by this policy.
           String of comma-separated values. Mime types by category
           are presented here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/content_filters.html
           Example: mime_types=audio/x-mpeg3, audio/*

        - `file_names`: file names to be blocked by this policy.
           String of comma-separated values.
           Example: file_names=document.doc,spreadsheet.xls.
           File names are not case sensitive

        - `regexes`: Match specific file names by regular expressions.
           The regular expressions may not begin or end with '.*'.
           String of comma-separated values.

        Example:
        | Onbox DLP Policies Edit Content    | three |
        | | blocking_settings=custom           |
        | | http_file_size=10 mb               |
        | | ftp_file_size=no_limit             |
        | | block_types=${filetypes.ARC_ARC}:all, ${filetypes.DOC_PDF}:10 mb |
        | | mime_types=audio/x-mpeg3, video/avi |
        | | file_names=document.doc,spreadsheet.xls |
        | | regexes=[Pp]orno, [Ss$]ex |

        See more examples in unit test
        """
        COLUMN = 5
        self._info('Editing content settings for "%s" IDS policy' % (name,))

        self._open_page()
        self._click_edit_policy_link(name, COLUMN)
        self._select_objects_blocking_settings(blocking_settings)

        self._extend_closed_arrows()
        if http_file_size is not None:
            self._set_max_file_size_blocking(object_type='http',
                    file_size=http_file_size)
        if ftp_file_size is not None:
            self._set_max_file_size_blocking(object_type='ftp',
                    file_size=ftp_file_size)
        if block_types is not None:
            self._set_blocking_of_predefined_objects \
              (self._convert_to_dictionary(block_types))
        if mime_types is not None:
            self._set_blocking_of_mime_types \
                (self._convert_to_tuple(mime_types))
        if file_names is not None:
            self._set_blocking_of_file_names \
                (self._convert_to_tuple(file_names))
        if regexes is not None:
            self._set_blocking_of_regexes \
                (self._convert_to_tuple(regexes))

        self._click_submit_button()

    def onbox_dlp_policies_edit_wbrs(self,
            name,
            settings_type=None,
            score=None,
            ):
        """Edit the WBRS for the IDS policy.

        Parameters:

        - `name`: name of the policy to edit.

        - `settings_type`: 'global' 'custom' or 'disable'

        - `score`: The threshold in between block and monitor actions.
          Can be set only with settings_type=custom.
          Not implemented yet

        Example:
        | Onbox DLP Policies Edit WBRS    | three |
        | | settings_type=custom  |

        """
        COLUMN = 4
        self._info('Editing WBRS settings for "%s" IDS policy' % (name,))

        self._open_page()

        self._click_edit_policy_link(name, COLUMN)

        if settings_type is not None:
            self._select_wbrs_settings(settings_type)

        if settings_type == 'custom':
            if score is not None:
                self._set_wbrs_score(score)

        self._click_submit_button()

    def _select_objects_blocking_settings(self, settings):
        object_settings = {
            'global': 'default',
            'custom': 'custom',
            'disable': 'disable',
        }
        SETTINGS_TYPE_LOC = 'id=settings_type'

        self._info("Selecting '%s' blocking settings" % (settings))

        if settings not in object_settings:
            raise ValueError, 'Invalid "%s" object blocking settings' \
                % (settings)

        self.select_from_list(SETTINGS_TYPE_LOC, object_settings[settings])

    def _set_max_file_size_blocking(self, object_type, file_size):
        """Setting file size for HTTP/HTTPS and FTP
        Parameters:

        - `object_type` -'http' or 'ftp'

        - `file_size`: Maximum File Size. Acceptable values:
           - .'no_limit' - No Maximum
           - .'nnn kb'   - set limit in KB
           - .'nnn mb'   - set limit in MB
           - .'nnn gb'   - set limit in GB
        """

        RADIO_BOX = lambda object_type, use: 'enforce_file_size_%s_%s' \
            % (object_type, use)
        SIZE = lambda object_type: 'max_file_size_%s' % (object_type)
        UNIT = lambda object_type: 'max_file_size_%s_units' % (object_type)

        self._info("Setting blocking '%s' to:'%s'" % (object_type, file_size))

        size_pattern = '(?P<size>[0-9]+) *(?P<unit>[KMG]).*'

        if file_size.lower() == 'no_limit':
            self._click_radio_button(RADIO_BOX(object_type, 'no'))

        elif re.match(size_pattern, file_size.upper()) is not None:
            # process size
            m = re.match(size_pattern, file_size.upper())
            self._click_radio_button(RADIO_BOX(object_type, 'yes'))
            self.input_text(SIZE(object_type), m.group('size'))
            self.select_from_list(UNIT(object_type), m.group('unit') + 'B')
        else:
            raise ValueError, \
                "Value '%s' should be 'no_limit' or <nnn> KB, MB, or GB" % \
                    (file_size)

    def _set_blocking_of_predefined_objects(self, object_types):
        """Expand all objects' categories and call settings by object_type
        Note. Expanding does not work now, that's supposedly a bug in Selenium
        Workaround is used: setting blocking by types twice - it works.
        The following code is commented-out to be applied when the bug is fixed.
        """
#        ARROW = "xpath=//div[starts-with(@id , 'arrow_open_') and not(@style='')]/../.."

#        count = int(self.get_matching_xpath_count(ARROW))
#
#        for i in range(count):
#            if self._is_visible(ARROW):
#                self.click_element(ARROW, "don't wait")
#
#        count = int(self.get_matching_xpath_count(ARROW))
#        if count > 0:
#            raise guiexceptions.GuiControlNotFoundError( \
#                "Failed to expand " + str(count) + " ARROWs")

        for object_type in object_types.keys():
            self._set_blocking_type(object_type, object_types[object_type])

    def _set_blocking_type(self, object_type, block):
        """Set blocking of the specified type of file
        block must be between 4KB and 256MB.
        Acceptable values:
            # 'off' - do not block
            # 'all' - block all files of this type
            # 'nnn kb' - block files of this type if over nnn KB.
            # 'nnn mb' - block files of this type if over nnn MB.
        """
        CHECK_BOX = lambda object_type:  "xpath=//tr[td/label = '%s']/td[1]/input" \
          % (object_type)
        TYPE_BOX = lambda object_type:  "xpath=//tr[td/label = '%s']/td[3]/select[1]"\
          % (object_type)
        SIZE = lambda object_type:  "xpath=//tr[td/label = '%s']/td[3]/input"\
          % (object_type)
        UNIT = lambda object_type:  "xpath=//tr[td/label = '%s']/td[3]/select[2]"\
          % (object_type)

        BLOCK_ALL = "Block all files of this type"
        BLOCK_OVERSIZE = "Block file of this type if over size:"

        self._info("Setting blocking '%s' to:'%s'" % (object_type, block))
        size_pattern = '(?P<size>[0-9]+) *(?P<unit>[KM]).*'

        if block.lower() == 'off':
            if self._is_checked(CHECK_BOX(object_type)):
                self.click_element(CHECK_BOX(object_type), "don't wait")

        elif block.lower() == 'all':
            if not self._is_checked(CHECK_BOX(object_type)):
                self.click_element(CHECK_BOX(object_type), "don't wait")
            self.select_from_list(TYPE_BOX(object_type), BLOCK_ALL)

        elif re.match(size_pattern, block.upper()) is not None:
            # process size
            self.select_checkbox(CHECK_BOX(object_type))
            self.select_from_list(TYPE_BOX(object_type), BLOCK_OVERSIZE)

            m = re.match(size_pattern, block.upper())
            self.input_text(SIZE(object_type), m.group('size'))
            self.select_from_list(UNIT(object_type), m.group('unit') + 'B')
        else:
            raise ValueError, \
            "Block '%s' should be 'off', 'all' or <nnn> KB or MB" % \
                (block)

    def _set_blocking_of_mime_types(self, mime_types):
        INPUT = 'id=custom_object_types'
        self._info('Setting blocking for "%s" mime types' % str(mime_types))
        self.input_text(INPUT, '\r\n'.join(mime_types))

    def _set_blocking_of_file_names(self, file_names):
        INPUT = 'id=custom_file_names'
        self._info('Setting blocking for "%s" file names' % str(file_names))
        self.input_text(INPUT, '\r\n'.join(file_names))

    def _set_blocking_of_regexes(self, regexes):
        ARROW = 'id=regex_arrow_closed'
        INPUT = 'custom_filenames_regex'
        self._info('Setting blocking for "%s" regex patterns' % str(regexes))
        if not self._is_visible(INPUT):
            self.click_element(ARROW, "don't wait")

        self.input_text(INPUT, '\r\n'.join(regexes))

    def _select_wbrs_settings(self, settings):
        wbrs_settings = {
            'global': 'use_global',
            'custom': 'custom',
            'disable':'disabled'}
        SETTINGS_TYPE_LOC = 'id=settings_type'

        self._info('Selecting "%s" wbrs settings' % (settings,))

        if settings not in wbrs_settings:
            raise ValueError, "Invalid wbrs settings '%s' should be in %s" \
                % (settings, str(wbrs_settings.keys()))

        self.select_from_list(SETTINGS_TYPE_LOC, wbrs_settings[settings])

    def _set_wbrs_score(self, score):
#        BLOCK_LOC = 'id=custom_block_boundary'
        self._info('Setting up %s WBRS score' % score)
        raise NotImplementedError

    def _extend_closed_arrows(self):
        """
        Extend all closed arrows
        """
        LIST = [
            'arrow_closed_Archives_edit',
            'arrow_closed_Inspectable Archives_edit',
            'arrow_closed_Document Types_edit',
            'arrow_closed_Executable Code_edit',
            'arrow_closed_Installers_edit',
            'arrow_closed_Media_edit',
            'arrow_closed_P2P Metafiles_edit',
            'arrow_closed_Web Page Content_edit',
            'arrow_closed_Miscellaneous_edit',
        ]
        for item in LIST:
            ARROW = "//div [@id='%s']/img" % item + \
                "[contains(@src,'arrow_showhide_hiding.gif')]"
            if self._is_visible(ARROW):
                self.click_element(ARROW, "don't wait")
