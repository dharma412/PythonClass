#!/usr/bin/env python

"""Classes to control a Unix shell session:  IafUnixShellBase, get_sess()"""
from __future__ import absolute_import

# imports
import os
import re
import time
import sal.net.sshlib
import socket
import subprocess
from sal.deprecated import expect

debug = False


#: Reference Symbols: shellbase, shelltools

class IafUnixShellBase:
    """Represents remote shell
    """

    def __init__(self, sess):

        self._sess = sess

    def send_cmd(self, cmd, timeout=None):

        self._sess.writeln(cmd)
        time.sleep(0.5)
        out = self._sess.wait_for_prompt(timeout=timeout, read_by_line=True)
        return self.strip_prompt(out.replace((cmd + '\r\n'), ''))

    def send_cmd_list(self, cmd_list, timeout=None):

        out = ''
        for cmd in cmd_list:
            self._sess.writeln(cmd)
            time.sleep(0.5)
            out += self._sess.wait_for_prompt(timeout=timeout, read_by_line=True)

        return self.strip_prompt(out.replace((cmd + '\r\n'), ''))

    def strip_prompt(self, data_str):

        # This depends on the prompt being an expect.*Match* object,
        # or a string or a compiled regular expression.
        prompt = self._sess.prompt

        # If this prompt has an underlying pattern, get it.
        if hasattr(prompt, 'get_pattern'):
            prompt = prompt.get_pattern()

        # If prompt is a string, just replace it with ''
        if isinstance(prompt, basestring):
            return data_str.replace(prompt, '')

        # Otherwise prompt is a regex, do a sub call
        return prompt.sub('', data_str)

    def __getattr__(self, name):
        """Delegate session calls to self._sess"""
        return getattr(self._sess, name)

    def exit(self):
        self._sess.writeln('exit')
        self._sess.close()


