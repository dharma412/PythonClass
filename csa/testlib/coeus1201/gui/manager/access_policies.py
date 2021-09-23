#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/access_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from constants import (filetypes, mwcats, applications)
from policybase import PolicyBase
import time

filetypes_locators_map = {
    # Archives
    filetypes.ARC_7Z: 'Inspectable Archives_application/x-7z-compressed_Allow', #7Zip
    filetypes.ARC_ARC: 'Archives_application/x-arc', # ARC
    filetypes.ARC_ARJ: 'Archives_application/x-arj', # ARJ
    filetypes.ARC_BINHEX: 'Archives_application/mac-binhex40', #  BinHex
    filetypes.ARC_BZIP2: 'Inspectable Archives_application/x-bzip2_Allow', #  BZIP2
    filetypes.ARC_Z: 'Inspectable Archives_application/x-compress_Allow', # Compress Archive (Z)
    filetypes.ARC_CPIO: 'Inspectable Archives_application/x-cpio_Allow', #  CPIO
    filetypes.ARC_GZIP: 'Inspectable Archives_application/x-gzip_Allow', #  GZIP
    filetypes.ARC_LHA: 'Inspectable Archives_application/x-lha_Allow', #  LHA
    filetypes.ARC_LHARC: 'Archives_application/x-lharc', #  LHARC
    filetypes.ARC_MSCAB: 'Inspectable Archives_application/vnd.ms-cab-compressed_Allow', #  Microsoft CAB
    filetypes.ARC_RAR: 'Inspectable Archives_application/x-rar_Allow', #  RAR
    filetypes.ARC_STUFFIT: 'Archives_application/x-stuffit', #  StuffIt
    filetypes.ARC_TAR: 'Inspectable Archives_application/x-tar_Allow', #  TAR
    filetypes.ARC_ZIP: 'Inspectable Archives_application/zip_Allow', #  ZIP Archive
    # Document Types
    filetypes.DOC_FM: 'Document Types_application/x-mif', #  FrameMaker Document (FM)
    filetypes.DOC_MSOFFICE: 'Document Types_Microsoft Office', #  Microsoft Office
    filetypes.DOC_OASIS: 'Document Types_OASIS Open Document Format', #  OASIS Open Document Format
    filetypes.DOC_OPENOFFICE: 'Document Types_OpenOffice Document', #  OpenOffice Document
    filetypes.DOC_PDF: 'Document Types_application/pdf', #  Portable Document Format (PDF)
    filetypes.DOC_PS: 'Document Types_application/postscript', #  PostScript Document (PS)
    filetypes.DOC_RTF: 'Document Types_text/rtf', #  Rich Text Format (RTF)
    filetypes.DOC_XML: 'Document Types_XML Document', #  XML Document (XML)
    # Executable Code
    filetypes.EXE_JAVA: 'Executable Code_application/x-java-applet', #  Java Applet
    filetypes.EXE_UNIXEXEC: 'Executable Code_UNIX Executable', #  UNIX Executable
    filetypes.EXE_WINEXEC: 'Executable Code_Windows Executable', #  Windows Executable
    # Installers
    filetypes.INST_UNIX: 'Installers_UNIX/LINUX Packages', # UNIX/LINUX Packages
    # Media
    filetypes.MEDIA_AUDIO: 'Media_Audio', #  Audio
    filetypes.MEDIA_VIDEO: 'Media_Video', #  Video
    filetypes.MEDIA_IMAGE: 'Media_Photographic Images', #  Photographic Image Processing Formats (TIFF/PSD)
    # P2P Metalinks
    filetypes.P2P_BITTORRENT: 'P2P Metafiles_application/x-bittorrent', # BitTorrent Links (.torrent)
    # Web Page Content
    filetypes.WEB_FLASH: 'Web Page Content_application/x-shockwave-flash', #  Flash
    filetypes.WEB_IMAGE80: 'Web Page Content_Images', #  Images
    # Miscellaneous
    filetypes.MISC_VCAL: 'Miscellaneous_text/calendar', #  Calendar Data
}

amp_known_malicious_locator = '37'

mwcats_locators_map = {
    mwcats.ADWARE: '13',
    mwcats.ADDONS: '12',
    mwcats.COMM_SYSMON: '18',
    mwcats.DIALER: '19',
    mwcats.SPYWARE: '10',
    mwcats.HIJACKER: '20',
    mwcats.OTHER: '33',
    mwcats.PHISHING_URL: '21',
    mwcats.PUA: '34',
    mwcats.SYSMON: '14',
    mwcats.DOWNLOADER: '22',
    mwcats.TROJAN: '23',
    mwcats.PHISHER: '24',
    mwcats.VIRUS: '27',
    mwcats.WORM: '25',
    mwcats.ENCRYPTED: '26',
    mwcats.UNSCANNABLE: '4',
    mwcats.SUA: 'sua',
    mwcats.ALLMALWARE: 'all_malware',
    mwcats.ALLOTHERMALWARE: 'other_mal'
}

