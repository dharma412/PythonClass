# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm75/cm75_onbox_dlp_policies.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus75.gui.manager.onbox_dlp_policies import OnboxDlpPolicies


class Cm75OnboxDlpPolicies(OnboxDlpPolicies):
    """
    Keywords for Web -> Configuration Master 7.5 -> Cisco Data Security
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 7.5', 'Cisco Data Security')

    def get_keyword_names(self):
        return [
            'cm75_onbox_dlp_policies_add',
            'cm75_onbox_dlp_policies_delete',
            'cm75_onbox_dlp_policies_edit',
            'cm75_onbox_dlp_policies_edit_url_categories',
            'cm75_onbox_dlp_policies_edit_content',
            'cm75_onbox_dlp_policies_edit_wbrs',
        ]

    def cm75_onbox_dlp_policies_add(self,
                                    name,
                                    description=None,
                                    order=None,
                                    identities='Global Identity Policy',
                                    protocols=None,
                                    proxy_ports=None,
                                    subnets=None,
                                    url_categories=None,
                                    user_agents=None,
                                    match_agents=True):
        """Add new IDS policy from Configuration Master 7.5

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
        | CM75 Onbox DLP Policies Add | three |
        | | description=Adding policy           |
        | | identities=Global Identity Policy   |
        | | protocols=http, ftpoverhttp         |
        | | proxy_ports=1234, 5321             |
        | | subnets=10.1.1.0/24, 1.2.3.44       |
        | | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | | user_agents=ie-all             |
        """
        self.onbox_dlp_policies_add(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm75_onbox_dlp_policies_delete(self, name):
        """Delete IDS policy from Configuration Master 7.5

        Parameters:

        - `name`: name of the policy to delete.

        Example:
        | CM75 Onbox DLP Policies Delete | three |
        """
        self.onbox_dlp_policies_delete(name)

    def cm75_onbox_dlp_policies_edit(self,
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
        """Edit IDS policy from Configuration Master 7.5

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
        | CM75 Onbox DLP Policies Edit | three |
        | | description=Adding policy          |
        | | identities=Global Identity Policy  |
        | | protocols=http, ftpoverhttp        |
        | | proxy_ports=80             |
        | | subnets=99.1.1.0/24             |
        | | url_categories=${webcats.CRIMINAL} |
        | | user_agents=ie-all             |
        """
        self.onbox_dlp_policies_edit(
            name,
            new_name=new_name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm75_onbox_dlp_policies_edit_url_categories(self,
                                                    name,
                                                    set_custom_all=None,
                                                    custom_url_categories=None,
                                                    set_predefined_all=None,
                                                    url_categories=None,
                                                    uncategorized_action=None):
        """Edit the IDS policy URL categories settings
         from Configuration Master 7.5

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

        Exceptions:
        - ValueError:action should be one of:['global', 'allow', 'monitor', 'block']
        - ValueError:action should be one of:['global', 'monitor', 'block']

        Example:
        | CM75 Onbox DLP Policies Edit URL Categories  | three |
        |   | url_categories=${webcats.CHAT}:block, ${webcats.ADULT}:block |
        |   | set_predefined_all=monitor   |
        |   | uncategorized_action=global  |
        | CM75 Onbox DLP Policies Edit URL Categories | three |
        |   | set_predefined_all=block   |
        |   | url_categories=${webcats.CHAT}:monitor, ${webcats.CHEAT}:monitor |
        |   | uncategorized_action=allow |
        """
        self.onbox_dlp_policies_edit_url_categories(
            name,
            set_custom_all=set_custom_all,
            custom_url_categories=custom_url_categories,
            set_predefined_all=set_predefined_all,
            url_categories=url_categories,
            uncategorized_action=uncategorized_action)

    def cm75_onbox_dlp_policies_edit_content(self,
                                             name,
                                             blocking_settings=None,
                                             http_file_size=None,
                                             ftp_file_size=None,
                                             block_types=None,
                                             mime_types=None,
                                             file_names=None,
                                             regexes=None,
                                             ):
        """Edit content setting for IDS policy from Configuration Master 7.5

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

        Exceptions:
        - ValueError:Invalid "xxx" object blocking settings
        - ValueError:Value 'xxx' should be 'no_limit' or <nnn> KB, MB, or GB
        - ValueError:Block 'xxx' should be 'off', 'all' or <nnn> KB or MB

        Example:
        | CM75 Onbox DLP Policies Edit Content    | three |
        | | blocking_settings=custom           |
        | | http_file_size=10 mb               |
        | | ftp_file_size=no_limit             |
        | | block_types=${filetypes.ARC_ARC}:all, ${filetypes.DOC_PDF}:10 mb |
        | | mime_types=audio/x-mpeg3, video/avi |
        | | file_names=document.doc,spreadsheet.xls |
        | | regexes=[Pp]orno, [Ss$]ex |

        See more examples in unit test
        """

        self.onbox_dlp_policies_edit_content(
            name,
            blocking_settings=blocking_settings,
            http_file_size=http_file_size,
            ftp_file_size=ftp_file_size,
            block_types=block_types,
            mime_types=mime_types,
            file_names=file_names,
            regexes=regexes,
        )

    def cm75_onbox_dlp_policies_edit_wbrs(self,
                                          name,
                                          settings_type=None,
                                          score=None,
                                          ):
        """Edit the WBRS for the IDS policy  from Configuration Master 7.5

        Parameters:

        - `name`: name of the policy to edit.

        - `settings_type`: 'global' 'custom' or 'disable'

        - `score`: The threshold in between block and monitor actions.
          Can be set only with settings_type=custom.
          Not implemented yet

        Exceptions:
        - ValueError:Invalid wbrs settings 'xxx' should be in ['global', 'custom', 'disable']
        - NotImplementedError

        Example:
        | CM75 Onbox DLP Policies Edit WBRS    | three |
        | | settings_type=custom  |

        """
        self.onbox_dlp_policies_edit_wbrs(
            name,
            settings_type=settings_type,
            score=score,
        )
