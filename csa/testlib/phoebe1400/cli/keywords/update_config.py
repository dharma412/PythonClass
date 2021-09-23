# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/update_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class UpdateConfig(CliKeywordBase):
    """Configure system update parameters."""

    def get_keyword_names(self):
        return ['update_config_setup',
                'update_config_dynamichost',
                'update_config_validate_certificates']

    def update_config_setup(self, *args):
        """Edit update configuration.

        Parameters:
        - `update_from`: update from either 'Use own' or 'Use cisco' server.
        - `update_server`: base url where the system will download updates from.
            The format is: http://optionalname:password@local.server:port/directory/
            The default HTTP port is 80;
            The optional username/password will be presented using HTTP BASIC_AUTH.
        - `update_images_from`: download images from either 'Use own' or 'Use cisco' server.
        - `update_images_server`: the hostname and port of the HTTP server;
            The format is local.server:port.
            The server name may be an IP address. The default port is 80.
        - `update_upgrade_images_from`: download the system updates from either 'Use own' or 'Use cisco' server.
        - `update_upgrade_images_server`: the hostname and port of the HTTP server;
            The format is local.server:port.
            The server name may be an IP address. The default port is 80.
        - `update_ims_and_cloudmark_from`: update from either 'Use own' or 'Use cisco' server.
            (present if relevant feature key installed)
        - `update_ims_and_cloudmark_server`: the hostname and port of the update server.
            (present if relevant feature key installed)
        - `update_list_from`: update list from either 'Use own' or 'Use ironport' server.
        - `update_list_server`: full HTTP URL of the update list.
            The default HTTP port is 80.
            The optional username/password will be presented using HTTP BASIC_AUTH.
            eg, http://optionalname:password@local.server:port/directory/manifest.xml
            Leave the entry blank to use the default server.
        - `update_upgrade_list_from`: update from either 'Use own' or 'Use cisco' server.
        `update_upgrade_list_server`: full HTTP URL of the update list.
            The default HTTP port is 80. The optional username/password
            will be presented using HTTP BASIC_AUTH. Leave the entry blank
            to use the default server.
        - `interval`: set time interval.
            Use a trailing 's' for seconds, 'm' for minutes or 'h' for hours.
            The minimum valid update time is 30s or enter '0' to disable automatic updates.
        - `interface`: choose the interface to use for initiating a connection to the update server.
        - `use_proxy`: setting up a proxy server for HTTP updates. Either Yes or No.
        - `proxy_server`: URL of the proxy server. The default port is 80.
            You can specify an optional authentication and port using
            the format: http://optionaluser:pass@proxy.server:80
        - `use_https_proxy`: setting up a HTTPS proxy server for HTTPS updates.
            Either Yes or No.
        - `https_proxy_server`: URL of the HTTPS proxy server. The default port
            is 443. You can specify an optional authentication and port
            using the format: https://optionaluser:pass@proxy.server:443

        Examples:
        | Update Config Setup |
        | ... | update_from=Use own |
        | ... | update_server=http://optionalname:password@update.server.qa:1111/updates_dir/ |
        | ... | update_images_from=Use own |
        | ... | update_images_server=images.server.qa:2222 |
        | ... | update_upgrade_images_from=Use own |
        | ... | update_upgrade_images_server=upgrade.images.server.qa:4444 |
        | ... | update_ims_and_cloudmark_from=Use own |
        | ... | update_ims_and_cloudmark_server=ims.cloud.update.server.qa |
        | ... | update_list_from=Use own |
        | ... | update_list_server=http://update.list.com |
        | ... | update_upgrade_list_from=Use own |
        | ... | update_upgrade_list_server=http://upgrade.list.qa:3333 |
        | ... | interval=45s |
        | ... | interface=Management |
        | ... | use_proxy=YES |
        | ... | proxy_server=http://proxy.com |
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
        - `confirm_switch_to_cluster`: whether to force switch from cluster to machine mode.
        Either 'Yes' or 'No'. 'Yes' by default.
        - `choose_a_machine`: choose a machine to enter dynamichost value in cluster mode.

        Examples:
        | Update Config Dynamic Host | dynamic_host=test.com:443 |
        | ... | confirm_switch_to_cluster=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.updateconfig().dynamichost(**kwargs)


    def update_config_validate_certificates(self, *args):
        """Enter YES or NO for Validating Servers Certificates.
        updateconfig > VALIDATE_CERTIFICATES

        Parameters:
        - `validate_certificates=YES or NO.
        - `confirm_switch_to_cluster`: whether to force switch from cluster to machine mode.
        Either 'Yes' or 'No'. 'Yes' by default.

        Examples:
        | Update Config Validate Certificates | validate_certificates=NO |
        | ... | confirm_switch_to_cluster=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.updateconfig().validate_certificates(**kwargs)