class IafUnixLocalShellBase(IafUnixShellBase):
    """Defines object that provides 'local shell'."""

    def __init__(self, user=None, password=None, logger=None,
                 sudo_passwordless=False):
        """Initialization.

        :Parameters:
            - `user`: login name.
            - `password`: login password.
            - `logger`: logger object.
            - `sudo_passwordless`: if sudo doesn't require password this
                                   option should be set to True.
        """

        self.user = user
        self.password = password
        self.logger = logger
        self.sudo_passwordless = sudo_passwordless

        self.print_info = True

    def _log(self, method, msg):
        """Write message to log.

        :Parameters:
            - `method`: name of method to use: info, debug, warning, error.
            - `msg`: string to write in to a log.
        """

        if self.logger:
            exec ('self.logger.%s(msg)' % (method,))

    def info(self, str, msg_type='INFO'):
        """Print local shell info message.

        :Parameters:
            - `str`: info message.
            - `msg_type`: type of info message: INFO, NOTE, ERROR etc...
        """

        if self.print_info:
            print "... Local Shell %s: %s" % (msg_type, str)

    def do_not_print_info(self):
        """Do not allow printing info messages on the screen."""

        self.print_info = None

    def send_cmd(self, command):
        """Execute one command.

        :Parameters:
            - `command`: command to execute.
        """

        return self.send_cmd_list([command, ])

    def send_cmd_list(self, commands_list, read_stdout=True):
        """Execute the list of 'shell' commands. It could be UNIX commands
        or Product's scripts.

        :Parameters:
            - `commands_list`: the list of commands to execute one by one.

            e.g.
            commands_list=['sudo -S su corpus',
                           '/usr/local/ironport/corpus/etc/rc.d/corpus-\
            preprocessor.sh status',
                           'chmod 666 /tmp/msg.1']

            or

            commands_list=['sudo -S /usr/local/ironport/corpus/etc/rc.d/corpus-\
            preprocessor.sh status']
        """

        # Split the first command.
        # e.g. ['sudo', '-S', 'su', 'corpus']
        command = commands_list[0]
        args_list = command.split()

        # Print info message.
        self.info(command, 'Command')

        # Log.
        self._log('info', 'Execute command <%s>' % (command,))

        # Create subprocess.
        shell = subprocess.Popen(args=args_list,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        # Sudo requires password.
        if args_list[0] == 'sudo' and not self.sudo_passwordless:
            shell.stdin.write('%s\n' % (self.password,))

        # Write the rest of commands to shell's stdin.
        if commands_list[1:]:
            for command in commands_list[1:]:
                # Print on screen.
                self.info(command, 'Command')

                # Write to log.
                self._log('info', 'Execute command <%s>' % (command,))

                shell.stdin.write('%s\n' % (command,))

        # Close shell stdin.
        shell.stdin.close()

        ######################
        # Process stderr pipe.
        # Read shell stderr.
        if read_stdout:
            stderr_output = shell.stderr.read().strip()
        else:
            stderr_output = None

        # Close shell stderr.
        shell.stderr.close()

        ######################
        # Process stdout pipe.
        # Read shell stdout.
        if read_stdout:
            stdout_output = shell.stdout.read().strip()
        else:
            stdout_output = None

        # Close shell stdout.
        shell.stdout.close()

        if stdout_output:
            # Print info message on the screen.
            self.info(stdout_output, 'Result ')

            # Log result.
            self._log('info', 'Result of execution:\n%s' % (stdout_output,))

        # Return the result.
        return (stdout_output, stderr_output)

    def strip_prompt(self, data_str):
        """Overwrite. Is not needed in this class.
        """

        pass

    def exit(self):
        """Overwrite. Is not needed in this class.
        """
        pass


def get_sess(hostname, user=None, password=None, logfile=None, extraoptions=''):
    sh_prompt = 'ShellBase_Prompt> '
    sess = sal.net.sshlib.get_ssh(hostname, user, password, logfile=logfile,
                                  extraoptions=extraoptions,
                                  prompt=sh_prompt, force_prompt=sh_prompt)

    # change to prompt which is unique (eg Iaf_Prompt> is better than #).
    # note: we try to match sh_prompt at the beginning of the line
    #       or sometimes if interrupt(control-C) is sent, the
    #       prompt will be prefixed by ^C (two characters ^ and C)
    #       and we match on '^C'+sh_prompt
    return sess


def get_shell(hostname=socket.gethostname(),
              user=None,
              password=None,
              logfile=None,
              local=False,
              **args):
    """Return shell object

    :param hostname: (for ssh session)
    :param user: (for ssh session)
    :param password: (for ssh session)
    :param logfile: (for ssh session)
    :param local: if True get_shell returns local shell object
    """

    if not local:

        # create ssh session object
        sess = get_sess(hostname, user, password, logfile)

        # create remote shell object
        shell = IafUnixShellBase(sess)

    else:

        sudo_passwordless = False

        if args.has_key('sudo_passwordless'):
            sudo_passwordless = args['sudo_passwordless']

        # create local shell object
        shell = IafUnixLocalShellBase(user, password, logfile, sudo_passwordless)

    # return shell
    return shell


def backup_etc_hosts(shell):
    shell.send_cmd('cp /etc/hosts /etc/hosts.bak')


def restore_etc_hosts(shell):
    shell.send_cmd('mv /etc/hosts.bak /etc/hosts')


def load_etc_hosts(shell, entry_list):
    for entry in entry_list:
        shell.send_cmd('echo %s >> /etc/hosts' % entry)


def list_files(shell, *dir_list):
    files = []
    for directory in dir_list:
        out = shell.send_cmd('ls -1 %s' % directory).strip()
        files.extend([os.path.join(directory, f) for f \
                      in out.splitlines()])
    return files


def get_build(dut_type):
    """Gets installed build version of dut product.
    """
    # FIXME: Use shell or at least subprocess, not os.popen
    build_patt = r'(%s-[0-9.,\-_]+)\s+' % dut_type
    pkg_info = os.popen('/usr/sbin/pkg_info').read()
    match = re.search(build_patt, pkg_info)
    if match:
        return match.group(1)
    else:
        return ''
