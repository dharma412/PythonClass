# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm118/cm118_bypass_settings.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm118/cm118_bypass_settings.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from coeus1180.gui.manager.bypass_settings import BypassSettings

class Cm110BypassSettings(BypassSettings):

    """
    Keywords library for WebUI page Web -> Configuration Master 11.8 -> Bypass Settings
    """

    def _open_proxy_bypass_page(self):
        self._navigate_to('Web', 'Configuration Master 11.8', 'Bypass Settings')

    def get_keyword_names(self):
        return ['cm118_bypass_settings_edit',
                'cm118_bypass_settings_application_edit',
                'cm118_bypass_settings_get_settings',
             ]

    def cm118_bypass_settings_get_settings(self):
        """Get proxy bypass settings from Configuration Master 11.8

        Parameters: None

        Example of usage:
        | ${settings}= | CM118 Bypass Settings Get Settings |
        | Log | ${settings} |
        | Should Contain | ${settings}['proxy'] | 10.0.0.1 |
        """

        return self.proxy_bypass_get_settings()

    def cm118_bypass_settings_edit(self, bypass_list):
        """Edit the proxy bypass list from Configuration Master 11.8

        :Parameters:
        - `bypass_list`: a comma separated values of domains/subnets
                         being bypassed.

        Exceptions:
        - ValueError:bypass_list should be either tuple or list of strings
        - GuiFeatureDisabledError:Proxy must be in transparent mode in order to use proxy bypass feature.

        Example:
        | CM118 Bypass Settings Edit | 10.7.11.48/24,example.com |
        | CM118 Bypass Settings Edit | crm.example.com |
        """

        self.proxy_bypass_edit(bypass_list)

    def cm118_bypass_settings_application_edit(self, apps_bypass):
        """Edit application scanning bypass settings from Configuration Master 11.8

        :Parameters:
        - `apps_bypass`: a comma separated values of application
                         names and boolean values separated by ':'. Values are
                         boolean variables which enables or disables bypass
                         scanning for the application to bypass. Example:
                         'Webex:True, Apps:False, Mcaff:True'

        Exceptions:
        - ValueError:"xxx" application does not exist

        Examples:
        | CM118 Bypass Settings Application Edit | Webex:True |
        | CM118 Bypass Settings Application Edit | Webex:False |
        """
        self.proxy_bypass_application_edit(apps_bypass)