class AccessPolicies(GuiCommon, PolicyBase):
    """Access Policies page interaction class.

    This class designed to interact with GUI elements of Web Security Manager ->
    Access Policies page. Use keywords, listed below, to configure Access
    Policies.

    Additional information:
    1. <a href="http://eng.ironport.com/docs/qa/sarf/keyword/coeus75/gui/policy_base.html">Identities specification</a>.
    2. <a href="http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst">URL Categories specification</a>.
    3. <a href="http://eng.ironport.com/docs/qa/sarf/keyword/common/content_filters.html">MIME types specification</a>.
    4. <a href="http://eng.ironport.com/docs/qa/sarf/keyword/common/applications.rst">Applications constants specification</a>.
    5. <a href="http://eng.ironport.com/docs/qa/sarf/keyword/common/mwcats.rst">Malware constants specification</a>.
    """

    ap_policy_name_column = 2
    ap_prot_usr_agnt_column = 3
    ap_url_filtering_column = 4
    ap_applications_column = 5
    ap_objects_column = 6
    ap_wbrs_column = 7
    ap_delete_column = 8

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
            'access_policies_add',
            'access_policies_edit',
            'access_policies_delete',
            'access_policies_edit_protocols_and_user_agents',
            'access_policies_edit_objects',
            'access_policies_edit_url_categories',
            'access_policies_edit_referrer_content',
            'access_policies_disable_referrer_content',
            'access_policies_delete_referrer_content',
            'access_policies_edit_applications',
            'access_policies_edit_anti_malware_and_reputation',
            'access_policies_edit_content_filtering_settings',
            'access_policies_disable_policy',
            'access_policies_enable_policy',
            'access_policies_is_enabled_policy',
            'access_policies_get_list',
        ]

    def access_policies_get_list(self):
        """
        Returns: dictionary of access policies. Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `protocols_and_user_agents`
        - `url_filtering`
        - `applications`
        - `objects`
        - `anti_malware_and_reputation`

        Examples:

        | ${policies}= | Access Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['applications'] == '(global policy)' |
        """

        self._open_acc_pol_page()
        return self._get_policies()


    def access_policies_add(
        self,
        name,
        description=None,
        order=None,
        identity='Global Identification Profile',
        protocols=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_range=None,
        url_categories=None,
        user_agents=None,
        common_user_agents=None,
        match_agents=None,
        expires=None,
        datetimemin=None,
        dut=None
    ):
        """Adds new access policy.

        Parameters:
        - `name`: name of access policy.
        - `description`: description for access policy.
        - `order`: order of access policy.
        - `identity`:
    Identities are specified as a string of comma-separated values where each
    identity is presented in the following format:

    <name>[:<auth_method>[:<list of users>[:<list of groups>]]]

    - name: name is the only required field
    - auth_method: default value is None. Other accepted values:
        * authenticated
        * selected
        * guests
        * all
     - list of users: users separated by #
     - list of groups: groups separated by #
     - list of SGT groups: groups separated by #
    - expires: True. True If the policy expiration needs to be set and user is entering the expiration date and time else do not set anything.
    - datetimemin: Enter the expiration date time in hr and minute. Format <dd-hr-min>.
        * dd : Enter the date. Choose date 1 - 31
        * hr : Enter the hour. Choose hour 00 - 23
        * min: Enter minute. The options available are 00 and 30

    Note. If identity with name "All Identification Profiles" is in the list of
    identities, it should be the only 1 in the list

    Note. List of users, list of groups, and list of STG groups are used when
    auth_method is "selected"

    Examples:
    | identities=i2 |
    | identities=Global Identification Profile:authenticated |
    | identities=i2:selected:vasia#petya:group1#group2:SGTGroup8#SGTGroup6 |
    | identities=All Identification Profiles:all |
    | identities=i2:selected::group3#group4, Global Identification Profile:guests |
        - `protocols`: string with comma separated values. Available values:
        'http', 'https', 'ftpoverhttp', 'nativeftp'.
        - `proxy_ports`: string with comma separated values.
        - `subnets`: string with comma separated values.
        - `time_range`: name of specified time_range.
        - `match_range`: ${True} if "Match during the selected time range"
        ${False} if "Match except during the selected time range".
        - `url_categories`: string with comma separated values. Document that
        describes URL Categories can be found here.
        - `user_agents`: string with comma separated values.
        - `match_agents`: ${True} if "Match the selected user agent definitions"
        ${False} if "Match all except the selected user agent definitions"

        Examples:
        | Access Policies Add | myDefaultAccPol |
        | ... | description=This policy uses Global Identification Profile |

        | Access Policies Add | myOtherAccPol |
        | ... | description=This policy uses custom identity |
        | ... | identity=myID |

        | Access Policies Add | myNewPolicy |
        | ... | description=Test access policy |
        | ... | identity=Global Identification Profile |
        | ... | protocols=http |
        | ... | proxy_ports=8080, 3128 |
        | ... | subnets=192.168.1.1/24 |
        | ... | time_range=test |
        | ... | match_range=${True} |
        | ... | url_categories=test |
        | ... | user_agents=ie7, ie8 |
        | ... | common_user_agents=Mozilla/4.0 \(compatible; MSIE 5.5;\) |
        | ... | match_agents=${True} |
        """

        self._open_acc_pol_page()
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order, expires, datetimemin, dut)

        self._edit_identity_membership(identity)

        self._edit_advanced_settings(protocols, proxy_ports, subnets,
                                     time_range, match_range, url_categories,
                                     user_agents, common_user_agents,
                                     match_agents)

        self._click_submit_button(wait=False)

    def access_policies_edit(
        self,
        name,
        description=None,
        order=None,
        identity='Global Identification Profile',
        protocols=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_range=None,
        url_categories=None,
        user_agents=None,
        common_user_agents=None,
        match_agents=True,
        new_name=None,
    ):
        """Edits specified access policy.

        Parameters:
        - `name`: name of access policy to be edited.
        - `description`: description for access policy.
        - `order`: order of access policy.
        - `identity`:
    Identities are specified as a string of comma-separated values where each
    identity is presented in the following format:

    <name>[:<auth_method>[:<list of users>[:<list of groups>]]]

    - name: name is the only required field
    - auth_method: default value is None. Other accepted values:
        * authenticated
        * selected
        * guests
        * all
     - list of users: users separated by #
     - list of groups: groups separated by #
     - list of SGT groups: groups separated by #

    Note. If identity with name "All Identification Profiles" is in the list of
    identities, it should be the only 1 in the list

    Note. List of users, list of groups, and list of STG groups are used when
    auth_method is "selected"

    Examples:
    | identities=i2 |
    | identities=Global Identification Profile:authenticated |
    | identities=i2:selected:vasia#petya:group1#group2:SGTGroup8#SGTGroup6 |
    | identities=All Identification Profiles:all |
    | identities=i2:selected::group3#group4, Global Identification Profile:guests |
        - `protocols`: string with comma separated values. Available values:
        'http', 'https', 'ftpoverhttp', 'nativeftp'.
        - `proxy_ports`: string with comma separated values that represent port
        numbers.
        - `subnets`: string with comma separated values.
        - `time_range`: name of specified time_range. String.
        - `match_range`: ${True} if "Match during the selected time range"
        ${False} if "Match except during the selected time range".
        - `url_categories`: string with comma separated values. Document that
        describes URL Categories can be found here.
        - `user_agents`: string with comma separated values.
        - `match_agents`: ${True} if "Match the selected user agent definitions"
        ${False} if "Match all except the selected user agent definitions"
        - `new_name`: new name of the policy, if it should be changed

        Example:
        | Access Policies Edit | myNewTestPolicy |
        | ... | description=Edited by unittest |
        | ... | order=2 |
        | ... | identity=Global Identification Profile |
        | ... | protocols=http, ftp |
        | ... | proxy_ports=80, 443 |
        | ... | subnets=10.0.0.1/24 |
        | ... | time_range=test1 |
        | ... | match_range=${False} |
        | ... | url_categories=test |
        | ... | user_agents=ie-all |
        | ... | common_user_agents=Mozilla/.* Gecko/.* Firefox/ |
        | ... | match_agents=${False} |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_policy_name_column)
        self._fill_policy_page(new_name, description, order)

        self._edit_identity_membership(identity)
        self._edit_advanced_settings(protocols, proxy_ports, subnets,
                                     time_range, match_range, url_categories,
                                     user_agents, common_user_agents,
                                     match_agents)

        self._click_submit_button(wait=False)

    def access_policies_delete(self, name):
        """Deletes specified access policy.

        `name`: name of access policy to be deleted.

        Example:
        | Delete Access Policy | myAccPol |
        """

        self._open_acc_pol_page()
        self._delete_policy(name, self.ap_delete_column)

    def access_policies_edit_protocols_and_user_agents(self,
                                                       name,
                                                       setting_type='custom',
                                                       block_protocols=None,
                                                       connect_ports=None,
                                                       block_user_agents=None):
        """Sets protocol blocking.

        Parameters:
        - `name`: name of access policy to edit.
        - `setting_type`: setting type to use.  Either 'custom', 'global'
          or 'disable'.
        - `block_protocols`: protocols to be blocked. Either 'block all',
          'allow all' or a list of one or more protocols to be blocked.
          Avaliable protocols: 'ftpoverhttp', 'nativeftp', 'http', 'https'.
        - `connect_ports`: Tunneled ports. String with comma separated ports or
        port-ranges.
        - `block_user_agents`: list with user agents patterns.

        Exceptions:
        - GuiValueError:Invalid setting type - xxx
        - ConfigError:Setting type 'global' can not be applied to 'Global Policy'.

        Example:

        | @{user_agents} | Mozilla/.* Gecko/.* Firefox/ |
        | ... | Mozilla/.*compatible; MSIE |

        | Edit Protocols And User Agents | myAccPol |
        | ... | block_protocols=allow all |
        | ... | connect_ports=8080, 21, 443, 563, 8443, 20, 1-15 |
        | ... | block_user_agents=${user_agents} |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_prot_usr_agnt_column)

        if(
            setting_type.strip().lower() == 'global'
            and name.strip().lower() == 'global policy'
        ):
            raise guiexceptions.ConfigError(
                "Setting type 'global' can not be applied to 'Global Policy'."
            )

        self._select_protocols_setting_type(setting_type)

        if setting_type.strip().lower() == 'custom':
            if block_protocols is not None:
                self._edit_protocols_blocking(block_protocols)
            if block_user_agents is not None:
                self._edit_user_agents_blocking(block_user_agents)
            if connect_ports is not None:
                self._edit_connect_ports(connect_ports)

        self._click_submit_button()

    def access_policies_edit_objects(
        self,
        name,
        setting_type='global',
        http_size=None,
        ftp_size=None,
        file_types=None,
        inspect_archive=None,
        custom_mime_types=None
    ):
        """Edit specified Access Policy object settings.

        Parameters:
        - `name`: name of the access policy to edit.
        - `setting_type`: setting type to use.  Either 'custom', 'global'
        or 'disable'.
        - `http_size`: use if setting type is 'custom'. Positive integer value
        (from 1 to 1024) sets 'HTTP/HTTPS Max Download Size'. Value
        'No Maximum' sets option 'Max Download Size' to 'No Maximum' value.
        - `ftp_size`: use if setting type is 'custom'. Positive integer value
        (from 1 to 1024) sets 'FTP Max Download Size'. Value 'No Maximum'
        sets option 'Max Download Size' to 'No Maximum' value.
        - `file_types`: List with file types to be blocked. MIME types Document.
        - `custom_mime_types`: list with custom MIME types to be blocked.
        - `inspect_archive`: If not specified, the inspectable filetype is 'blocked'.
        If any string is specified, inspectable file types are set to 'inspect'

        Exceptions:
        - GuiValueError:Invalid setting type - xxx
        - ConfigError:"xxx" object type is not predefined
        - ConfigError:Setting type 'global' can not be applied to 'Global Policy'.

        Example:
        | @{filetypes_list}= | Create List |
        | ... | ${filetypes.ARC_ARC} |
        | ... | ${filetypes.ARC_GZIP} |
        | ... | ${filetypes.MEDIA_AUDIO} |
        | ... | ${filetypes.P2P_BITTORRENT} |

        | @{mime_types_list}= | Create List |
        | ... | audio/x-mpeg3 |
        | ... | audio/* |

        | Access Policies Edit Objects | myTestPolicy |
        | ... | setting_type=custom |
        | ... | http_size=1024 |
        | ... | ftp_size=1024 |
        | ... | file_types=${filetypes_list} |
        | ... | custom_mime_types=${mime_types_list} |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_objects_column)
        if setting_type.lower() == 'global' and name.lower() == 'global policy':
            raise guiexceptions.ConfigError(
                "Setting type 'global' can not be applied to 'Global Policy'."
            )

        self._select_setting_type(setting_type)
        if setting_type.strip().lower() == 'custom':

            # setting block object size options
            if http_size is not None:
                self._set_max_file_size_blocking('http', http_size)
            if ftp_size is not None:
                self._set_max_file_size_blocking('ftp', ftp_size)

            # setting block custom MIME type options
            if custom_mime_types is not None:
                if (isinstance(custom_mime_types, str) or
                    isinstance(custom_mime_types, unicode)):
                    custom_mime_types = (custom_mime_types,)
                mime_types_text = '\r\n'.join(custom_mime_types)
                self.input_text("xpath=//textarea[@id='custom_object_types']",
                                mime_types_text)

            # setting block object type options
            if file_types is not None:
                self._set_blocking_of_predefined_objects(file_types, inspect_archive)

        self._click_submit_button()

    def select_content_filtering_custom_settings_type(self, policytype):
        type_dict = {
            'global':  'use_global',
            'custom':  'custom'
        }

        if policytype.strip().lower() not in type_dict.keys():
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )

        self.select_from_list(
            'content_filtering_custom_settings',
            type_dict[policytype]
        )

    def _set_safe_search(self, setting, unsupported):

        ss_checkbox = "xpath=//input[@id='enable_safe_search']"
        ss_enabled = self._is_checked(ss_checkbox)
        if setting.strip().lower() == 'enable' and not ss_enabled:
            self.click_element(ss_checkbox, "don't wait")
        if setting.strip().lower() == 'disable' and ss_enabled:
            self.click_element(ss_checkbox, "don't wait")
        if ss_enabled and unsupported is not None:
            if unsupported.strip().lower() == 'block':
                self.select_checkbox('id=block_not_supported_safe_search')
            else:
                self.unselect_checkbox('id=block_not_supported_safe_search')

    def _set_site_content_rating(self, setting, action):

        cr_checkbox = "xpath=//input[@id='enable_content_rating']"
        cr_enabled = self._is_checked(cr_checkbox)
        if setting.strip().lower() == 'enable' and not cr_enabled:
            self.click_element(cr_checkbox, "don't wait")
        if setting.strip().lower() == 'disable' and cr_enabled:
            self.click_element(cr_checkbox, "don't wait")

        if cr_enabled and action is not None:
            if action.strip().lower() == 'block':
                self._click_radio_button(
                    'id=block_not_supported_content_rating')
            elif action.strip().lower() == 'warn':
                self._click_radio_button('id=warn_not_supported_content_rating')
            else:
                raise guiexceptions.GuiConfigError(
                    'Invalid Action Type. Action: "%s"' % action
                )

    def access_policies_edit_content_filtering_settings(
        self,
        name,
        setting_type='custom',
        safe_search_option=None,
        unsupported_option=None,
        content_rating=None,
        content_action=None
    ):

        """Edit specified Access Policies Content Filtering Settings.

        Parameters:
        - `name`: name of the access policy to edit.
        - `setting_type`: setting type to use.  Either 'custom' or 'global'.
        - `safe_search_option`: either 'enable' or 'disable'.
        - `unsupported_option`: either 'block' or 'allow'.
        - `content_rating`: either 'enable' or 'disable'.
        - `content_action`: either 'block' or 'warn'.

        Exceptions:
        - GuiValueError:Invalid setting type xxx

        Examples:
        | ${pol} | Set Variable | test |

        | Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=global |

        | Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=custom |
        | ... | safe_search_option=enable |
        | ... | unsupported_option=allow |
        | ... | content_rating=enable |
        | ... | content_action=block |

        | Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=custom |
        | ... | safe_search_option=disable |
        | ... | content_rating=disable |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_url_filtering_column)
        self._check_feature_status('acceptable_use_control')
        if name.strip().lower() != 'global policy':
            self.select_content_filtering_custom_settings_type(setting_type)
        if setting_type.strip().lower() == 'custom':
            if safe_search_option is not None or unsupported_option is not None:
                self._set_safe_search(safe_search_option, unsupported_option)
            if content_rating is not None or content_action is not None:
                self._set_site_content_rating(content_rating, content_action)
        self._click_submit_button()

    def access_policies_edit_anti_malware_and_reputation(
        self,
        name,
        setting_type='custom',
        wbrs_setting=None,
        amp_file_rep_setting=None,
        amp_known_malicious_action=None,
        sua_setting=None,
        sua_action=None,
        webroot=None,
        av=None,
        ams_setting=None,
        amw_categories=None,
        custom_block_boundary=None,
        custom_allow_boundary=None
    ):
        """Edit specified Access Policies: Anti-Malware and Reputation
        Settings.

        This keyword allows to set:
        - `WBRS settings`,
        - `Advanced Malware Protection settings`,
        - `Suspect User Agent Scanning settings`,
        - `Anti-Malware Scanning (Webroot, McAfee, and Sophos)`

        Parameters:
        - `name`: name of the access policy to edit.
        - `setting_type`: setting type to use.  Either 'custom' or 'global'.
        - `wbrs_setting`: either 'enable' or 'disable'. Web reputation feature
        setting.
        - `amp_file_rep_setting`: either 'enable' or 'disable'. Advanced
        Malware Protection File Reputation Filtering setting.
        - 'amp_known_malicious_action`: either 'monitor' or 'block'. It requires
        that Advanced Malware Protection Settings -> Enable File Reputation Filtering
        to be checked first.
        - `sua_setting`: either 'enable' or 'disable'. Suspected User Agent
        settings.
        - `sua_action`: either 'block' or 'monitor'. Action for suspected user
        agents.
        - `webroot`: either 'enable' or 'disable'. Webroot setting. Used only if
        adaptive scanning is disabled.
        - `av`: either 'mcafee', 'sophos' or 'disable'. Antivirus setting. Used
        only if adaptive scanning is disabled.
        - `ams_setting`: either 'enable' or 'disable'. Adaptive scanning
        setting. If disabled, use 'av' and 'webroot' instead.
        - `amw_categories`: list with items. Each item represents two values,
        separated by colon. First value is mwcat object, second is action (
        either monitor or block). Document that describes mwcats constants.
        - `custom_block_boundary`: All URLs which have score lower than this
        value will be blocked w/o scanning. This option makes sense only if
        adaptive scanning feature is disabled.
        - `custom_allow_boundary`: All URLs which have score higher than
        this value will be allowed w/o scanning.  This option makes sense only
        if adaptive scanning feature is disabled.

        Exceptions:
        - GuiConfigError:Invalid setting type - "xxx"
        - ConfigError:Setting 'xxx' should be either 'enable' or 'disable
        - ConfigError:Unknown antivirus - "xxx". Should be "mcafee"or "sophos"
        - GuiValueError:Invalid setting type - xxx
        - ConfigError:Unknown action - "xxx". Should be "block"or "monitor"

        Examples:
        | ${pol} | Set Variable | test |

        | @{ams_cats}= | Set Variable |
        | ... | ${mwcats.ADWARE}:monitor |
        | ... | ${mwcats.SYSMON}:block |

        | Access Policies Edit Anti Malware And Reputation| ${pol} |
        | ... | setting_type=global |

        | Access Policies Edit Anti Malware And Reputation | ${pol} |
        | ... | wbrs_setting=enable |
        | ... | sua_setting=enable |
        | ... | sua_action=block |
        | ... | ams_setting=enable |
        | ... | amw_categories=${ams_cats} |

        | Access Policies Edit Anti Malware And Reputation | ${pol} |
        | ... | webroot=enable |
        | ... | av=sophos |

        | Access Policies Edit Anti Malware And Reputation | ${pol} |
        | ... | wbrs_setting=enable |
        | ... | custom_block_boundary=-8 |
        | ... | custom_allow_boundary=7.5 |

        | Access Policies Edit Anti Malware And Reputation | ${pol} |
        | ... | amp_file_rep_setting=enable |
        | ... | amp_known_malicious_action=block |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_wbrs_column)

        if name.strip().lower() != 'global policy':
            self._select_ams_setting_type(setting_type)

        if setting_type.strip().lower() == 'custom':
            if (
                ams_setting is not None
                or amw_categories is not None
                or webroot is not None
                or av is not None
            ):
                self._set_ams_settings(ams_setting, webroot, av, amw_categories)

            if amp_file_rep_setting is not None:
                self._set_amp_file_rep_settings(
                    amp_file_rep_setting,
                    amp_known_malicious_action
                )

            if sua_setting is not None or sua_action is not None:
                self._set_sua_settings(sua_setting, sua_action)

            if wbrs_setting is not None:
                self._set_wbrs_settings(
                    wbrs_setting,
                    custom_allow_boundary,
                    custom_block_boundary
                )

        self._click_submit_button()

    def _set_ams_settings(self, ams_setting, webroot, av, amw_categories):

        amw_categories = self._convert_to_tuple(amw_categories)
        ams_checkbox = "xpath=//input[@id='enable_adaptivescanning']"
        webroot_checkbox = "xpath=//input[@id='enable_webroot']"
        av_checkbox = "xpath=//input[@id='select_engine']"

        if ams_setting is not None:
            self._enable_or_disable_checkbox(ams_checkbox, ams_setting)
        if webroot is not None:
            self._enable_or_disable_checkbox(webroot_checkbox, webroot)
        if av is not None:
            if av == 'disable':
                av_setting = 'disable'
            else:
                av_setting = 'enable'
                self._select_av(av)
            self._enable_or_disable_checkbox(av_checkbox, av_setting)

        if amw_categories is not None:
                self._select_categories(amw_categories)

    def _enable_or_disable_checkbox(self, locator, setting):
        if setting.lower().strip() in ['enable', 'disable']:
            self._validate_presence(locator)
            element_checked = self._is_checked(locator)
            if setting.lower().strip() == 'enable' and not element_checked:
                self.click_element(locator, "don't wait")
            if setting.lower().strip() == 'disable' and element_checked:
                self.click_element(locator, "don't wait")
        else:
            raise guiexceptions.ConfigError(
                'Setting should be either [enable | disable] Setting: %s'
                % setting
            )

    def _select_av(self, av):
        av_select = "xpath=//select[@id='av_engine']"
        if av in ['mcafee', 'sophos']:
            self.select_from_list(av_select, '%s' % av)
        else:
            raise guiexceptions.ConfigError(
                    'Unknown antivirus: "%s". AV should be [mcafee | sophos]'
                    % av
            )

    def _set_sua_settings(self, setting, action):

        sua_monitor_link = "xpath=//td[@id='state_scan_sua']"
        sua_block_link = "xpath=//td[@id='state_block_sua']"
        sua_checkbox = "xpath=//input[@id='enable_sua']"

        sua_enabled = self._is_checked(sua_checkbox)
        if setting.strip().lower() == 'enable' and not sua_enabled:
            self.click_element(sua_checkbox, "don't wait")
        elif setting.strip().lower() == 'disable' and sua_enabled:
            self.click_element(sua_checkbox, "don't wait")
        if sua_enabled and action is not None:
            if action.strip().lower() == 'block':
                self.click_element(sua_block_link, "don't wait")
            if action.strip().lower() == 'monitor':
                self.click_element(sua_monitor_link, "don't wait")

    def _set_amp_file_rep_settings(self, setting, action):

        amp_file_rep_checkbox = "xpath=//input[@id='enable_amp_file_rep']"

        amp_file_rep_enabled = self._is_checked(amp_file_rep_checkbox)
        if setting.strip().lower() == 'enable' and not amp_file_rep_enabled:
            self.click_element(amp_file_rep_checkbox, "don't wait")

        if setting.strip().lower() == 'disable' and amp_file_rep_enabled:
            self.click_element(amp_file_rep_checkbox, "don't wait")

        link = None
        if action:
            if action.strip().lower() == 'monitor':
                link = 'state_scan_%s' % amp_known_malicious_locator
            elif action.strip().lower() == 'block':
                link = 'state_block_%s' % amp_known_malicious_locator
            else:
                raise guiexceptions.ConfigError(
                    'Unknown action: "%s". Should be [block | monitor' % action
                )

            self.click_element(link, "don't wait")

    def _set_wbrs_settings(self, setting, allow_boundary, block_boundary):

        web_reputation_checkbox = "xpath=//input[@id='enable_wbrs']"
        allow_boundary_input_id = 'custom_allow_boundary'
        block_boundary_input_id = 'custom_block_boundary'

        wbrs_enabled = self._is_checked(web_reputation_checkbox)
        if setting.strip().lower() == 'enable' and not wbrs_enabled:
            self.click_element(web_reputation_checkbox, "don't wait")

        if setting.strip().lower() == 'disable' and wbrs_enabled:
            self.click_element(web_reputation_checkbox, "don't wait")

        if setting.strip().lower() == 'enable':
            if allow_boundary is not None:
                self._set_input_value_with_javascript(
                    allow_boundary_input_id, allow_boundary)

            if block_boundary is not None:
                self._set_input_value_with_javascript(
                    block_boundary_input_id, block_boundary)

    def _open_acc_pol_page(self):
        """Go to Access Policies configuration page."""

        self._navigate_to('Web Security Manager', 'Access Policies')
        time.sleep(2)

    def _select_avc_setting_type(self, policytype):
        type_dict = {
            'global':  'default',
            'custom':  'custom'
        }

        if policytype.strip().lower() not in type_dict.keys():
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )
        self.select_from_list('settings_type', type_dict[policytype])

    def _select_ams_setting_type(self, policytype):
        type_dict = {
            'global':  'global',
            'custom':  'custom'
        }

        if policytype.strip().lower() not in type_dict.keys():
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )
        self.select_from_list('settings_type', type_dict[policytype])

    def _select_setting_type(self, policytype):
        type_dict = {
            'global':  'default',
             'custom':  'custom',
             'disable': 'disable'
        }

        if policytype.strip().lower() not in type_dict.keys():
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )
        self.select_from_list('settings_type', type_dict[policytype])

    def _select_protocols_setting_type(self, policytype):
        type_dict = {
            'global':  'global',
            'custom':  'custom',
            'disable': 'disable'
        }

        if policytype.strip().lower() not in type_dict.keys():
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )

        try:
            self._wait_until_element_is_present("id='settings_type'")
        except:
            time.sleep(3)
        self.select_from_list('settings_type', type_dict[policytype])

    def _edit_protocols_blocking(self, block_protocols):

        valid_protocols = {
            'ftpoverhttp': 'id=prot_ftp',
            'http': 'id=prot_http',
            'nativeftp': 'id=prot_nativeftp'
        }

        if self._is_visible('id=prot_https'):
            valid_protocols['https'] = 'id=prot_https'

        if isinstance(block_protocols, (str, unicode)):
            if block_protocols.strip().lower() == 'allow all':
                block_protocols = []
            elif block_protocols.strip().lower() == 'block all':
                block_protocols = valid_protocols.keys()
            else:
                block_protocols = list(self._convert_to_tuple(block_protocols))

        for protocol in valid_protocols.keys():
            if protocol in block_protocols:
                self.select_checkbox(valid_protocols[protocol])
            else:
                self.unselect_checkbox(valid_protocols[protocol])

    def _edit_user_agents_blocking(self, user_agents):

        self._info('User Agents: %s | Type: %s' % (user_agents, type(user_agents)))

        if isinstance(user_agents, str) or isinstance(user_agents, unicode):
            user_agents = (user_agents,)
        user_agents_text = '\r\n'.join(user_agents)
        self.input_text(
            "xpath=//textarea[@name='custom_user_agents']",
            user_agents_text
        )

    def _edit_connect_ports(self, ports):
        self.input_text("xpath=//input[@name='connect_ports']", ports)

    def _set_max_file_size_blocking(self, proto, file_size):
        prefix = {'http': '', 'ftp': 'ftp_'}[proto]
        if file_size.strip().isdigit():
            self._click_radio_button(
                "xpath=//input[@id='enforce_%sfile_size_limit_yes']" % prefix)
            self.input_text(
                "xpath=//input[@id='max_%sfile_size_mb']" %
                prefix,
                str(file_size)
            )

        else:
            self._click_radio_button(
                "xpath=//input[@id='enforce_%sfile_size_limit_no']" % prefix)

    def _set_blocking_of_predefined_objects(self, object_types, inspect_action):
        object_types = self._convert_to_tuple(object_types)
        for object_type in object_types:
            if object_type not in filetypes_locators_map:
                raise guiexceptions.ConfigError(
                    '"%s" object type is not predefined' % object_type
                )

        self._expand_all_predefined_objects()

        for file_type in filetypes_locators_map:
            if file_type in object_types:
                if inspect_action:
                    filetype_location = filetypes_locators_map[file_type].replace('Allow', 'Inspect')
                else:
                    filetype_location = filetypes_locators_map[file_type].replace('Allow', 'Block')

                if filetypes_locators_map[file_type].split(' ')[0] == 'Inspectable':
                    self._click_radio_button(
                        "xpath=//input[@id='%s']" % filetype_location
                    )
                else:
                    self.select_checkbox(
                        "xpath=//input[@id='%s']" % filetypes_locators_map[file_type]
                    )
            else:
                if filetypes_locators_map[file_type].split(' ')[0] == 'Inspectable':
                    self._click_radio_button(
                        "xpath=//input[@id='%s']" %
                        filetypes_locators_map[file_type]
                    )
                else:
                    self.unselect_checkbox(
                        "xpath=//input[@id='%s']" %
                        filetypes_locators_map[file_type]
                    )

    def _expand_all_predefined_objects(self):
        self._info('Expanding all categories')
        arrow_selector = "//div[starts-with(@id, 'arrow_closed')]"
        arrows = self._get_visible_elements(arrow_selector)
        for arrow in arrows:
            self.click_element(arrow, "don't wait")

    def _select_object_setting_type(self, policytype):
        type_dict = {
            'global':  'label=Use Global Policy Objects Blocking Settings',
            'custom':  'label=Define Custom Objects Blocking Settings',
            'disable': 'label=Disable Object Blocking for this Policy'
        }
        if policytype not in type_dict:
            raise guiexceptions.GuiValueError, (
                'Invalid setting type: "%s"' % policytype
            )
        self.select_from_list('settings_type', type_dict[policytype])

    def _select_categories(self, categories):

        link_id_malware = "xpath=//a[contains(@onclick,'block') and not(contains(@onclick,'sua'))]"
        link_id_other = "xpath=//a[contains(@onclick,'block') and contains(@onclick,'sua')]"
        for category in categories:
            cat, action = \
                self._convert_to_tuple_from_colon_separated_string(category)

            if cat not in mwcats_locators_map:
                raise guiexceptions.ConfigError('Unknown category: "%s"' % cat)

            if action.strip().lower() == 'block':
                link = 'state_block_%s' % mwcats_locators_map[cat]
            elif action.strip().lower() == 'monitor':
                link = 'state_scan_%s' % mwcats_locators_map[cat]
            elif action.strip().lower() == 'blockall':
                if cat == 'All Malware':
                    link = link_id_malware
                elif cat == 'Other Malware':
                    link = link_id_other
            else:
                raise guiexceptions.ConfigError(
                    'Unknown action: "%s". Should be [block | monitor]' % action
                )

            self.click_element(link, "don't wait")

    def access_policies_edit_applications(
        self,
        name,
        defaults=None,
        actions=None,
        bypass_avc=None,
        range_request_settings=None,
        settings_type='custom'
    ):
        """Setups applications setting for the certain access policy.

        Document that describes applications and applications types van be found
        here.

        Parameters:
        - `name`: The name of the edited policy. String. Mandatory.
        - `default`: default application types settings. Makes sense for Global
        Policy only. List with items, each item contains 3 values separated by
        colon. First value is application type, second is default action
        ('block' or 'monitor'), and last one is bandwidth limit (i.e: 10 kbps,
        100 mbps). If bandwidth limit is not applicable for certain
        application type - leave it blank.
        - `actions`: aplication settings. List with items, each item contains 4
        values separated by colon. First value is application type, second is
        action ('global', 'block', 'monitor'), third set of is blocking options
        (block types separated by semicolon), and last one is bandwidth limit
        usage option (either 'yes' or 'no'. Leave blank if not applicable).
        - `settings_type`: either 'custom' or 'global'.
        - `bypass_avc`: either `True` or `False`
        - `range_request_settings' - Exception list for range request bypass
        list of clients or destinations separated by ';'
        -NOTE:bypass_avc and range_request_settings  options valid only if Range Request Forwarding
        is enabled in Web Proxy Settings

        Exceptions:
        - GuiValueError:Invalid setting type - xxx
        - ConfigError:Invalid bandwidth limit configuration for application types
        - GuiControlNotFoundError:<app_type> Access Policies
        - ValueError:Argument xxx should be string type

        Examples:
        | @{apps} | Set Variable |
        | ... | ${applications.FLASH}:monitor::yes |
        | ... | ${applications.YAHOO_IM}:monitor:block_file: |

        | @{apps1} | Set Variable |
        | ... | ${applications.BITTORRENT}:block:: |
        | ... | ${applications.WEBEX}:monitor:: |

        | @{defs} | Set Variable |
        | ... | ${applications.MEDIA}:monitor:10 Mbps |
        | ... | ${applications.SOCIAL}:block: |

        | Access Policies Edit Applications | Global Policy |
        | ... | defaults=${defs} |
        | ... | actions=${apps} |

        | Access Policies Edit Applications | test |
        | ... | actions=${apps1} |

        | Access Policies Edit Applications | test |
        | ... | bypass_avc=True |

        | Access Policies Edit Applications | test |
        | ... | range_request_settings=ebay.com;foo.com;dot.com |
        """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_applications_column)
        if name.strip().lower() == 'global policy':
            if defaults is not None:
                self._edit_avc_defaults(defaults)
        else:
            self._select_avc_setting_type(settings_type)

        if actions is not None:
            self._edit_avc_actions(actions)

        if bypass_avc is not None:
            value = "0"
            if bypass_avc:
                value = "1"
            self.select_from_list('id=bypass_avc', value)
        if range_request_settings:
            self._info("Got the exception list - %s" % range_request_settings)
            exception_list = range_request_settings.split(';')
            exception_list = '\n'.join(exception_list)
            exception_list_field = 'exception'
            self.input_text(exception_list_field, exception_list)

        self._click_submit_button()

    def _edit_avc_defaults(self, defaults):
        defaults = self._convert_to_tuple(defaults)
        for item in defaults:
            app_type, action, bw_limit = \
                self._convert_to_tuple_from_colon_separated_string(item)
            self._edit_default_avc_inline(app_type, action, bw_limit)

    def _edit_default_avc_inline(self, app_type, action, bw_limit):
        """
        - `setting`: an object with attributes:
            -`action`: Either MonitorAction or BlockAction.
            -`bw_limit`: 'no', '2 kbps', '10 mbps'
        """
        SUBMIT_BUTTON = lambda id: 'id=button_submit_actions_%s' % id
        SUBMIT_BW_BUTTON = lambda id: 'id=button_submit_bw_%s' % id
        ACTION_DIALOG_LINK = lambda id: 'id=type_default_action_link_%s' % id
        BW_DIALOG_LINK = lambda id: 'id=bandwidth_link_%s' % id
        BW_LIMIT_BOX = lambda id: 'bandwidth_limit_%s' % id
        BW_UNITS_COMBO = lambda id: 'bandwidth_units_%s' % id
        BW_UNITS_VALUE = lambda val: '%s' % val

        avc_actions_map = lambda action_type, id: {
            'monitor': 'type_actions_%s_scan',
            'block': 'type_actions_%s_block'
            }[action_type] % id

        avc_bandwith_map = lambda setting, id: {
            'no': 'bandwidth_%s_no_limit_type',
            'yes': 'bandwidth_%s_limit'
        }[setting] % id

        self.click_element(ACTION_DIALOG_LINK(app_type), "don't wait")

        loc = avc_actions_map(action, app_type)
        self._click_radio_button(loc)

        self.click_element(SUBMIT_BUTTON(app_type), "don't wait")

        if action.strip().lower() == 'monitor':
            if bw_limit is not None:
                self.click_element(BW_DIALOG_LINK(app_type), "don't wait")
                if bw_limit.strip().lower() == 'no':
                    self._click_radio_button(
                            avc_bandwith_map('no', app_type))
                else:
                    self._click_radio_button(
                            avc_bandwith_map('yes', app_type))
                    size, units = bw_limit.split()
                    if size.isdigit() and units.lower() in ['kbps', 'mbps']:
                        self.input_text(BW_LIMIT_BOX(app_type), size)
                        self.select_from_list(
                            BW_UNITS_COMBO(app_type),
                            BW_UNITS_VALUE(units.lower())
                        )
                    else:
                        raise guiexceptions.ConfigError(
                            'Invalid bandwidth limit configuration for application types'
                        )

            self.click_element(SUBMIT_BW_BUTTON(app_type), "don't wait")

    def _edit_avc_actions(self, actions):
        actions = self._convert_to_tuple(actions)
        for item in actions:
            setting = self._convert_to_tuple_from_colon_separated_string(item)
            self._edit_avc_action_via_browse(setting)

    def _edit_avc_action_via_browse(self, setting):

        DIALOG_LINK = lambda id: 'id=app_action_descr_%s' % (id,)
        APP_TYPE_EXPANDED_LOC = lambda id: 'id=type_name_expanded_%s' % (id,)
        APP_TYPE_NODE_LOC = lambda id: "xpath=//table[@id='browse_content']" + \
            "//a[contains(@href, \"avc_objects['%s']\")]" % id

        app = setting[0]
        app_to_app_type_map = {
            # Blogging
            applications.BLOGGER.id: applications.BLOGGING,
            applications.DISQUS.id: applications.BLOGGING,
            applications.FC2BLOG.id: applications.BLOGGING,
            applications.LIVEJOURNAL.id: applications.BLOGGING,
            applications.TUMBLR.id: applications.BLOGGING,
            applications.WORDPRESS.id: applications.BLOGGING,
            # Collaboration
            applications.ANSWERS.id: applications.COLLABORATION,
            applications.PASTEBIN.id: applications.COLLABORATION,
            applications.WIKIPEDIA.id: applications.COLLABORATION,
            # Enterprise Applications
            applications.AMAZONS3.id: applications.ENTERPRISEAPP,
            applications.CONCUR.id: applications.ENTERPRISEAPP,
            applications.SHAREPOINT.id: applications.ENTERPRISEAPP,
            applications.SUGARCRM.id: applications.ENTERPRISEAPP,
            # Facebook
            applications.FACEBOOKAPP_ENTERTAINMENT.id: applications.FACEBOOK,
            applications.FACEBOOKAPP_GAMES.id: applications.FACEBOOK,
            applications.FACEBOOKAPP_OTHER.id: applications.FACEBOOK,
            applications.FACEBOOKAPP_SPORTS.id: applications.FACEBOOK,
            applications.FACEBOOKAPP_UTILITIES.id: applications.FACEBOOK,
            applications.FACEBOOKEVENTS.id: applications.FACEBOOK,
            applications.FACEBOOKGENERAL.id: applications.FACEBOOK,
            applications.FACEBOOKCHAT.id: applications.FACEBOOK,
            applications.FACEBOOKNOTES.id: applications.FACEBOOK,
            applications.FACEBOOKPHOTOSVIDEOS.id: applications.FACEBOOK,
            # File Sharing
            applications.RAPIDSHARE.id: applications.P2P,
            applications.FOURSHARED.id: applications.P2P,
            applications.BITTORRENT.id: applications.P2P,
            applications.YOUSENDIT.id: applications.P2P,
            # Games
            applications.EVONY.id: applications.GAMES,
            applications.HANGAMECOJP.id: applications.GAMES,
            applications.POGO.id: applications.GAMES,
            applications.WII.id: applications.GAMES,
            # Google +
            applications.GOOGLEPLUSGAMES.id: applications.GOOGLEPLUS,
            applications.GOOGLEPLUSGENERAL.id: applications.GOOGLEPLUS,
            applications.GOOGLEPLUSHANGOUTS.id: applications.GOOGLEPLUS,
            applications.GOOGLEPLUSLOCATION_TAGGING.id: applications.GOOGLEPLUS,
            applications.GOOGLEPLUSPHOTOS.id: applications.GOOGLEPLUS,
            applications.GOOGLEPLUSVIDOES.id: applications.GOOGLEPLUS,
            # Instant Messaging
            applications.AOL_IM.id: applications.IM,
            applications.FETION.id: applications.IM,
            applications.GTALK.id: applications.IM,
            applications.ILOVEIM.id: applications.IM,
            applications.KOOLIM.id: applications.IM,
            applications.MESSENGERFX.id: applications.IM,
            applications.MIBBIT.id: applications.IM,
            applications.MSN_IM.id: applications.IM,
            applications.WECHATWEB.id: applications.IM,
            applications.YAHOO_IM.id: applications.IM,
            # Internet Utilities
            applications.EBAY.id: applications.IM,
            applications.GOOGLEANALYTICS.id: applications.IM,
            applications.GOOGLEAPPENGINE.id: applications.IM,
            applications.GOOGLECALENDAR.id: applications.IM,
            applications.GOOGLEMAP.id: applications.UTILITIES,
            applications.GOOGLETRANSLATE.id: applications.IM,
            applications.YAHOOTOOLBAR.id: applications.IM,
            # iTunes
            applications.ITUNES_DESKTOP.id: applications.IM,
            applications.ITUNES_IPAD.id: applications.IM,
            applications.ITUNES_IPHONE.id: applications.IM,
            applications.ITUNES_IPOD.id: applications.IM,
            # LinkedIn
            applications.LINKEDINCONTACTS.id: applications.LINKEDIN,
            applications.LINKEDINGENERAL.id: applications.LINKEDIN,
            applications.LINKEDININBOX.id: applications.LINKEDIN,
            applications.LINKEDINJOBS.id: applications.LINKEDIN,
            applications.LINKEDINPROFILE.id: applications.LINKEDIN,
            # Media
            applications.MEDIA500PX.id: applications.MEDIA,
            applications.MEDIA56COM.id: applications.MEDIA,
            applications.ASF.id: applications.MEDIA,
            applications.DAILYMOTION.id: applications.MEDIA,
            applications.DEEZER.id: applications.MEDIA,
            applications.FLASH.id: applications.MEDIA,
            applications.FOTKI.id: applications.MEDIA,
            applications.FREEETV.id: applications.MEDIA,
            applications.GYAO.id: applications.MEDIA,
            applications.HULU.id: applications.MEDIA,
            applications.JANGO.id: applications.MEDIA,
            applications.JOOST.id: applications.MEDIA,
            applications.LASTFM.id: applications.MEDIA,
            applications.LIVE365.id: applications.MEDIA,
            applications.LIVESTREAM.id: applications.MEDIA,
            applications.MEGAVIDEO.id: applications.MEDIA,
            applications.MPEG.id: applications.MEDIA,
            applications.NETFLIX.id: applications.MEDIA,
            applications.NICONICODOUGA.id: applications.MEDIA,
            applications.PANDORA.id: applications.MEDIA,
            applications.PANDORATV.id: applications.MEDIA,
            applications.PHOTOBUCKET.id: applications.MEDIA,
            applications.PICASA.id: applications.MEDIA,
            applications.PLAYMUSIC.id: applications.MEDIA,
            applications.PPSTV.id: applications.MEDIA,
            applications.PPTV.id: applications.MEDIA,
            applications.QTIME.id: applications.MEDIA,
            applications.REAL_MEDIA.id: applications.MEDIA,
            applications.SOHUVIDEO.id: applications.MEDIA,
            applications.SHUTTERFLY.id: applications.MEDIA,
            applications.SILVERLIGHT.id: applications.MEDIA,
            applications.SMUGMUG.id: applications.MEDIA,
            applications.TUDOU.id: applications.MEDIA,
            applications.VIDDLER.id: applications.MEDIA,
            applications.VIMEO.id: applications.MEDIA,
            applications.WINAMPREMOTE.id: applications.MEDIA,
            applications.WIN_MEDIA.id: applications.MEDIA,
            applications.YOUKU.id: applications.MEDIA,
            applications.YOUTUBE.id: applications.MEDIA,
            applications.IMDB.id: applications.MEDIA,
            # Myspace
            applications.MYSPACEGENERAL.id: applications.MYSPACE,
            applications.MYSPACEMUSIC.id: applications.MYSPACE,
            applications.MYSPACEPHOTOS.id: applications.MYSPACE,
            applications.MYSPACEVIDEOS.id: applications.MYSPACE,
            # Presentation/Conferencing
            applications.CROSSLOOP.id: applications.TELEPRESENCE,
            applications.EROOMNET.id: applications.TELEPRESENCE,
            applications.GLIDE.id: applications.TELEPRESENCE,
            applications.TEAMVIEWER.id: applications.TELEPRESENCE,
            applications.TECHINLINE.id: applications.TELEPRESENCE,
            applications.TWIDDLA.id: applications.TELEPRESENCE,
            applications.WEBEX.id: applications.TELEPRESENCE,
            # Proxies
            applications.ASPROXY.id: applications.PROXIES,
            applications.AVOIDR.id: applications.PROXIES,
            applications.CAMOPROXY.id: applications.PROXIES,
            applications.CGIPROXY.id: applications.PROXIES,
            applications.CORALCDN.id: applications.PROXIES,
            applications.FLYPROXY.id: applications.PROXIES,
            applications.GLYPE.id: applications.PROXIES,
            applications.GUARDSTER.id: applications.PROXIES,
            applications.KPROXY.id: applications.PROXIES,
            applications.MEGAPROXY.id: applications.PROXIES,
            applications.OTHERWEBPROXY.id: applications.PROXIES,
            applications.PHPPROXY.id: applications.PROXIES,
            applications.PROXONO.id: applications.PROXIES,
            applications.SOCKS2HTTP.id: applications.PROXIES,
            applications.SURESOME.id: applications.PROXIES,
            applications.SURROGAFIER.id: applications.PROXIES,
            applications.VTUNNEL.id: applications.PROXIES,
            applications.ZELUNE.id: applications.PROXIES,
            # Social Networking
            applications.AMEBA.id: applications.SOCIAL,
            applications.DELICIOUS.id: applications.SOCIAL,
            applications.DIGG.id: applications.SOCIAL,
            applications.FRIENDFEED.id: applications.SOCIAL,
            applications.GOOGLEGROUPS.id: applications.SOCIAL,
            applications.GOOGLEWAVE.id: applications.SOCIAL,
            applications.GREE.id: applications.SOCIAL,
            applications.KAIXIN001.id: applications.SOCIAL,
            applications.MIXI.id: applications.SOCIAL,
            applications.PINTEREST.id: applications.SOCIAL,
            applications.QUORA.id: applications.SOCIAL,
            applications.REDDIT.id: applications.SOCIAL,
            applications.RENREN.id: applications.SOCIAL,
            applications.SCRIBD.id: applications.SOCIAL,
            applications.SLASHDOT.id: applications.SOCIAL,
            applications.SNAPCHAT.id: applications.SOCIAL,
            applications.SOHUWEIBO.id: applications.SOCIAL,
            applications.STUMBLEUPON.id: applications.SOCIAL,
            applications.TENCENTWEIBO.id: applications.SOCIAL,
            applications.TWITTER.id: applications.SOCIAL,
            applications.TWOCHANNEL.id: applications.SOCIAL,
            applications.VIADEO.id: applications.SOCIAL,
            applications.WEIBO.id: applications.SOCIAL,
            applications.XING.id: applications.SOCIAL,
            applications.YAHOOMOBAGE.id: applications.SOCIAL,
            applications.YIKYAK.id: applications.SOCIAL,
            applications.ZHIHU.id: applications.SOCIAL,
            # Software Updates
            applications.MACAFEE_UPDATE.id: applications.UPDATES,
            applications.SOPHOS_UPDATE.id: applications.UPDATES,
            applications.SYMANTEC_UPDATE.id: applications.UPDATES,
            applications.TRENDMICRO_UPDATE.id: applications.UPDATES,
            applications.WINDOWS_UPDATE.id: applications.UPDATES,
            # Webmail
            applications.AOLMAIL.id: applications.WEBMAIL,
            applications.COMCASTMAIL.id: applications.WEBMAIL,
            applications.EYEJOT.id: applications.WEBMAIL,
            applications.GMAIL.id: applications.WEBMAIL,
            applications.GMXEMAIL.id: applications.WEBMAIL,
            applications.HUSHMAIL.id: applications.WEBMAIL,
            applications.MAILRU.id: applications.WEBMAIL,
            applications.MOBILEME.id: applications.WEBMAIL,
            applications.OUTLOOK.id: applications.WEBMAIL,
            applications.YAHOOMAIL.id: applications.WEBMAIL,
        }

        self.select_from_list('id=page_mode', 'browse')
        # expand app type group.
        app_type = app_to_app_type_map[app]
        if not self._is_element_present(APP_TYPE_NODE_LOC(app_type.id)):
            raise guiexceptions.GuiControlNotFoundError(app_type,
                                                        'Access Policies')

        if not self._is_visible(APP_TYPE_EXPANDED_LOC(app_type.id)):
            self.click_element(APP_TYPE_NODE_LOC(app_type.id), "don't wait")

        # edit in inline edit dialog
        self.click_element(DIALOG_LINK(app), "don't wait")
        self._edit_avc_app_inline(setting)

    def _edit_avc_app_inline(self, setting):
        """ Both Application and Application Type can be edited there

        - `setting`: an object with attributes:
            -`action`: Either GlobalAction, MonitorAction, or BlockAction.
            -`block`: tuple. `generic`, `file`, `unsafe`
            -`bw_limit`: 'global', 'no'
        """
        app, action, block, bw_limit = setting
        CANCEL_BUTTON = lambda id: 'id=button_cancel_actions_%s' % id
        SUBMIT_BUTTON = lambda id: 'id=button_submit_actions_%s' % id

        avc_actions_map = lambda action_type, id: {
            'global': 'actions_%s_not_defined',
            'monitor': 'actions_%s_scan',
            'block': 'actions_%s_block'
            }[action_type] % id

        avc_behavior_map = {
            'block_generic': lambda id: 'behaviors_%s_200' % id,
            'block_file': lambda id: 'behaviors_%s_201' % id,
            'block_unsafe': lambda id: 'behaviors_%s_202' % id,
            'block_upload': lambda id: 'behaviors_%s_205' % id,
            'block_posting': lambda id: 'behaviors_%s_206' % id,
            'block_like': lambda id: 'behaviors_%s_207' % id,
            'block_install': lambda id: 'behaviors_%s_208' % id,
            'block_tweats': lambda id: 'behaviors_%s_210' % id,
            'block_clients': lambda id: 'behaviors_%s_211' % id,
            'block_apps': lambda id: 'behaviors_%s_212' % id,
            'block_job_search': lambda id: 'behaviors_%s_213' % id,
            'block_job_post': lambda id: 'behaviors_%s_214' % id,
            'block_recomendations': lambda id: 'behaviors_%s_215' % id,
            'block_groups': lambda id: 'behaviors_%s_216' % id,
            'block_events': lambda id: 'behaviors_%s_217' % id,
            'block_status': lambda id: 'behaviors_%s_218' % id,
            'block_file_upload': lambda id: 'behaviors_%s_219' % id,
            'block_file_downlaod': lambda id: 'behaviors_%s_220' % id,
            'block_email_send': lambda id: 'behaviors_%s_221' % id,
        }

        block = self._convert_to_tuple_from_semicolon_separated_string(block)

        avc_bandwith_map = lambda setting, id: {
            'yes': 'bandwidth_%s_not_defined',
            'no': 'bandwidth_%s_no_limit'
        }[setting] % id

        loc = avc_actions_map(action, app)
        self._click_radio_button(loc)

        # Monitor Action also enables setting blocking some content and
        # limiting bandwith
        if action.strip().lower() == 'monitor':
            # Selective content blocking
            if block:
                for k, v in avc_behavior_map.items():
                    avc_behavior_loc = v(app)
                    if self._is_element_present(avc_behavior_loc):
                        if k in block:
                            self.select_checkbox(avc_behavior_loc)
                        else:
                            self.unselect_checkbox(avc_behavior_loc)

            # Bandwith limit
            if bw_limit:
                self._click_radio_button(avc_bandwith_map(bw_limit, app))

        # Submit inline edit dialog
        self.click_element(SUBMIT_BUTTON(app), "don't wait")

    def access_policies_edit_url_categories(
        self,
        name,
        url_categories=None,
        uncategorized_action=None,
        enable_overall_quota=None,
        overall_quota=None
    ):

        """Edit specified access policy URL categories settings.

        Parameters:
        - `name`: name of the policy to edit.

        - `url_categories`:  a string of comma separated items or a list of
        items. Each item is string with values separated by colon.

    - 'enable_overall_quota' : 'True' To enable Time quota Notification
        'False' To disable time quota and 'None' To use current or default value.

    - 'overall_quota' : quota profile name to be used.
    | First value is url category object,
        | second value is action

        | (Available actions for predefined url categories:
        | 'global', 'block', 'monitor', 'warn', 'timebased', 'quotabased'.
        | Available actions for custom url categories:
        | 'block', 'redirect', 'allow', 'warn', 'monitor', 'timebased', 'quotabased').

        | If 'redirect' action is selected next value is redirect url.
        | If 'timebased' action is selected next values are:
        | time range, time based action and other time based action.
        | If time based action is
        'redirect', redirect url should be specified after dash sign. i.e:
        'redirect-http://yandex.ru'.

        - `uncategorized_action`: the action undertaken for uncategorized URLs.

        Exceptions:
        - GuiControlNotFoundError: <category> <location>

        Examples:
        | @{url_cats}= | Set Variable | ${webcats.ADULT}:block | ${webcats.CHAT}:warn |

        | Access Policies Edit Url Categories | myNewTestPolicy |
        | ... | ${url_cats} |
        | ... | block |

        | @{url_cats}= | Set Variable |
        | ... | testCustomUrlCat1:timebased:testCustomTR1:redirect-http://yandex.ru:redirect-http://google.com |
        | ... | ${webcats.COMPUTER_SEC}:timebased:testCustomTR2:monitor:block |

        | Access Policies Edit Url Categories | testPolicyWithTimebasedCategories |
        | ... | ${url_cats} |

        | Access Policies Edit Url Categories | testPolicyWithRedirectCategories |
        | ... | testCustomUrlCat1:redirect:http://yandex.ru, testCustomUrlCat2:redirect:http://google.com |

    | @{url_cats}= | Set Variable |
        | ... | testCustomUrlCat1:quotabased:testCustomTQ1 |
        | ... | ${webcats.COMPUTER_SEC}:quotabased:testCustomTQ2 |

        | Access Policies Edit Url Categories | testPolicyWithQuotabasedCategories |
        | ... | ${url_cats} |
    | ... | ${True} |
    | ... | testCustomTQ2 |
    """

        self._open_acc_pol_page()
        self._click_edit_policy_link(name, self.ap_url_filtering_column)

        if url_categories is not None:
            custom_cats = self._get_custom_url_categories()
            predefined_cats = self._get_predefined_url_categories()
            url_categories = self._convert_to_tuple(url_categories)
            for item in url_categories:
                item = self._convert_to_tuple_from_colon_separated_string(item)
                cat = item[0]
                # set default action to monitor if not specified
                if len(item) == 1:
                    action = 'monitor'
                else:
                    action = item[1].lower()

                if action.strip().lower() == 'timebased':
                    timerange = item[2]
                    tb_action = item[3]
                    index = 4        # starts checking following list items
                    if tb_action.startswith('redirect'):
                        while not item[index].startswith('redirect'):
                            index += 1
                        tb_action = ':'.join(item[3:index])
                    tb_otherwise = ':'.join(item[index:])
                    redirect_link = None
                    quota = None

                elif action.strip().lower() == 'quotabased':
                    quota = item[2]
                    timerange = None
                    tb_action = None
                    tb_otherwise = None
                    redirect_link = None

                elif action.strip().lower() == 'redirect':
                    redirect_link = ':'.join(item[2:])
                    timerange = None
                    tb_action = None
                    tb_otherwise = None
                    quota = None

                else:
                    timerange = None
                    tb_action = None
                    tb_otherwise = None
                    redirect_link = None
                    quota = None

                if cat in custom_cats:
                    self._edit_url_category(
                        action,
                        custom_cats[cat],
                        timerange,
                        tb_action,
                        tb_otherwise,
                        redirect_link, quota
                    )

                elif cat in predefined_cats:
                    self._edit_url_category(
                        action,
                        predefined_cats[cat],
                        timerange,
                        tb_action,
                        tb_otherwise,
                        redirect_link,
                        quota
                    )

                else:
                    raise guiexceptions.GuiControlNotFoundError(
                        cat,
                        self.get_location()
                    )

        if enable_overall_quota is None:
            self._info("Overall quota not applied")

        elif enable_overall_quota:
            self.select_from_list('prequota_profile', overall_quota)
            self._info("Overall quota applied")

        else:
            self.select_from_list('prequota_profile', 'Select Time and Volume Quota ...')

        if uncategorized_action is not None:
            self._select_uncategorized_urls_action(uncategorized_action)
        self._click_submit_button()

    def _convert_to_tuple_from_semicolon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(';')])
        else:
            raise ValueError(
                'Argument \'%s\' should be string type.' % user_input
            )
        return user_input

    def _convert_to_tuple_from_colon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError(
                'Argument \'%s\' should be string type.' % user_input
            )
        return user_input

    def _select_uncategorized_urls_action(self, uncategorized_action):
        actions_list = 'id=uncategorized_action'
        allowed_actions = ['global', 'block', 'monitor', 'warn']

        if uncategorized_action not in allowed_actions:
            raise guiexceptions.ConfigError(
                'Unknown uncategorized URLs action: "%s"' %
                uncategorized_action
            )

        self._select_action_combo(actions_list, uncategorized_action)

    def access_policies_disable_referrer_content(self, policy_name):
        """Disables referrer content section in access policy

        Parameters:
            - `policy_name` - Specify the policy name to edit

        Examples:
            | Access Policies Disable Referrer Content  Global Policy
        """
        # xpaths required for disabling referrer content
        ENABLE_REFERRER_CONTENT_LOCATOR = "xpath=//input[@id=\'enable_exception\']"

        # Open access policies pages and click on the mentioned policy to edit
        self._open_acc_pol_page()
        self._click_edit_policy_link(policy_name, self.ap_url_filtering_column)

        # Enable checkbox to disable referrer content
        self._wait_until_element_is_present(ENABLE_REFERRER_CONTENT_LOCATOR)
        if self._is_checked(ENABLE_REFERRER_CONTENT_LOCATOR):
            self.click_element(ENABLE_REFERRER_CONTENT_LOCATOR)

            # Click submit only if referrer content is disabled
            self._wait_until_element_is_present("xpath=//input[@value=\'Submit\'][2]")
            self.click_element("xpath=//input[@value=\'Submit\'][2]")

    def access_policies_edit_referrer_content(
        self,
        policy_name,
        source_referrer_content=None,
        dest_referrer_option=None,
        dest_referrer_content=None
    ):

        """Sets referrer content in access policy

        Parameters:
            - `policy_name` - Specify the policy name to edit
            - `source_referrer_content` - Source refferer content
                                          Custom URL Cats : Predefined URL Cats
            - `dest_refferer_option` - Specify the destination referrer option
                                     all | except | selected
            - `dest_referrer_content` - Specify destination referrer content forthe
                                        option selected
                                        Custom URL Cats : Predefined URL Cats for either Categories or Applications

        Returns the row number that is created.

        Examples:
        ${row_no}=  | Access Policies Edit Referrer Content  Global Policy
                    ...  source_referrer_content=all:Adult#Alcohol
                    ...  dest_referrer_option=except|all|selected
                    ...  destination_referrer_content=cat@MyCat2:Adult#Tobacco#MyCat1||app@Picasa#Pandora

        Note: While specifying source and destination referrer content, ':' in categories is mandatory which will
        differentiate custom and pre-defined URL categories
        """

        # xpaths required for handling referrer header on the main table
        ENABLE_REFERRER_CONTENT_LOCATOR = "xpath=//input[@id=\'enable_exception\']"
        DEFAULT_ROW_LOCATOR = "//table[@id=\'exceptions\']/tbody/tr/td/a[contains(text(), \'Click to select\')]"
        ADD_EXCEPTION_BUTTON_LOCATOR = "xpath=//input[@id='exceptions_domtable_AddRow']"
        ADD_CATEGORY_LOCATOR = lambda row: "xpath=//a[@id=\'categories_selection_%s\']" % (row,)

        if not source_referrer_content:
            raise guiexceptions.GuiValueError, ('Source referrer content is mandatory')

        if not dest_referrer_option:
            raise guiexceptions.GuiValueError, ('Destination referrer content is mandatory')

        # Open access policies pages and click on the mentioned policy to edit
        self._open_acc_pol_page()
        self._click_edit_policy_link(policy_name, self.ap_url_filtering_column)

        # Check if referrer content is enabled; if not enable it
        self._wait_until_element_is_present(ENABLE_REFERRER_CONTENT_LOCATOR)
        if not self._is_checked(ENABLE_REFERRER_CONTENT_LOCATOR):
            self.click_element(ENABLE_REFERRER_CONTENT_LOCATOR)

        # Check if new row has to be added in the referrer content table
        new_rows = None

        # Check if default row exists in the referrer content table
        new_rows = self._find_elements(DEFAULT_ROW_LOCATOR)
        if new_rows == None:
            self._info('Clicking on Add Exception button')
            self._wait_until_element_is_present(ADD_EXCEPTION_BUTTON_LOCATOR)
            self.click_element(ADD_EXCEPTION_BUTTON_LOCATOR)

        # Get the row id from the xpath of the row which got created above
        current_row = self._get_element_id(DEFAULT_ROW_LOCATOR)

        # Find the current row no by splitting the row id and take the last index
        current_url_cat_row = current_row.split('_')[2]

        # Set the source referrer content
        self._set_source_referrer_content(current_url_cat_row, source_referrer_content)

        # Set the destination referrer content
        self._set_dest_referrer_content(current_url_cat_row,
                                        dest_referrer_option,
                                        dest_referrer_content)

        # Click the Submit button
        self._wait_until_element_is_present("xpath=//input[@value=\'Submit\'][2]")
        self.click_element("xpath=//input[@value=\'Submit\'][2]")

        # Return the run number that got created in this keyword
        return current_url_cat_row

    def _set_source_referrer_content(self, current_row_no, referrer_content):
        # This function is used to handle referrer source content in UI

        # xpaths to handle source referrer content
        ADD_CATEGORY_LOCATOR = lambda row_no: "xpath=//a[@id=\'categories_selection_%s\']" % row_no
        DONE_BUTTON_LOCATOR = "xpath=//input[@title=\'Done\']"
        URL_CAT_LOCATOR = lambda category: "xpath=//*[contains(text(), \'%s\')]/parent::tr/td[2]/div" % category

        # Click on Add category to select the categories
        self._wait_until_element_is_present(ADD_CATEGORY_LOCATOR(str(current_row_no)))
        self.click_element(ADD_CATEGORY_LOCATOR(str(current_row_no)))

        # Wait for the URL category page to be loaded
        self.wait_until_page_loaded()

        # Split custom URL categories and predefined categories
        category_types = referrer_content.split(':')

        # Set the URL categories supplied to keyword
        self._select_url_categories(category_types, URL_CAT_LOCATOR)

        # Click on page done once all the categories are selected
        self.click_element(DONE_BUTTON_LOCATOR)

    def _set_dest_referrer_content(self, current_row_no, referrer_option, referrer_content):
        # This function sets destination referrer content on the UI

        # xpaths required to set destination referrer content
        REFERRER_OPTION_LOCATOR = lambda row: 'exceptions[%s][type_selection]' % (row,)
        CAT_OPTION_LOCATOR = lambda row: "xpath=//a[@id=\'categories_exception_%s\']" % (row,)
        APP_OPTION_LOCATOR = lambda row: "xpath=//a[@id=\'applications_exception_%s\']" % (row,)
        CAT_ELEMENT_LOCATOR = lambda category: "xpath=//*[contains(text(), \'%s\')]/parent::tr/td[2]/div" % (category,)
        APP_ELEMENT_LOCATOR = lambda category: "xpath=//div[text()=\'%s\']/parent::td/following-sibling::td/div/input" % (category,)
        DONE_BUTTON_LOCATOR = "xpath=//input[@title=\'Done\']"

        # Mapping for setting exception for referred content
        referrer_option_map = {
            'all': '0',
            'selected': '1',
            'except': '2',
        }

        select_option = referrer_option_map[referrer_option]

        # Select the referrer option select menu
        self._wait_until_element_is_present(REFERRER_OPTION_LOCATOR(current_row_no))
        self.select_from_list(REFERRER_OPTION_LOCATOR(current_row_no), select_option)

        # Check if referrer option is not all
        if referrer_option != 'all':
            referrer_option_content = referrer_content.split('||')
            for option_type in referrer_option_content:
                type, content = option_type.split('@')
                if type == 'cat':
                    option_locator = CAT_OPTION_LOCATOR(current_row_no)
                    content_locator = CAT_ELEMENT_LOCATOR
                elif type == 'app':
                    option_locator = APP_OPTION_LOCATOR(current_row_no)
                    content_locator = APP_ELEMENT_LOCATOR

                self._add_dest_referrer_content(
                    current_row_no,
                    type,
                    option_locator,
                    content_locator,
                    content
                )

                self._wait_until_element_is_present(DONE_BUTTON_LOCATOR)
                # Click on page done once all the categories are selected
                self.click_element(DONE_BUTTON_LOCATOR)

    def _add_dest_referrer_content(
        self,
        current_row_no,
        type,
        option_locator,
        content_locator,
        content
    ):
        # This function is used to set the destination content

        # xpaths
        APP_SELECT_ALL_LOCATOR = "xpath=//input[@id=\'select_all\']"

        # Select the referrer option content type i.e category or application
        self._wait_until_element_is_present(option_locator)
        self.click_element(option_locator)

        # Split custom cat and predefined cat
        category_types = content.split(':')

        if type == 'cat':
            self._select_url_categories(category_types, content_locator)
        elif type == 'app':
            if category_types[0] == 'all':
                self._wait_until_element_is_present(APP_SELECT_ALL_LOCATOR)
                self.click_element(APP_SELECT_ALL_LOCATOR)
            else:
                self._select_category(category_types[0], content_locator)

    def _select_url_categories(self, category_types, content_locator):

        # xpaths required for selecting individual category
        SELECT_ALL_LOCATOR = lambda event: "xpath=//a[contains(@onclick, \'%s\')]" % (event,)

        # set the categories specified in the source content
        for index, category_type in enumerate(category_types):

            # Check if select all is set
            if category_type == 'all':

                # Set which select-all has to be clicked - cust cat or predefined cat
                if index == 0:
                    onclick_event_name = 'memberscustomcat'
                else:
                    onclick_event_name = 'memberswebcat'

                self._wait_until_element_is_present(SELECT_ALL_LOCATOR(onclick_event_name))
                self.click_element(SELECT_ALL_LOCATOR(onclick_event_name))
            else:
                self._select_category(category_type, content_locator)

    def _select_category(self, categories, content_locator):

        if categories:
           # Split the categories to add exception
            url_categories = categories.split('#')

        if url_categories:
            for url_category in url_categories:
                self._wait_until_element_is_present(content_locator(url_category))
                self.click_element(content_locator(url_category))

    def access_policies_delete_referrer_content(self, policy_name, content):
        """Deletes specified or all referrer content in the access policy

        Parameters:
            - `policy_name` : Access policy name
            - `content` : referrer content to be deleted

        Example:
            | Access Policies Delete Referrer Content | myPolicy | all
        """

        # xpaths required for deleting referrer content
        ENABLE_REFERRER_CONTENT_LOCATOR = "xpath=//input[@id=\'enable_exception\']"
        ROW_LOCATOR = "//tr[contains(@id,\'exceptions_row\')]"
        DELETE_ROW_LOCATOR = lambda row: "xpath=//tr[@id=\'exceptions_row%s\']/td[3]/img" % (row,)

        # Open access policies pages and click on the mentioned policy to edit
        self._open_acc_pol_page()
        self._click_edit_policy_link(policy_name, self.ap_url_filtering_column)

        # Check if referrer content is enabled
        self._wait_until_element_is_present(ENABLE_REFERRER_CONTENT_LOCATOR)
        if self._is_checked(ENABLE_REFERRER_CONTENT_LOCATOR):
            # Check if all content to be deleted or specific row
            if content == 'all':
                self.click_element(ENABLE_REFERRER_CONTENT_LOCATOR)
            else:
                rows = content.split('#')
                for row in rows:
                    # Check if only one row is left to be deleted
                    existing_rows = self._find_elements(ROW_LOCATOR)
                    if len(existing_rows) == 1:
                        self.click_element(ENABLE_REFERRER_CONTENT_LOCATOR)
                    else:
                        self._wait_until_element_is_present(DELETE_ROW_LOCATOR(row))
                        self.click_element(DELETE_ROW_LOCATOR(row))

            # Click submit only if referrer content is disabled
            self._wait_until_element_is_present("xpath=//input[@value=\'Submit\'][2]")
            self.click_element("xpath=//input[@value=\'Submit\'][2]")

    def access_policies_enable_policy(self, name):
        """Enables existing policy

        Parameters:
            - `name` policy name to enable

        Examples:
            | Access Policies Enable Policy | myDefaultAccPol |
        """

        self._open_acc_pol_page()
        self._enable(name)

    def access_policies_disable_policy(self, name):
        """Disables existing policy

        Parameters:
            - `name` policy name to enable

        Examples:
            | Access Policies Disable Policy | myDefaultAccPol |
        """

        self._open_acc_pol_page()
        self._disable(name)

    def access_policies_is_enabled_policy(self, name):
        """Returns True if existing policy is enabled or False otherwise.

        Parameters:
            - `name` policy name to check

        Examples:
            | ${enabled}= | Access Policies Is Enabled Policy | myDefaultAccPol |
        """

        self._open_acc_pol_page()
        return self._is_enabled(name)
