#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/ssc_config.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class SSCConfig(CliKeywordBase):
    """Keywords for sscconfig CLI command."""

    def get_keyword_names(self):
        return ['ssc_config_enable',
                'ssc_config_disable',
                'ssc_config_onbox',
                'ssc_config_offbox',
                'ssc_config_list',
                'ssc_config_show', ]

    def ssc_config_enable(self, service_name, interface_name, port=8003):
        """Enable a service on Security Services Cluster. Available only on SSC.

        Parameters:
        - `service_name`: Name of the scanning engine/service.
        - `interface_name`: Name of the interface on which service should run.
        - `port`: Port on which service should run. Default is 8003.

        Examples:
        | SSC Config Enable | sophos | 10.76.68.138 | 8111 |
        | SSC Config Enable | case | 10.76.68.138 |
        """
        self._cli.sscconfig().enable(
            service_name=service_name,
            interface_name=interface_name,
            port=port)

    def ssc_config_disable(self, service_name):
        """Disable a service on Security Services Cluster. Available only on SSC.

        Parameters:
        - `service_name`: Name of the scanning engine/service.

        Examples:
        | SSC Config Disable | sophos |
        """
        self._cli.sscconfig().disable(service_name)

    def ssc_config_onbox(self, service_name):
        """Enable scanning service(onbox) on MG. Available only for MG.

        Parameters:
        - `service_name`: Name of the scanning engine/service.

        Examples:
        | SSC Config Onbox | sophos |
        """
        self._cli.sscconfig().onbox(service_name)

    def ssc_config_offbox(self, service_name, service_address, port=8003):
        """Enable scanning service(offbox). Availble only on MG.

        Parameters:
        - `service_name`: Name of the scanning engine/service.
        - `service_address`: Remote IP address of the service.
        - `port`: Port on which service will be running. Default is 8003.

        Examples:
        | SSC Config Offbox | sophos | 10.76.68.138 | 8111 |
        | SSC Config Offbox | case | 10.76.68.138 |
        """
        self._cli.sscconfig().offbox(
            service_name=service_name,
            service_address=service_address,
            port=port)

    def ssc_config_list(self):
        """Returns a list of services that can run as a Security Service Cluster.

        Examples:
        | ${services} = | SSC Config List |
        | Log | ${services} |
        """
        return self._cli.sscconfig().list()

    def ssc_config_show(self, *args):
        """Returns a dictionary containing Status of Security Services Clusters.

        Parameters:
        - `as_dictionary`: Format result as dictionary. YES or NO.

        Return:
        Dictionary or String(raw output).
        Dictionary:
        | Dictionary | Keys |
        | service | Location |
        |         | Service Address |

        Examples:
        | ${ssc_status} = | SSC Config Show |
        | ${ssc_status} = | SSC Config Show | as_dictionary=yes |
        | Log Dictionary | ${ssc_status} |
        | ${service} | Get From Dictionary | ${ssc_status} | sophos |
        | Log | ${service} |
        | ${service_location} | Get From Dictionary | ${service} | Location |
        | Log | ${service_location} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.sscconfig().show(**kwargs)
