#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/servers/mail_delivery.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit
import tempfile
import time
import os
import warnings

from SSHLibrary import SSHLibrary


class MailDeliveryDaemonError(Exception): pass


GET_TEMPPATH_CMD = 'python -c "import os, tempfile; ' \
                   'print(os.tempnam(tempfile.gettempdir()))"'


class MailDeliveryServer(object):
    DAEMON_DIR = '/usr/local/etc/rc.d'
    DAEMON_NAME = 'dovecot'
    CONTROLLER_NAME = 'doveadm'
    DAEMON_NAME_PRINTABLE = 'Dovecot Daemon'
    RC_CMD = 'sudo %s' % (os.path.join(DAEMON_DIR, DAEMON_NAME),)
    USER = 'testuser'
    PASSWORD = 'ironport'

    SHELL_CONNECTIONS_POOL = {}

    def __init__(self, hostname):
        self._hostname = hostname

    @property
    def hostname(self):
        return self._hostname

    @property
    def shell(self):
        should_reinit_shell = False
        if self._hostname in self.SHELL_CONNECTIONS_POOL:
            try:
                self.SHELL_CONNECTIONS_POOL[self._hostname].execute_command('uname')
            except Exception as e:
                should_reinit_shell = True
        if self._hostname not in self.SHELL_CONNECTIONS_POOL or should_reinit_shell:
            shell = SSHLibrary()
            shell.open_connection(host=self._hostname,
                                  timeout=5 * 60,
                                  prompt='$')
            shell.login(self.USER, self.PASSWORD)
            self.SHELL_CONNECTIONS_POOL[self._hostname] = shell
        return self.SHELL_CONNECTIONS_POOL[self._hostname]

    def start(self):
        if self.is_running():
            self._write_log('%s is already running' % (self.DAEMON_NAME_PRINTABLE,))
        else:
            self._write_log('Starting %s..' % (self.DAEMON_NAME_PRINTABLE,))
            status = self.shell.execute_command('%s start' % (self.RC_CMD,))
            # To be sure all processes are started
            time.sleep(1.0)
            self._write_log('Start status: %s' % (status,))
            if not self.is_running():
                raise MailDeliveryDaemonError('%s has failed to start on host %s' % \
                                              (self.DAEMON_NAME_PRINTABLE, self._hostname))
            self._write_log('%s start status: OK' % (self.DAEMON_NAME_PRINTABLE,))

    def stop(self):
        if self.is_running():
            self._write_log('Stopping %s...' % (self.DAEMON_NAME_PRINTABLE,))
            status = self.shell.execute_command('%s stop' % (self.RC_CMD,))
            # To be sure all processes are stopped
            time.sleep(1.0)
            self._write_log('Stop status: %s' % (status,))
            if self.is_running():
                raise MailDeliveryDaemonError('%s has failed to stop on host %s' % \
                                              (self.DAEMON_NAME_PRINTABLE, self._hostname))
            self._write_log('%s stop status: OK' % (self.DAEMON_NAME_PRINTABLE,))
        else:
            self._write_log('%s is already stopped' % (self.DAEMON_NAME_PRINTABLE,))

    def restart(self):
        if self.is_running():
            self._write_log('Restarting %s...' % (self.DAEMON_NAME_PRINTABLE,))
            status = self.shell.execute_command('%s reload' % (self.CONTROLLER_NAME,))
            self._write_log('Restart status: %s' % (status,))
        if not self.is_running():
            raise MailDeliveryDaemonError('%s has failed to restart on host %s' % \
                                          (self.DAEMON_NAME_PRINTABLE, self._hostname))

    def is_running(self):
        cmd_ps = 'ps axww | grep %s | grep -v grep' % (self.DAEMON_NAME,)
        cmd_ps_out = self.shell.execute_command(cmd_ps)
        is_running = len(cmd_ps_out) > 0
        self._write_log('Checking whether %s is already running: % s' % \
                        (self.DAEMON_NAME_PRINTABLE, is_running))
        return is_running

    def get_config(self, remote_path, local_path=None):
        if local_path is None:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning)
                local_path = os.tempnam(tempfile.gettempdir())
        remote_temppath = self.shell.execute_command(GET_TEMPPATH_CMD)
        self.shell.execute_command('sudo cp -f "%s" "%s"' % (remote_path,
                                                             remote_temppath))
        self.shell.execute_command('sudo chmod 666 "%s"' % (remote_temppath,))
        self.shell.get_file(remote_temppath, local_path)
        if not os.path.exists(local_path):
            raise OSError('Failed to get the config file %s from host %s' % \
                          (remote_path, self._hostname))
        else:
            self.shell.execute_command('sudo rm -f "%s"' % (remote_temppath,))
            self._write_log('Successfully transferred config from %s to %s' % \
                            (self._hostname, local_path))
        return local_path

    def set_config(self, local_path, remote_path, should_move_file=True):
        remote_temppath = self.shell.execute_command(GET_TEMPPATH_CMD)
        self.shell.put_file(local_path, remote_temppath)
        self.shell.execute_command('sudo mv -f "%s" "%s"' % (remote_temppath,
                                                             remote_path))
        self._write_log('Successfully transferred %s to %s' % (local_path,
                                                               self._hostname))
        self.restart()
        if should_move_file:
            os.unlink(local_path)

    def _write_log(self, log_str):
        print '%s :: %s' % (time.asctime(), log_str)


@atexit.register
def close_all_opened_cli_connections():
    for shell in MailDeliveryServer.SHELL_CONNECTIONS_POOL.itervalues():
        try:
            shell.close_connection()
        except Exception as e:
            print e
