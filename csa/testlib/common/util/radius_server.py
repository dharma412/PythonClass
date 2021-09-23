#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/radius_server.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon
from sal.servers.radius import FreeRadiusServer


class RadiusServer(UtilCommon):
    """Keywords for interacting with host running FreeRadius daemon.
    """
    SERVERS_CACHE = {}

    def get_keyword_names(self):
        return ['radius_server_start',
                'radius_server_stop',
                'radius_server_restart',
                'radius_server_is_running',

                'radius_server_is_config_valid',
                'radius_server_preserve_config',
                'radius_server_restore_config',
                'radius_server_set_config_file_content',
                'radius_server_get_config_file_content']

    def _get_server_obj(self, host):
        if not self.SERVERS_CACHE.has_key(host):
            self.SERVERS_CACHE[host] = FreeRadiusServer(host)
        return self.SERVERS_CACHE[host]

    def radius_server_start(self, host):
        """Start Radius daemon on particular FreeBSD host.
        Will be ignored if service is already running.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Exceptions:*
        - `ConfigError`: if current radius config is not correct
        and thus service can not be started
        - `RuntimeError`: if the service is not started after shell
        command is passed

        *Examples:*
        | Radius Server Start | sma19.sma |
        """
        self._get_server_obj(host).start()

    def radius_server_stop(self, host):
        """Stop Radius daemon on particular FreeBSD host.
        Will be ignored if service is already stopped

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Exceptions:*
        - `RuntimeError`: if the service is not stopped after shell
        command is passed

        *Examples:*
        | Radius Server Stop | sma19.sma |
        """
        self._get_server_obj(host).stop()

    def radius_server_restart(self, host):
        """Restart Radius daemon on particular FreeBSD host.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Exceptions:*
        - `ConfigError`: if current radius config is not correct
        and thus service can not be started
        - `RuntimeError`: if the service is not restarted after shell
        command is passed

        *Examples:*
        | Radius Server Restart | sma19.sma |
        """
        self._get_server_obj(host).restart()

    def radius_server_is_running(self, host):
        """Return run status of Radius daemon on particular FreeBSD host.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Return:*
        Either ${True} or ${False}

        *Examples:*
        | ${status}= | Radius Server Is Running | sma19.sma |
        """
        return self._get_server_obj(host).is_running()

    def radius_server_is_config_valid(self, host):
        """Return status of Radius daemon config on particular FreeBSD host.
        In case current config is not valid then Start/Restart keywords
        with fail with ConfigError exception on this machine.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Return:*
        Either ${True} or ${False}

        *Examples:*
        | ${status}= | Radius Server Is Config Valid | sma19.sma |
        """
        return self._get_server_obj(host).is_config_valid()

    def radius_server_preserve_config(self, host):
        """Preserve Radius daemon config on particular FreeBSD host.
        Thus, the whole content of /usr/local/etc/raddb folder
        (including subfolders) is gzipped and saved to file in
        temporary dir on remote host.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine

        *Return:*
        Full path to the saved config archive on the remote machine

        *Examples:*
        | ${archive_path}= | Radius Server Preserve Config | sma19.sma |
        """
        return self._get_server_obj(host).preserve_settings()

    def radius_server_restore_config(self, host, archive_path,
                                     should_clean_archived_settings=True):
        """Restore Radius daemon config on particular FreeBSD host.
        Thus, the whole content of /usr/local/etc/raddb folder
        (including subfolders) is restored.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine
        - `archive_path`: valid path to gzipped archive on remote
        host returned by *Radius Server Preserve Config* keyword
        - `should_clean_archived_settings`: whether to delete
        `archive_path` after Radius config was successfully restored

        *Exceptions:*
        - `ConfigError`: if Radius service has failed to start because
        of broken config

        *Examples:*
        | ${archive_path}= | Radius Server Preserve Config | sma19.sma |
        | Radius Server Restore Config | sma19.sma |
        | ... | ${archive_path} | ${False} |
        """
        self._get_server_obj(host).restore_settings(archive_path,
                                                    should_clean_archived_settings)

    def radius_server_set_config_file_content(self, host, file_name,
                                              new_content):
        """Set Radius daemon config file content on particular FreeBSD host.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine
        - `file_name`: relative config file name. Root folder is
        /usr/local/etc/raddb/
        - `new_content`: string containing new content have to be
        written into `file_name` config file

        *Exceptions:*
        - `ConfigError`: if Radius service has failed to start because
        of broken config

        *Examples:*
        | ${new_content}= | Set Variable | blabla |
        | Radius Server Set Config File Content | sma19.sma | users |
        | ... | ${new_content} |
        """
        self._get_server_obj(host).set_config(file_name, new_content)

    def radius_server_get_config_file_content(self, host, file_name):
        """Get Radius daemon config file content on particular FreeBSD host.

        *Parameters:*
        - `host`: valid hostname or IP address of FreeBSD machine
        - `file_name`: relative config file name. Root folder is
        /usr/local/etc/raddb/

        *Return:*
        String, content of particular config file

        *Examples:*
        | ${content}= | Radius Server Get Config File Content |
        | ... | sma19.sma | users |
        """
        return self._get_server_obj(host).get_config(file_name)
