# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/update_config.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class UpdateConfig(CliKeywordBase):
    """Configure system update parameters."""

    def get_keyword_names(self):
        return ['update_config_setup',
                'update_config_dynamichost',
                'update_config_validate_certificates']


    def update_config_setup(self, *args):
        """Edit update configuration.

        updateconfig > setup

        *Parameters:*
        - `update_from`: update from either 'Use own' or 'Use cisco'
                server.
        - `update_server`: hostname and port of the HTTP server to download
                updates (images) from, using the format (local.server:port).
                The server name may be an IP address. The default port is 80.
        - `timezone_image_from`: update from either 'Use own' or 'Use cisco server.
        - `timezone_image_server`: hostname and port of the HTTP server tob download
                updates (images) from, using the format (local.server:port).
                The server name may be an IP address. The default port is 80.
        - `asyncos_image_from`: update from either 'Use own' or 'Use cisco server.
        - `asyncos_image_server`: hostname and port of the HTTP server tob download
                updates (images) from, using the format (local.server:port).
                The server name may be an IP address. The default port is 80.
        - `timezone_list_from`: update list from either 'Use own' or
                'Use ironport' server.
        - `timezone_list_server`: full HTTP URL of the update list using.
                The default HTTP port is 80. The optional username/password
                will be presented using HTTP BASIC_AUTH. Leave the entry blank
                to use the default server.
        - `asyncos_list_from`: update list from either 'Use own' or
                'Use ironport' server.
        - `asyncos_list_server`: full HTTP URL of the update list using.
                The default HTTP port is 80. The optional username/password
                will be presented using HTTP BASIC_AUTH. Leave the entry blank
                to use the default server.
        - `interval`: update interval. Use a trailing 'm' for minutes or 'h'
                for hours. Enter '0' to disable automatic updates.
        - `routing_table`: choose the routing table to use. Either 'Data' or
                'Management'.
        - `use_proxy`: setting up a proxy server for HTTP updates.
                Either Yes or No.
        - `proxy_server`: URL of the proxy server. The default port is 80.
                You can specify an optional authentication and port using
                the format: http://optionaluser:pass@proxy.server:80
        - `use_proxy_for_asyncos`: setting up a proxy server for HTTP updates.
                Either Yes or No.
        - `proxy_server_for_asyncos`: URL of the proxy server. The default port is 80.
                You can specify an optional authentication and port using
                the format: http://optionaluser:pass@proxy.server:80
        - `use_https_proxy`: setting up a HTTPS proxy server for HTTPS updates.
                Either Yes or No.
        - `https_proxy_server`: URL of the HTTPS proxy server. The default port
                is 443. You can specify an optional authentication and port
                using the format: https://optionaluser:pass@proxy.server:443

        *Examples:*
        | Update Config Setup |
        | ... | update_from=Use own |
        | ... | update_server=myserver.com:80 |
        | ... | timezone_image_from=Use own |
        | ... | timezone_image_server=myserver.com |
        | ... | asyncos_image_from=Use own |
        | ... | asyncos_image_server=myserver.com |
        | ... | timezone_list_from=Use own |
        | ... | timezone_list_server=http://list.com |
        | ... | asyncos_list_from=Use own |
        | ... | asyncos_list_server=http://list.com |
        | ... | interval=33m |
        | ... | routing_table=Management |
        | ... | use_proxy=YES |
        | ... | proxy_server=http://proxy.com |
        | ... | use_proxy_for_asyncos=YES |
        | ... | proxy_server_for_asyncos=http://proxy.com |
        | ... | use_https_proxy=YES |
        | ... | https_proxy_server=https://https_proxy.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.updateconfig().setup(**kwargs)

    def update_config_dynamichost(self, *args):
        """Edit dynamic host name.

        updateconfig > dynamichost

        Parameters:
        - `dynamic_host`: string with valid hostname:port value.

        Examples:
        | Update Config Dynamic Host | dynamic_host=test.com:443 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.updateconfig().dynamichost(**kwargs)

    def update_config_validate_certificates(self, *args):
        """Edit dynamic host name.

        updateconfig > dynamichost

        Parameters:
        - `dynamic_host`: string with valid hostname:port value.

        Examples:
        | Update Config Dynamic Host | dynamic_host=test.com:443 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.updateconfig().validate_certificates(**kwargs)

