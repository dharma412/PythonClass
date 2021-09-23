#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/heimdall.py#1 $

from common.util.utilcommon import UtilCommon


class Heimdall(UtilCommon):
    """Keywords to control and get status of process using
       /data/bin/heimdall_svc command.

       These are valid names of process that can be specified for `app_name`
       parameter below:
       | avc | coeuslogd | commandd | configdefragd |
       | counterd | external_auth_rpc_server | firestone | ftpd |
       | gathererd | ginetd | gui | haystackd |
       | heimdall | hermes | interface_controller | ipmitool |
       | local_authd | mcafee | merlin | musd |
       | pacd | prox | qlogd | reportd |
       | reportd_helper | reportqueryd | samld | shd |
       | sntpd | sophos | thirdparty | trafmon |
       | uds | updaterd | wbrsd |
    """

    def get_keyword_names(self):
        return [
            'heimdall_start',
            'heimdall_stop',
            'heimdall_restart',
            'heimdall_status',
        ]

    def heimdall_start(self, app_name=None, block=True):
        """Starts a process.

        Parameters:
           - `app_name`: name of process to start.
           - `block`: specify whether or not to make this a blocking call.
                      Either 'True' or 'False'.

        Examples:
        | Heimdall Start | app_name=uds |
        | Heimdall Start | app_name=uds |
        """
        self._shell.heimdall.start(app_name=app_name, block=block)

    def heimdall_stop(self, app_name=None, block=True):
        """Stops a process.

        Parameters:
           - `app_name`: name of process to stop.
           - `block`: specify whether or not to make this a blocking call.
                      Either 'True' or 'False'.

        Examples:
        | Heimdall Stop | app_name=uds |
        | Heimdall Stop | app_name=uds |
        """
        self._shell.heimdall.stop(app_name=app_name, block=block)

    def heimdall_restart(self, app_name=None, block=True):
        """Restarts a process.

        Parameters:
           - `app_name`: name of process to restart.
           - `block`: specify whether or not to make this a blocking call.
                      Either 'True' or 'False'.

        Examples:
        | Heimdall Restart | app_name=uds |
        | Heimdall Restart | app_name=uds |
        """
        self._shell.heimdall.restart(app_name=app_name, block=block)

    def heimdall_status(self, app_name=None, return_info='pid'):
        """Get status of a process.

        Parameters:
           - `app_name`: name of process to get status for.
           - `return_info`: a string of comma-separated value or a list of
                            the following status: 'enabled', 'ignore', 'pid',
                            'ready', or 'up'.  Defaulted to 'pid'. 

        Examples:
        | ${enabled} | Heimdall Status | app_name=uds | return_info=enabled |
        | ${ignore} | ${pid} | ${ready} | Heimdall Status |
        | | app_name=uds | return_info=ignore, pid, ready |
        | ${pid} | Heimdall Status | app_name=uds |
        """
        return_info = self._convert_to_tuple(return_info)
        return self._shell.heimdall.status(app_name=app_name,
                                           return_info=return_info)
