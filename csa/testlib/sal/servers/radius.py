#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/servers/radius.py#2 $ $DateTime: 2019/06/11 06:52:26 $ $Author: revlaksh $

import atexit
import codecs
from datetime import datetime
import os
import re
import tempfile
import time

from SSHLibrary import SSHLibrary

from sal.exceptions import ConfigError


def del_tree(dir_path):
    if not os.path.isdir(dir_path):
        return
    for filename in os.listdir(dir_path):
        item_path = os.path.join(dir_path, filename)
        if os.path.isdir(item_path):
            del_tree(item_path)
        else:
            os.unlink(item_path)
    os.rmdir(dir_path)


class BaseRadiusServer(object):
    def __init__(self, hostname):
        self._hostname = hostname

    @property
    def hostname(self):
        return self._hostname

    def start(self, should_verify_config=True):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def stop(self):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def restart(self):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def is_running(self):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def preserve_settings(self):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def restore_settings(self, saved_config_path, should_clean_archived_settings=True):
        raise NotImplementedError('Virtual method. Define in derived class.')

    def _write_log(self, log_str):
        print '%s :: %s' % (time.asctime(), log_str)


class FreeRadiusServer(BaseRadiusServer):
    DAEMON_DIR = '/usr/local/etc/rc.d'
    CONF_DIR = '/usr/local/etc/raddb'
    DAEMON_NAME = 'radiusd'
    SERVICE_NAME = 'freeradius'
    DAEMON_NAME_PRINTABLE = 'RADIUS Daemon'
    RC_CMD = 'sudo %s' % (os.path.join(DAEMON_DIR, DAEMON_NAME),)
    USER = 'testuser'
    PASSWORD = 'ironport'

    SHELL_CONNECTIONS_POOL = {}

    @property
    def shell(self):
        if not self.SHELL_CONNECTIONS_POOL.has_key(self._hostname):
            shell = SSHLibrary()
            shell.open_connection(host=self._hostname,
                                  timeout=5 * 60,
                                  prompt='$')
            fp, logfile_path = tempfile.mkstemp('.log', 'radiusserver')
            self._write_log('%s shell debug log path: %s' % (self.DAEMON_NAME_PRINTABLE,
                                                             logfile_path))
            shell.enable_ssh_logging(logfile_path)
            shell.login(self.USER, self.PASSWORD)
            self.SHELL_CONNECTIONS_POOL[self._hostname] = shell
        return self.SHELL_CONNECTIONS_POOL[self._hostname]

    def __init__(self, hostname):
        super(FreeRadiusServer, self).__init__(hostname)

    def start(self, should_verify_config=True):
        if self.is_running():
            # don't start again if we're already running
            return
        if should_verify_config and not self.is_config_valid():
            raise ConfigError('%s could not be started on host %s. Please fix its ' \
                              'settings and try again. See debug log for more details.' % \
                              (self.DAEMON_NAME_PRINTABLE, self._hostname))
        self._write_log('Starting %s..' % (self.DAEMON_NAME_PRINTABLE,))
        status = self.shell.execute_command('%s start' % (self.RC_CMD,))
        # To be sure all processes are started
        time.sleep(1.0)
        self._write_log('Start status: %s' % (status,))
        if not self.is_running():
            raise RuntimeError('%s has failed to start on host %s' % \
                               (self.DAEMON_NAME_PRINTABLE, self._hostname))
        else:
            self._write_log('%s start status: OK' % (self.DAEMON_NAME_PRINTABLE,))

    def stop(self):
        if not self.is_running():
            # don't stop if we're already stopped
            return
        self._write_log('Stopping %s...' % (self.DAEMON_NAME_PRINTABLE,))
        cmd_ps = 'ps axww | grep %s | grep -v grep' % (self.DAEMON_NAME,)
        cmd_ps_out = self.shell.execute_command(cmd_ps)
        if cmd_ps_out:
            for line in cmd_ps_out.splitlines():
                pid_match = re.search(r'([0-9]+)', line)
                if pid_match:
                    self.shell.execute_command('sudo kill -9 %s' % (pid_match.group(0),))
        if self.is_running():
            raise RuntimeError('%s has failed to stop on host %s' % \
                               (self.DAEMON_NAME_PRINTABLE, self._hostname))
        else:
            self._write_log('%s stop status: OK' % (self.DAEMON_NAME_PRINTABLE,))

    def restart(self):
        self._write_log('Restarting %s...' % (self.DAEMON_NAME_PRINTABLE,))
        status = self.shell.execute_command('%s restart' % (self.RC_CMD,))
        # To be sure all processes are restarted
        time.sleep(1.0)
        if not self.is_running():
            raise RuntimeError('%s has failed to restart on host %s' % \
                               (self.DAEMON_NAME_PRINTABLE, self._hostname))
        else:
            self._write_log('%s restart status: OK' % (self.DAEMON_NAME_PRINTABLE,))

    def is_running(self):
        cmd_ps = 'ps axww | grep %s | grep -v grep' % (self.DAEMON_NAME,)
        cmd_ps_out = self.shell.execute_command(cmd_ps)
        is_running = len(cmd_ps_out) > 0
        self._write_log('Checking whether %s is already running: % s' % \
                        (self.DAEMON_NAME_PRINTABLE, is_running))
        return is_running

    def is_config_valid(self):
        self._write_log('Verifying %s config...' % (self.DAEMON_NAME_PRINTABLE,))
        should_continue_service_run = False
        if self.is_running():
            self.stop()
            should_continue_service_run = True
        status = self.shell.execute_command('sudo check-radiusd-config')
        self._write_log('%s config verification status:\n %s' % \
                        (self.DAEMON_NAME_PRINTABLE, status))
        if status.find('Radius server configuration looks OK.') >= 0:
            if should_continue_service_run:
                self.start(False)
            return True
        else:
            return False

    def preserve_settings(self):
        self._write_log('Preserving %s settings...' % (self.DAEMON_NAME_PRINTABLE,))
        temp_arch_path = os.path.join('/', 'tmp', '%s_settings_%d.tar.gz' % \
                                      (self.DAEMON_NAME,
                                       int(time.mktime(datetime.now().timetuple()))))
        status = self.shell.execute_command('sudo tar cfz %s %s' % (temp_arch_path,
                                                                    os.path.join(self.CONF_DIR, )))
        if status.find('tar: Error') >= 0:
            raise ConfigError('Unable to save current %s config\n %s' % \
                              (self.DAEMON_NAME_PRINTABLE, status))
        self._write_log('%s settings were successully saved as %s' % \
                        (self.DAEMON_NAME_PRINTABLE, temp_arch_path))
        return temp_arch_path

    def restore_settings(self, saved_config_path, should_clean_archived_settings=True):
        self._write_log('Restoring % s settings...' % (self.DAEMON_NAME_PRINTABLE,))
        self.stop()
        status = self.shell.execute_command('sudo tar xC / -f %s' % (saved_config_path,))
        if status.find('tar: Error') >= 0:
            raise ConfigError('Unable to restore current %s config\n %s' % \
                              (self.DAEMON_NAME_PRINTABLE, status))
        self._write_log('%s settings were successfully restored' % \
                        (saved_config_path,))
        self.start()
        if should_clean_archived_settings:
            self.shell.execute_command('sudo rm -f "%s"' % (saved_config_path,))

    def get_config(self, config_name):
        self._write_log('Getting config file of %s...' % (self.DAEMON_NAME_PRINTABLE,))
        dst_path = os.path.join(tempfile.mkdtemp(), config_name)
        src_path = os.path.join('/', 'tmp', config_name)
        try:
            self.shell.execute_command('sudo cp -f %s %s' % \
                                       (os.path.join(self.CONF_DIR, config_name),
                                        src_path))
            self.shell.execute_command('sudo chmod 666 %s' % (src_path,))
            self._write_log('Downloading %s\'s %s config to local machine...' % \
                            (self.DAEMON_NAME_PRINTABLE, config_name))
            self.shell.get_file(src_path, dst_path)
            self._write_log('Download finished')
            if os.path.exists(dst_path):
                with open(dst_path, 'rU') as f:
                    config_content = f.read()
            else:
                raise ValueError('Radius config file %s can not be found on host %s' % \
                                 (config_name, self._hostname))
            return config_content
        finally:
            self.shell.execute_command('sudo rm -f "%s"' % (src_path,))
            del_tree(os.path.split(dst_path)[0])

    def set_config(self, config_name, content):
        self._write_log('Preparing config file of %s...' % (self.DAEMON_NAME_PRINTABLE,))
        src_path = os.path.join(tempfile.mkdtemp(), config_name)
        with codecs.open(src_path, 'w', 'utf-8') as f:
            f.write(content)
        dst_path = os.path.join('/', 'tmp', config_name)
        try:
            self.shell.execute_command('sudo rm -f "%s"' % (dst_path,))
            self._write_log('Uploading %s\'s %s config to remote machine...' % \
                            (self.DAEMON_NAME_PRINTABLE, config_name))
            self.shell.put_file(src_path, dst_path)
            upload_cmds = ['sudo chown %s %s' % (self.SERVICE_NAME, dst_path),
                           'sudo chmod 640 %s' % (dst_path,),
                           'sudo mv -f %s %s' % (dst_path,
                                                 os.path.join(self.CONF_DIR, config_name))]
            for cmd in upload_cmds:
                self.shell.execute_command(cmd)
            try:
                self.stop()
                self.start()
                self._write_log('Upload status: OK')
            except RuntimeError:
                raise ConfigError('%s has failed to restart. Please double check your ' \
                                  '%s config file first' % \
                                  (self.DAEMON_NAME_PRINTABLE, config_name))
        finally:
            del_tree(os.path.split(src_path)[0])


def close_all_opened_cli_connections():
    for shell in FreeRadiusServer.SHELL_CONNECTIONS_POOL.itervalues():
        try:
            shell.close_connection()
        except Exception as e:
            print e


atexit.register(close_all_opened_cli_connections)

if __name__ == '__main__':
    server = FreeRadiusServer('localhost')

    print '******'
    print server.get_config('users')
    print '******'

    settings_path = server.preserve_settings()
    try:
        clients_content = server.get_config('clients.conf')
        server.set_config('clients.conf', clients_content + '\n')
        clients_content2 = server.get_config('clients.conf')
        assert (clients_content != clients_content2)
    finally:
        server.restore_settings(settings_path)

    server.stop()
    server.start()
    server.restart()

    print 'Press Ctrl+Z to exit...'
