#!/usr/bin/python
__revision = '$Revision: #1 $'
"""
It allows the caller to:
    - run unix commands on the WSA's backdoor
    - start/stop/reestart heidmall monitored applications (eg. hermes)
"""

import sal.net.sshlib
from sal import irontools
import time
import sal.time
import sal.logging
import paths
import re
import sal.deprecated.expect as expect
import curses.ascii
import os
import shellcmds
import qlogreader

debug = False
sh_prompt = '_IafPrompt_> '  # sh prompt not bash prompt


class IronPortShellBase:
    def __init__(self, sess):
        self._sess = sess

    def send_cmd(self, cmd, timeout=None):
        print "*DEBUG* Sending commands to shell:", cmd
        self._sess.writeln(cmd)
        time.sleep(0.5)
        out = self._sess.wait_for_prompt(timeout=timeout, read_by_line=True)
        print "*DEBUG* out:", out
        return out.replace((cmd + '\r\n'), '').replace(sh_prompt, '')

    def send_cmd_list(self, cmd_list, timeout=None):
        out = ''
        for cmd in cmd_list:
            self._sess.writeln(cmd)
            time.sleep(0.5)
            out += self._sess.wait_for_prompt(timeout=timeout,
                                              read_by_line=True)
        return out

    def __getattr__(self, name):
        """Delegate session calls to self._sess"""
        return getattr(self._sess, name)


class IronPortShell(IronPortShellBase):
    """ This class provides the interface to the WSA's unix shell."""

    def __init__(self, sess):
        IronPortShellBase.__init__(self, sess)
        self.heimdall = HeimdallInterface(sess)
        self.backdoor = BackdoorInterface(sess)
        # Note that we pass the IronportShell to QlogReader
        self.logreader = qlogreader.QlogReader(self)

        self.paths = paths.get_paths()
        self.test_tools_path = str(paths.get_paths().binary_home)
        self.testd = shellcmds.TestdInterface(sess, self.test_tools_path)
        self.query_cli = shellcmds.QueryCLI(sess, self.test_tools_path)
        self.table_reader = shellcmds.MultipleTableReader(sess,
                                                          self.test_tools_path)

    def exit(self):
        out = self.send_cmd('exit')
        return out


class BackdoorInterface(IronPortShellBase):
    """telnet to /tmp/<app_name>.bd and execute python code.
    NOTES:
        1. Use IronPortShellBase classe's self.send_cmd() to
           invoke Backdoor commands.
        2. If the Backdoor is opened, it must first be closed
           before Shell commands can be invoked again. In other words
           interlacing backdoor and shell commands is not allowed.
    """

    def __init__(self, sess):
        IronPortShellBase.__init__(self, sess)
        self._app_name = None

    def run(self, app_name=None, code_list=()):
        """Run a python program in the backdoor:
                Open the backdoor.
                Run the python code.
                Close the backdoor.  """
        self._app_name = app_name or self._app_name
        assert self._app_name
        assert len(code_list)

        out = self.open(self._app_name)
        # for code in code_list:
        #    out += self.send_cmd(code)
        out = self.send_cmd_list(code_list)
        out += self.close()
        return out

    def open(self, app_name=None):
        """Open backdoor"""
        self._app_name = app_name or self._app_name
        assert self._app_name

        self._old_prompt = self._sess.prompt
        self._sess.set_prompt(expect.RegexUserMatch('>>> |\.\.\. '))

        cmd = 'telnet /tmp/%s.bd' % self._app_name
        out = self.send_cmd(cmd)
        return out

    def close(self):
        """Close backdoor"""
        # send control-D to exit backdoor and return to unix shell
        self._sess.write(chr(curses.ascii.EOT))

        self._sess.set_prompt(self._old_prompt)
        out = self._sess.wait_for_prompt()
        return out


