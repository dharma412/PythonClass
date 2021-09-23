#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/heimdal.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit
from time import sleep

import sal
from SSHLibrary import SSHLibrary

from credentials import RTESTUSER, RTESTUSER_PASSWORD

DEFAULT_TIMEOUT = 60


class Heimdal(object):
    """Methods for interacting with appliance's heimdal manager.
    """

    SHELL_CONNECTIONS_POOL = {}

    def __init__(self, hostname):
        self._hostname = hostname

    def _get_shell_object(self):
        shell = SSHLibrary()
        shell.open_connection(host=self._hostname, timeout=60)
        shell.login(RTESTUSER, RTESTUSER_PASSWORD)
        return shell

    @property
    def shell(self):
        if self.SHELL_CONNECTIONS_POOL.has_key(self._hostname):
            # check whether SSH connection is still alive
            try:
                self.SHELL_CONNECTIONS_POOL[self._hostname].execute_command('uname')
            except:
                self.SHELL_CONNECTIONS_POOL[self._hostname] = self._get_shell_object()
        else:
            self.SHELL_CONNECTIONS_POOL[self._hostname] = self._get_shell_object()
        return self.SHELL_CONNECTIONS_POOL[self._hostname]

    def _calc_service_state(self, state_dict):
        return state_dict[0]['up'] \
               and state_dict[0]['ready'] \
               and state_dict[0]['enabled']

    def get_services_status(self, services_list=[]):
        """Get internal status of all appliance services

        *Parameters:*
        - `services_list`: list of service name whose status should
        be returned. Can be an empty list in order to get all available services
        status

        *Exceptions:*
        - `ValueError`: if there is no service(s) with given name on
        appliance

        *Return:*
        Dictionary returned by by
        `/data/bin/heimdall_svc status_extended`
        command on appliance.
        Dictionary keys are service names and values are 1-element lists.
        This element is dictionary whose structure looks like:
        {'enabled': True, 'ignore': False, 'pid': 1398, 'ready': True, 'up': True}
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
        str_output = self.shell.execute_command(
            '/data/bin/heimdall_svc status_extended')
        services_status = eval(str_output)
        if len(services_list) > 0:
            available_services = services_status.keys()
            if not set(services_list).issubset(set(available_services)):
                raise ValueError('Service names should be taken from %s' \
                                 ' but %s is given' % (available_services,
                                                       services_list))
            result = {}
            for service_name, status_dict in services_status.iteritems():
                if service_name in services_list:
                    result[service_name] = status_dict
            return result
        else:
            return services_status

    def wait_for_services(self, services_list, should_be_enabled=True,
                          timeout=DEFAULT_TIMEOUT):
        """Wait for group of services within the given timeout

        *Parameters:*
        - `services_list`: list of service names that should be monitored
        - `should_be_enabled`: whether to wait until all given services are enabled
        (True) or disabled (False). True by default
        - `timeout`: number of seconds to wait for the service. 60 seconds by
        default

        *Exceptions:*
        - `AssertionError`: if services were not enabled/disabled within the given
        timeout
        """
        if isinstance(services_list, basestring):
            services_list = [services_list]
        expected_action = 'enabled' if should_be_enabled else 'disabled'
        tmr = sal.time.CountDownTimer(int(timeout)).start()
        while tmr.is_active():
            current_statuses = map(lambda x: self._calc_service_state(x),
                                   self.get_services_status(services_list).itervalues())
            if should_be_enabled and all(current_statuses):
                print 'The service(s) %s have been successfully %s' % \
                      (services_list, expected_action)
                return
            if not (should_be_enabled or any(current_statuses)):
                print 'The service(s) %s have been successfully %s' % \
                      (services_list, expected_action)
                return
            sleep(1)
        else:
            raise AssertionError('The service(s) "%s" are not %s within' \
                                 ' the %s seconds timeout' % (services_list,
                                                              expected_action, timeout))


def close_all_opened_cli_connections():
    for shell in Heimdal.SHELL_CONNECTIONS_POOL.itervalues():
        try:
            shell.close_connection()
        except Exception as e:
            print e


atexit.register(close_all_opened_cli_connections)
