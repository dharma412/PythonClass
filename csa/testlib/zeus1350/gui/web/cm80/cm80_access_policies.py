# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm80/cm80_access_policies.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from coeus80.gui.manager.access_policies import AccessPolicies


class Cm80AccessPolicies(AccessPolicies):
    """
    Keywords for Web -> Configuration Master 8.0 -> Access Policies
    """

    def _open_acc_pol_page(self):
        """Go to Access Policies configuration page."""

        self._navigate_to('Web', 'Configuration Master 8.0', 'Access Policies')

    def get_keyword_names(self):
        return ['cm80_access_policies_add',
                'cm80_access_policies_edit',
                'cm80_access_policies_delete',
                'cm80_access_policies_edit_protocols_and_user_agents',
                'cm80_access_policies_edit_objects',
                'cm80_access_policies_edit_url_categories',
                'cm80_access_policies_edit_applications',
                'cm80_access_policies_edit_wbrs_and_ams_settings',
                'cm80_access_policies_edit_content_filtering_settings',
                'cm80_access_policies_disable_policy',
                'cm80_access_policies_enable_policy',
                'cm80_access_policies_is_enabled_policy',
                'cm80_access_policies_get_list',
                ]

    def cm80_access_policies_get_list(self):
        """
        Returns: dictionary of access_policies from Configuration Master
        Keys are names of policies.
        Each policy is a dictionary with following keys:
        - `order`
        - `identity`
        - `protocols_and_user_agents`
        - `url_filtering`
        - `applications`
        - `objects`
        - `web_reputation_and_anti-malware_filtering`

        Examples:
        | ${policies}= | CM80 Access Policies Get List |
        | ${policies}= | Access Policies Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['policy']['applications'] == '(global policy)' |
        """
        return self.access_policies_get_list()

    def cm80_access_policies_add(self,
                                 name,
                                 description=None,
                                 order=None,
                                 identity='Global Identity Policy',
                                 protocols=None,
                                 proxy_ports=None,
                                 subnets=None,
                                 time_range=None,
                                 match_range=None,
                                 url_categories=None,
                                 user_agents=None,
                                 common_user_agents=None,
                                 match_agents=None):
        """Adds new access policy from Configuration Master 8.0

        Parameters:
        - `name`: name of access policy.
        - `description`: description for access policy.
        - `order`: order of access policy.
        - `identity`: identity associated with this access policy.
        Defaulted to Global Identity Policy. Document that describes identities
        specification.
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
        | CM80 Access Policies Add | myDefaultAccPol |
        | ... | description=This policy uses Global Identity Policy |


        | CM80 Access Policies Add | myOtherAccPol |
        | ... | description=This policy uses custom identity |
        | ... | identity=myID |

        | CM80 Access Policies Add | myNewPolicy |
        | ... | description=Test access policy |
        | ... | identity=Global Identity Policy |
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
        self.access_policies_add(
            name,
            description=description,
            order=order,
            identity=identity,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm80_access_policies_edit(self,
                                  name,
                                  description=None,
                                  order=None,
                                  identity='Global Identity Policy',
                                  protocols=None,
                                  proxy_ports=None,
                                  subnets=None,
                                  time_range=None,
                                  match_range=None,
                                  url_categories=None,
                                  user_agents=None,
                                  common_user_agents=None,
                                  match_agents=True):
        """Edits specified access policy from Configuration Master 8.0

        Parameters:
        - `name`: name of access policy to be edited.
        - `description`: description for access policy.
        - `order`: order of access policy.
        - `identity`: identity associated with this access policy.
        Defaulted to Global Identity Policy. Document that describes identities
        specification.
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

        Example:
        | CM80 Access Policies Edit | myNewTestPolicy |
        | ... | description=Edited by unittest |
        | ... | order=2 |
        | ... | identity=Global Identity Policy |
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
        self.access_policies_edit(
            name,
            description=description,
            order=order,
            identity=identity,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_range,
            url_categories=url_categories,
            user_agents=user_agents,
            common_user_agents=common_user_agents,
            match_agents=match_agents)

    def cm80_access_policies_delete(self, name):
        """Deletes specified access policy from Configuration Master 8.0

        `name`: name of access policy to be deleted.

        Example:
        | CM80 Access Policy Delete | myAccPol |
        """
        self.access_policies_delete(name)

    def cm80_access_policies_edit_protocols_and_user_agents(self,
                                                            name,
                                                            setting_type='custom',
                                                            block_protocols=None,
                                                            connect_ports=None,
                                                            block_user_agents=None):
        """Sets protocol blocking from Configuration Master 8.0

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

        | CM80 Access Policies Edit Protocols And User Agents | myAccPol |
        | ... | block_protocols=allow all |
        | ... | connect_ports=8080, 21, 443, 563, 8443, 20, 1-15 |
        | ... | block_user_agents=${user_agents} |
        """
        self.access_policies_edit_protocols_and_user_agents(
            name,
            setting_type=setting_type,
            block_protocols=block_protocols,
            connect_ports=connect_ports,
            block_user_agents=block_user_agents)

    def cm80_access_policies_edit_objects(self,
                                          name,
                                          setting_type='global',
                                          http_size=None,
                                          ftp_size=None,
                                          file_types=None,
                                          custom_mime_types=None):
        """Edit specified Access Policy object settings
         from Configuration Master 8.0

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

        | CM80 Access Policies Edit Objects | myTestPolicy |
        | ... | setting_type=custom |
        | ... | http_size=1024 |
        | ... | ftp_size=1024 |
        | ... | file_types=${filetypes_list} |
        | ... | custom_mime_types=${mime_types_list} |
        """
        self.access_policies_edit_objects(
            name,
            setting_type=setting_type,
            http_size=http_size,
            ftp_size=ftp_size,
            file_types=file_types,
            custom_mime_types=custom_mime_types)

    def cm80_access_policies_edit_content_filtering_settings(self,
                                                             name,
                                                             setting_type='custom',
                                                             safe_search_option=None,
                                                             unsupported_option=None,
                                                             content_rating=None,
                                                             content_action=None
                                                             ):
        """Edit specified Access Policies Content Filtering Settings
         from Configuration Master 8.0

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

        | CM80 Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=global |

        | CM80 Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=custom |
        | ... | safe_search_option=enable |
        | ... | unsupported_option=allow |
        | ... | content_rating=enable |
        | ... | content_action=block |

        | CM80 Access Policies Edit Content Filtering Settings | ${pol} |
        | ... | setting_type=custom |
        | ... | safe_search_option=disable |
        | ... | content_rating=disable |
        """
        self.access_policies_edit_content_filtering_settings(
            name,
            setting_type=setting_type,
            safe_search_option=safe_search_option,
            unsupported_option=unsupported_option,
            content_rating=content_rating,
            content_action=content_action
        )

    def cm80_access_policies_edit_wbrs_and_ams_settings(self,
                                                        name,
                                                        setting_type='custom',
                                                        wbrs_setting=None,
                                                        sua_setting=None,
                                                        sua_action=None,
                                                        webroot=None,
                                                        av=None,
                                                        ams_setting=None,
                                                        amw_categories=None,
                                                        custom_block_boundary=None,
                                                        custom_allow_boundary=None):
        """Edit specified Access Policies: Web Reputation and Anti-Malware
        Settings from Configuration Master 8.0

        This keyword allows to set:
        - `WBRS settings`,
        - `Suspect User Agent Scanning settings`,
        - `Anti-Malware Scanning (Webroot, McAfee, and Sophos)`

        Parameters:
        - `name`: name of the access policy to edit.
        - `setting_type`: setting type to use.  Either 'custom' or 'global'.
        - `wbrs_setting`: either 'enable' or 'disable'. Web reputation feature
        setting.
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

        | CM80 Access Policies Edit WBRS And AMS Settings | ${pol} |
        | ... | setting_type=global |

        | CM80 Access Policies Edit WBRS And AMS Settings | ${pol} |
        | ... | wbrs_setting=enable |
        | ... | sua_setting=enable |
        | ... | sua_action=block |
        | ... | ams_setting=enable |
        | ... | amw_categories=${ams_cats} |

        | CM80 Access Policies Edit Wbrs And Ams Settings | ${pol} |
        | ... | webroot=enable |
        | ... | av=sophos |

        | CM80 Access Policies Edit Wbrs And Ams Settings | ${pol} |
        | ... | wbrs_setting=enable |
        | ... | custom_block_boundary=-8 |
        | ... | custom_allow_boundary=8.0 |
        """
        self.access_policies_edit_wbrs_and_ams_settings(
            name,
            setting_type=setting_type,
            wbrs_setting=wbrs_setting,
            sua_setting=sua_setting,
            sua_action=sua_action,
            webroot=webroot,
            av=av,
            ams_setting=ams_setting,
            amw_categories=amw_categories,
            custom_block_boundary=custom_block_boundary,
            custom_allow_boundary=custom_block_boundary)

    def cm80_access_policies_edit_applications(self,
                                               name,
                                               defaults=None,
                                               actions=None,
                                               settings_type='custom'):
        """Setups applications setting for the certain access policy
         from Configuration Master 8.0

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

        | CM80 Access Policies Edit Applications | Global Policy |
        | ... | defaults=${defs} |
        | ... | actions=${apps} |

        | CM80 Access Policies Edit Applications | test |
        | ... | actions=${apps1} |
        """
        self.access_policies_edit_applications(
            name,
            defaults=defaults,
            actions=actions,
            settings_type=settings_type)

    def cm80_access_policies_edit_url_categories(self,
                                                 name,
                                                 url_categories=None,
                                                 uncategorized_action=None
                                                 ):
        """Edit specified access policy URL categories settings
         from Configuration Master 8.0

        Parameters:
        - `name`: name of the policy to edit.

        - `url_categories`:  a string of comma separated items or a list of
        items. Each item is string with values separated by colon.
        | First value is url category object,
        | second value is action

        | (Available actions for predefined url categories:
        | 'global', 'block', 'monitor', 'warn', 'timebased'.
        | Available actions for custom url categories:
        | 'block', 'redirect', 'allow', 'warn', 'monitor', 'timebased').

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

        | CM80 Access Policies Edit Url Categories | myNewTestPolicy |
        | ... | ${url_cats} |
        | ... | block |

        | @{url_cats}= | Set Variable |
        | ... | testCustomUrlCat1:timebased:testCustomTR1:redirect-http://yandex.ru:redirect-http://google.com |
        | ... | ${webcats.COMPUTER_SEC}:timebased:testCustomTR2:monitor:block |

        | CM80 Access Policies Edit Url Categories | testPolicyWithTimebasedCategories |
        | ... | ${url_cats} |

        | CM80 Access Policies Edit Url Categories | testPolicyWithRedirectCategories |
        | ... | testCustomUrlCat1:redirect:http://yandex.ru, testCustomUrlCat2:redirect:http://google.com |
        """
        self.access_policies_edit_url_categories(
            name,
            url_categories=url_categories,
            uncategorized_action=uncategorized_action
        )

    def cm80_access_policies_enable_policy(self, name):
        """Enables existing policy from Configuration Master 8.0

        Parameters:
            - `name` policy name to enable

        Examples:
            | CM80 Access Policies Enable Policy | myDefaultAccPol |
        """
        self.access_policies_enable_policy(name)

    def cm80_access_policies_disable_policy(self, name):
        """Disables existing policy from Configuration Master 8.0

        Parameters:
            - `name` policy name to enable

        Examples:
            | CM80 Access Policies Disable Policy | myDefaultAccPol |
        """
        self.access_policies_disable_policy(name)

    def cm80_access_policies_is_enabled_policy(self, name):
        """Returns True if existing policy is enabled or False otherwise
         from Configuration Master 8.0

        Parameters:
            - `name` policy name to check

        Examples:
            | ${enabled}= | CM80 Access Policies Is Enabled Policy | myDefaultAccPol |
        """
        return self.access_policies_is_enabled_policy(name)