class HeimdallInterface(IronPortShellBase):
    """Control processes via heimdall_svc.
    Allow start, stop, restart and status of applications.
    """
    heimdall_svc = paths.get_paths().binary_home.heimdall_svc

    def __init__(self, sess, app_name=None):
        IronPortShellBase.__init__(self, sess)
        self._app_name = app_name

    def set_app(self, app_name):
        self._app_name = app_name

    def start(self, app_name=None, block=True):
        global debug
        if debug: print 'heimdall_svc start', app_name
        self.heimdall_command(app_name, action='-u')

        if not block:
            return

        # check app's status. block until it has started (ie. pid !=0)
        tmr = sal.time.CountDownTimer(60).start()
        while tmr.is_active():
            pid = self.status(app_name)
            if pid != -1:
                break
            time.sleep(1)
        else:
            raise RuntimeError, 'failed to start %s' % self._app_name

        if debug: print 'wait 2s for %s app to initialize' % str(app_name)
        time.sleep(2)

    def stop(self, app_name=None, block=True):
        global debug
        if debug: print 'heimdall_svc stop', app_name
        self.heimdall_command(app_name, action='-D')

        if not block:
            return

        # check app's status. block until it has started (ie. pid !=0)
        tmr = sal.time.CountDownTimer(30).start()
        while tmr.is_active():
            pid = self.status(app_name)
            if pid == -1:
                break
            time.sleep(1)
        else:
            raise RuntimeError, 'failed to stop %s' % app_name

    def restart(self, app_name=None, block=True):
        global debug
        if debug: print 'heimdall_svc restart', app_name
        old_pid = self.status(app_name)
        self.heimdall_command(app_name, action='-r')

        if not block:
            return

        # check app's status. block until it has started (ie. pid !=0)
        tmr = sal.time.CountDownTimer(60).start()
        while tmr.is_active():
            pid = self.status(app_name)
            if pid != -1 and pid != old_pid:  # new process has started
                break
            time.sleep(1)
        else:
            raise RuntimeError, 'failed to restart %s' % app_name

        if debug: print 'wait 2s for %s app to initialize' % str(app_name)
        time.sleep(2)

    def status(self, app_name=None, return_info=('pid',)):
        """Returns requested info of a process managed by heimdall.

        Parameters:
           - `app_name`: name of process to get status.
           - `return_info`: a tupple of the followings status: 'enabled',
                            'ignore', 'pid', 'ready', or 'up'.  Defaulted to
                            'pid'.
        """
        return_list = []
        out = self.heimdall_command(app_name, action='-s')
        app_info_dict = eval(out.strip())
        for status in return_info:
            try:
                return_list.append(app_info_dict[status])
            except KeyError:
                print('*WARN* Invalid `%s` return info.  Returned None for '
                      'it' % status)
                return_list.append(None)
        if len(return_list) == 1:
            return return_list[0]
        else:
            return tuple(return_list)

    def heimdall_command(self, app_name=None, action=None):
        """Run for example:  heimdall_svc -u hermes.

        heimdall_svc
          Controlls the heimdall daemon.
        Usage:
          heimdall_svc [unix_socket_path] command
          unix_socket_path defaults to /tmp/heimdall.sock
        commands:
          -i app_name        ignore this app
          -D app_name        bring down this app
          -x app_name        bring down this app (w/o force quit)
          -u app_name        bring up this app
          -s app_name        get the status (pid, up, ignore) -n app_name        app_name is done initializing, continue
          -r app_name        recycle app_name.  brings it down then up (-x, -u)
          -H                 halt the system
          -R                 reboot the system

        """
        app_name = app_name or self._app_name
        cmd = ' '.join((self.heimdall_svc, action, app_name))
        out = self.send_cmd(cmd)
        return out


# backdoor shell
def get_shell(cfg=None,
              hostname=None, user=None, password=None, logfile=None):
    """get_shell() has two calling signatures.
    Specify either:
            1) cfg argument or
            2) hostname, user, password, prompt, logfile args
    """
    global sh_prompt

    devmode = False
    if os.environ.get('IAF2_DEVMODE'):
        devmode = True

    # ssh session to WSA's unix shell
    if cfg:
        if isinstance(cfg, basestring):
            # initial access to shelllog instantiates shelllog object
            hostname = cfg
            sess = irontools.get_ruser_ssh(hostname)
        else:
            # initial access to shelllog instantiates shelllog object
            logfile = sal.logging.get_or_create_logger(cfg.log_dir,
                                                       'shell_logger', 'shell.log', cfg.dut.hostname)
            sess = sal.irontools.get_ruser_ssh(cfg.dut.hostname, logfile)
    else:
        sess = sal.net.sshlib.get_ssh_unsafe(hostname, user, password,
                                             prompt=None, logfile=logfile, devmode=devmode)

    # change to prompt which is unique (eg Iaf_Prompt> is better than #).
    # note: we try to match sh_prompt at the beginning of the line
    #       or sometimes if interrupt(control-C) is sent, the
    #       prompt will be prefixed by ^C (two characters ^ and C)
    #       and we match on '^C'+sh_prompt
    sess.set_prompt(expect.RegexUserMatch(
        re.compile('(^%s|\^C%s)' % (sh_prompt, sh_prompt), re.MULTILINE)))
    sess.writeln('env PS1="%s" sh' % sh_prompt)  # always use bourne shell
    sess.wait_for_prompt()

    # create Shell
    shell = IronPortShell(sess)

    return shell


if __name__ == '__main__':
    from iafframework import iafcfg

    # ssh to mga's unix shell
    shell = get_shell(iafcfg.get_cfg())
    # shell = get_shell('cinnamon.qa')

    # SHELL: unix shell commands
    print shell.send_cmd('echo #')
    print shell.send_cmd('echo \#')
    print shell.send_cmd('ls')
    print shell.send_cmd('pwd')
    print shell.send_cmd('hostname')

    # HEIMDALL_SVC: start/stop/restart/status hermes
    shell.heimdall.set_app('hermes')
    print 'status', shell.heimdall.status()
    print 'stop', shell.heimdall.stop(block=True)
    print 'status', shell.heimdall.status()
    print 'start', shell.heimdall.start(block=True)
    print 'status', shell.heimdall.status()

    # BACKDOOR: Run some python code in /tmp/hermes.bd
    code_list = (
        'for i in range(3):',
        '   print i',
        '',
    )
    out = shell.backdoor.run('hermes', code_list)
    print out

    # SHELL: some more unix commands
    print shell.send_cmd('date')
    print shell.send_cmd('ps')
    out = shell.backdoor.run('hermes', code_list)
    print out

    result = shell.logreader.set_filename('mail_log')
    result = shell.logreader.search('MID .* queued for delivery')
    print result
