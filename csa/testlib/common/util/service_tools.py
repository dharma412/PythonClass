#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/service_tools.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon
from sal.clients.heimdal import Heimdal, DEFAULT_TIMEOUT


class ServiceTools(UtilCommon):
    """Keywords for interacting with appliance services.
    List of available service names highly depends on appliance type and version.
    For example, on ESA version 7.6 this list contains the next items:
    | dlp_rsa_interop |
    | cloudmark |
    | ftpd |
    | qlogd |
    | local_authd |
    | smad |
    | interface_controller |
    | snmpd |
    | euq_webui |
    | top |
    | slbld |
    | ldap |
    | unrard |
    | conduit |
    | postgres |
    | sshtunnel |
    | case |
    | postx |
    | sntpd |
    | gui |
    | dlp_rsa |
    | trackerd |
    | reportqueryd |
    | brightmail |
    | ldap_rpc_server |
    | repeng |
    | external_auth_rpc_server |
    | thirdparty |
    | raid |
    | reportd_helper |
    | splunkd |
    | euq_server |
    | image_analysis |
    | updaterd |
    | stellent |
    | hermes |
    | ginetd |
    | ipmitool |
    | mcafee |
    | sophos |
    | passthroughd |
    | slbl_db_server |
    | commandd |
    | reportd |
    """

    def get_keyword_names(self):
        return ['wait_for_appliance_services']

    def wait_for_appliance_services(self, host, services_list,
                                    should_be_enabled=True,
                                    timeout=DEFAULT_TIMEOUT):
        """Wait for group of services within the given timeout

        *Parameters:*
        - `host`: destination appliance hostname or IP address
        - `services_list`: list of service names that should be monitored
        or simply service name string if we have to monitor only one service
        - `should_be_enabled`: whether to wait until all given services are enabled
        (True) or disabled (False). True by default
        - `timeout`: number of seconds to wait for the service. 60 seconds by
        default

        *Exceptions:*
        - `AssertionError`: if services were not enabled/disabled within the given
        timeout
        """
        Heimdal(host).wait_for_services(services_list,
                                        should_be_enabled, timeout)
