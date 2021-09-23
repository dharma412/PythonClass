#! /usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/ftputility.py#2 $
# $DateTime: 2019/06/11 06:52:26 $
# $Author: revlaksh $

DEFAULT_TIMEOUT = 200
"""Timeout in seconds for waiting of response from remote host."""

DEFAULT_PEXPECT_BUFFER_SIZE = 524288
"""Buffer size for pexpect. Should be bigger for working with huge outputs."""

import re
from robot import utils
import logging
import os
import sys
import glob
import posixpath

try:
    import pexpect
except ImportError:
    raise ImportError('Importing pexpect module or its dependencies failed. '
                      'Make sure you have the required modules installed.')

import common.Variables


class ConnectionError(Exception): pass


class Logger:

    def _log_to_file(self, filename, level=logging.DEBUG):
        """Sends logs to a logfile, if they're not already going
        somewhere."""

        l = logging.getLogger("ftputility")
        if len(l.handlers) > 0:
            return
        l.setLevel(level)
        lh = logging.FileHandler(filename, 'w')
        lh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        l.addHandler(lh)
        return l


class ConnectionClient(object):
    """This class is responsible for launching an FTP client on a given host
    over ssh connection, creating session and running commands of the
    FTP client.
    """

    output_dict = {}
    """Outputs are stored here."""

    enable_logging = staticmethod(lambda path: Logger()._log_to_file(path))

    def __init__(self,
                 hostname,
                 username,
                 password,
                 time):
        """
        :Parameters:
            -`hostname`: host on which ftp client will be launched.
            -`username`: username for connecting to given host.
            -`password`: password for connecting to given host.
        """

        self.hostname = hostname
        self.username = username
        self.password = password
        self.command = None
        self.time_for_cmd_exec = time
        self.pexpect_buffer_size = None
        self.run_in_bg = False
        self.prompt = None
        # Flag to see if there was a previous attempt to open session
        self.session_is_opened = False
        self.ssh_connection = None

    def execute(self, command, prompt):
        """Executes command on hosts

        :Parameters:
            -`command`: command to execute. Command parameter may be
                        a string that includes a command and any
                        arguments to the command.
            -`prompt`: prompt to expect.
        """
        self.command = command.strip()
        self.prompt = prompt
        self._ssh_exec()

    def execute_in_session(self, command, prompt='ftp>'):
        """Executes command in opened sessions.

        :Parameters:
            - `command`: command to execute. command parameter may be a string
                         that includes a command and any arguments to the
                         command.
            - `prompt`: prompt to expect. Default is 'ftp>' prompt.
        """

        self.command = command.strip()
        self.prompt = prompt

        # Verify if session is opened.
        try:
            if self.session_is_opened:
                self._session_exec()
            else:
                return
        except pexpect.ExceptionPexpect, exc:
            err_msg = 'Failed to execute command \'%s\' on host \'%s\': %s' % \
                      (self.command, self.hostname, str(exc))
            raise ConnectionError(err_msg)

    def _ssh_exec(self):
        """Connects to specified host through SSH and execute command."""

        try:
            self.ssh_connection = None

            # We don't interrupt program when it is launched in background.
            if self.command.endswith('&'):
                self.command = self.command[:-1] + '> /dev/null 2>&1 &'
                ssh_command = 'ssh %s@%s \'%s\'' \
                              % (self.username, self.hostname, self.command)
                self.run_in_bg = True
            else:
                ssh_command = 'ssh -t %s@%s \'%s\'; echo $?' % \
                              (self.username, self.hostname, self.command)

            timeout = self.time_for_cmd_exec or DEFAULT_TIMEOUT
            bf_size = self.pexpect_buffer_size or DEFAULT_PEXPECT_BUFFER_SIZE

            self.ssh_connection = pexpect.spawn(ssh_command,
                                                timeout=timeout,
                                                maxread=bf_size,
                                                searchwindowsize=200)

            expect_list = [re.compile(r'\(yes\/no\)\?\s*$'),
                           re.compile(r'.*(P|p)assword\s*.*:\s*$'),
                           re.compile('not known\s*$'),
                           pexpect.TIMEOUT,
                           pexpect.EOF]

            # Update expect_list if prompt is specified.
            if self.prompt:
                expect_list.append(re.compile(r'%s' % (self.prompt,)))

            expect_list = self.ssh_connection.compile_pattern_list(expect_list)

            index = 0
            while index in [0, 1]:
                index = self.ssh_connection.expect_list(expect_list)
                if index is 0:
                    self.ssh_connection.sendline('yes')
                elif index is 1:
                    self.ssh_connection.sendline(self.password)
                elif index in [2, 3]:
                    if self.time_for_cmd_exec and index == 3:
                        break

                    if index is 2:
                        self.ssh_connection.before += self.ssh_connection.after

                    err_msg = 'Connection break: %s' % \
                              (self.ssh_connection.before,)
                    self.ssh_connection.close()
                    raise ConnectionError(err_msg)

            # Process output, get exit status, get rid of needless information.
            if self.run_in_bg:
                # Command has been launched in background mode.
                # We don't know its exit status.
                exitstatus = None
                output = ''
            else:
                try:
                    output = self.ssh_connection.before
                    output = output.splitlines()
                    # Get rid of needless information.
                    output = output[1:-2]
                    # Get exit status.
                    exitstatus = output[-1]
                    # Remove exit status from output.
                    output = output[:-1]
                except IndexError:
                    output = [self.ssh_connection.before, ]
                    exitstatus = None

            ConnectionClient.output_dict[self.hostname] = '\n'.join(output), \
                                                          exitstatus

            if self.prompt:
                if self.ssh_connection.isalive():
                    self.session_is_opened = True
                else:
                    err_msg = 'Session is not alive'
                    raise ConnectionError(err_msg)

        except pexpect.ExceptionPexpect, exc:
            err_msg = '%s: communication issues. %s: %s' % \
                      (self.hostname, exc.__class__.__name__, str(exc))
            if self.ssh_connection:
                self.ssh_connection.close()
            raise ConnectionError(err_msg)

    def _session_exec(self):
        """Execute command in already opened session."""

        # Check if there is a opened session.
        if not self.ssh_connection or not self.ssh_connection.isalive():
            err_msg = 'SSH session has not been opened yet.'
            raise ConnectionError(err_msg)

        # Send command.
        self.ssh_connection.sendline(self.command)
        expect_list = [re.compile(self.prompt),
                       pexpect.TIMEOUT,
                       pexpect.EOF]

        expect_list = self.ssh_connection.compile_pattern_list(expect_list)

        index = -1
        while index != 0:
            index = self.ssh_connection.expect_list(expect_list)
            if index in [1, 2]:
                if index == 1:
                    err_reason = "got pexpect TIMEOUT"
                else:
                    err_reason = "got pexpect EOF"
                err_msg = 'Broken session: %s\n%s' % \
                          (err_reason, self.ssh_connection.before)
                self.ssh_connection.close()
                raise ConnectionError(err_msg)

        output = self.ssh_connection.before
        exit_status = None
        ConnectionClient.output_dict[self.hostname] = (output, exit_status)


class FtpLibrary(object):
    """FTP Library is a test library for Robot Framework that enables executing
    ftp commands and working with FreeBSD ftp client or any other ftp client.
    FTP Library allows running an ftp client and its commands with different
    options both on local and remote machine over an ssh connection.

    FTP Library connects to given host and executes commands on the opened ssh
    connections.

    To use FTP Library you must first install pexpect implementation [1] and
    its dependencies.

    [1] http://pexpect.sourceforge.net/

    This library provides various keywords for working with ftp.
    Before executing some ftp commands  you must run ftp client using keyword
    'Start Ftp  Client'. When keyword 'Start Ftp Client' is used to execute
    ftp client, a new channel is opened over the SSH connection, ftp client is
    launched and then you can use other keywords to control ftp client
    and execute ftp  commands. Keyword 'Execute Ftp command' is used to execute
    every ftp client command with expected prompt.
    """

    def __init__(self, *args, **kwargs):

        self._client = None
        self._connections = []
        self.logger = None

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['start_ftp_client',
                'login_to_ftp_site',
                'execute_ftp_command',
                'ftp_get_file',
                'ftp_get_files',
                'ftp_put_file',
                'ftp_put_files',
                'ftp_delete_file',
                'ftp_delete_files',
                'ftp_log_out',
                'close_ftp_client',
                'close_all_ftp_clients',
                'assert_output',
                'set_ftp_debug',
                'start_ftp_command',
                'read_ftp_command_output',
                'enable_ftp_logging',
                'enable_debug_logging']

    def start_ftp_client(self, host_username, host_password,
                         ftp_client='tnftp', args=[], host='127.0.0.1',
                         prompt='ftp>', time=None):
        """Starts ftp client on remote machine with given host.
        The default value of `host` is localhost(127.0.0.1).

        :Parameters:
            -`host_username`: username for connecting to given host.
            -`host_password`: password for connecting to given host.
            -`ftp_client`: ftp client. The default is a standard
                           FreeBSD ftp client without any options.
            -`args`: list of options for ftp client.
            -`host`: host on which ftp client will be launched. The
                     default is localhost(127.0.0.1).
            -`prompt`: prompt to expect. The default is 'ftp>'.
            -`time`: timeout in seconds for waiting of response from ftp client.
        """

        self._client = ConnectionClient(host, host_username, host_password, time)

        variables = common.Variables.get_variables()
        if variables.has_key("${IPV_PARAM}"):
            ftp_client += (' ' + variables["${IPV_PARAM}"])
        else:
            ftp_client += ' -4'

        if args == []:
            command = ftp_client
        else:
            space = ' '
            command = ''
            for arg in args:
                command = command + space + arg
            command = ftp_client + command
        self._client.execute(command, prompt)
        self._connections.append(self._client)
        self._log('Start FTP client on host %s' % host)

    def login_to_ftp_site(self, ftp_site, username, password, account=None):
        """Logs in to given ftp site.

        :Parameters:
            -`ftp_site`: address of ftp server.
            -`username`: simple username or username in Raptor or
                         Check Point format to log in to the ftp
                         server.
            -`password`: simple password  or password in Raptor or
                         Check Point format  to log in to the ftp
                         server.
            -`account`:  account credential to log in to ftp server.
                         Required for Raptor authentication format.

        Example:
        | Login To Ftp Site | ftp.hp.com | anonymous | @anonymous |

        | Login To Ftp Site | vm10bsd0040.wga |
        | ... | ftpuser@vm10bsd0040.wga rtester |
        | ... | ironport |
        | ... | account=ironport |
        """

        command = 'open %s' % ftp_site
        self._client.execute_in_session(command, prompt='Name')
        self._client.execute_in_session(username, prompt='Password')
        if not account:
            self._client.execute_in_session(password, prompt='ftp>')
        else:
            self._client.execute_in_session(password, prompt='Account')
            self._client.execute_in_session(account, prompt='ftp>')
        self._log('Logging into %s as %s' % (ftp_site, username))
        self._log_output()
        return self._process_output(self._client.output_dict)

    def execute_ftp_command(self, command, args=[], prompt='ftp>'):
        """Executes an ftp command and returns output of this
        command until prompt is found.

        :Parameters:
            -`command`: command to execute. Command parameter may be
                        a string that includes a command and any
                        arguments to the command.
            -`args`: any arguments to the command. You may also pass
                     command its own argument list using this
                     parameter.
            -`prompt`: prompt to expect.

        :Return: Returns output of executed command until prompt
                 is found.

        Example:
        | ${output}= | Execute Ftp Command | command |
        """

        if args == []:
            new_command = command
        else:
            space = ' '
            new_command = ''
            for arg in args:
                new_command = new_command + space + arg
            new_command = command + new_command
        self._client.execute_in_session(new_command, prompt)
        self._log('Executing command %s' % new_command)
        self._log_output()
        return self._process_output(self._client.output_dict)

    def ftp_get_file(self, source, destination='', get_mode='binary',
                     ftp_mode=False):
        """Retrieves the remote-file and store it on the local machine.

        If the destination does not exist and it ends with path separator
        ('/' in unixes), it is considered a directory.
        That directory is created and source file copied into it.

        If the destination does not exist and it does not end with path
        separator, it is considered a file. If the path to the file does not
        exist it is created.

        By default, destination is empty, and in that case the current working
        directory in the local machine is used as destination.

        :Parameters:
            -'source': path to remote file to be copied. Using wild card
                       like '*' is allowed. When wild card is used,
                       destination MUST be a directory.
            -'destination': path to local files.
            -'get_mode': binary or ascii transfer mode.
            -'ftp_mode': turn on/off passive mode of FTP protocol. True/False.

        Examples:
        | Ftp Get File | /path_to_remote_file/file | /path_to_local_file/file |
        | Ftp Get File | /path_to_remote_files/*.txt | /path_to_destination_dir/ |
        | Ftp Get File | *.txt | /path_to_destination_dir/ |
        | Ftp Get File | *.txt | /path_to_destination_dir/ | ftp_mode=True |
        """

        self._client.execute_in_session(get_mode)
        expect = [re.compile(r'Type set to A'),
                  re.compile(r'Type set to I')]
        expect_list = []
        for item in expect:
            expect_list.append(item.search(
                self._process_output(self._client.output_dict)))
        if not any(expect_list):
            raise ValueError('Wrong transfer mode')
        if not ftp_mode:
            self._client.execute_in_session('passive')

        remotefiles = self._get_get_file_sources(source)
        self._log('Ftp Get File: Source pattern matched remote files: %s' \
                  % utils.seq2str(remotefiles))
        localfiles = self._get_get_file_destinations(remotefiles, destination)
        output = []
        for src, dst in zip(remotefiles, localfiles):
            command = 'get %s %s' % (src, dst)
            self._log('Getting %s to %s: %s' % (src, dst, command))
            self._client.execute_in_session(command)
            output.append(self._process_output(self._client.output_dict))
            self._log_output()
        return '\r\n'.join(output)

    def ftp_get_files(self, source):
        """Retrieves remote-files and store it on the local machine using
        `mget` command of ftp client.

        :Parameters:
            -'source': path to remote files.

        Examples:
        | Ftp Get Files | /path_to_remote_files/*.txt |
        | Ftp Get Files | *.py |
        """

        command = 'mget %s' % source
        self._log('Getting files using mget command: %s' % command)
        self._client.execute_in_session(command, prompt=']?')
        self._client.execute_in_session('a')
        self._log_output()
        return self._process_output(self._client.output_dict)

    def ftp_put_file(self, source, destination=' ', put_mode='binary',
                     ftp_mode=False):
        """Stores local file(s) on remote host using ftp.

        By default, destination is empty and the user's home directory in
        the remote machine is used as destination.

        :Parameters:
            -'source': path to file or files to be copied. Using wild card
                       like '*' is allowed. When wild card is used, destination
                       MUST be a directory.
            -'destination': destination where local file(s) are copied.
            -'put_mode': binary or ascii transfer mode.
            -'ftp_mode': turn on/off passive mode of FTP protocol. True/False.

        Examples:
        | Ftp Put File | /path_to_local_file/file | destination=/path_to_remote_file/file | ftp_mode=True |
        | Ftp Put File | /path_to_ local_files/*.txt | destination=/path_to_remote_dir/ |
        | Ftp Put File | /path_to_local_file/file | destination=/path_to_remote_file/file | put_mode='ascii' |
        """

        self._client.execute_in_session(put_mode)
        expect = [re.compile(r'Type set to A'),
                  re.compile(r'Type set to I')]
        expect_list = []
        for item in expect:
            expect_list.append(item.search(
                self._process_output(self._client.output_dict)))
        if not any(expect_list):
            raise ValueError('Wrong transfer mode')
        if not ftp_mode:
            self._client.execute_in_session('passive')

        localfiles = self._get_put_file_sources(source)
        self._log('Ftp Put File: Source pattern matched local files: %s' \
                  % utils.seq2str(localfiles))
        remotefiles = self._get_put_file_destinations(localfiles, destination)

        output = []
        for src, dst in zip(localfiles, remotefiles):
            command = 'put %s %s' % (src, dst)
            self._log("Putting '%s' to '%s': %s" % (src, dst, command))
            self._client.execute_in_session(command)
            self._log_output()
        return '\r\n'.join(output)

    def ftp_put_files(self, source):
        """Stores local files on remote host using `mput` command of ftp client.

        :Parameters:
            -'source': path to local files.

        Examples:
        | Ftp Put Files | /path_to_local_files/*.txt |
        | Ftp Put Files | *.py |
        """

        command = 'mput %s' % source
        self._log('Putting files using mput command: %s' % command)
        self._client.execute_in_session(command, prompt=']?')
        self._client.execute_in_session('a')
        self._log_output()
        return self._process_output(self._client.output_dict)

    def ftp_delete_file(self, remote_file):
        """Deletes remote-file on the remote host.

        :Parameters:
            -'remote_file': path to remote file to be deleted.

        Example:
        | Ftp Delete File | /path_to_remote_file/file |
        """

        command = 'delete %s' % remote_file
        self._log('Deleting remote file %s' % (remote_file,))
        self._client.execute_in_session(command)
        self._log_output()
        return self._process_output(self._client.output_dict)

    def ftp_delete_files(self, remote_files):
        """Deletes remote_files on the remote host.

        :Parameters:
            -'remote_files': path to remote files.

        Examples:
        | Ftp Delete Files | /path_to_remote_files/*.txt |
        | Ftp Delete Files | *.py |
        """

        command = 'mdelete %s' % remote_files
        self._log("Deleting remote files using mdelete command: %s" \
                  % command)
        self._client.execute_in_session(command, prompt=']?')
        self._client.execute_in_session('a')
        self._log_output()
        return self._process_output(self._client.output_dict)

    def ftp_log_out(self):
        """Closes currently active ftp connection.

        Example:
        | Ftp Log Out |
        """

        command = 'close'
        self._client.execute_in_session(command)
        self._log_output()

    def close_ftp_client(self):
        """Closes currently running ftp client.

        Example:
        | Close Ftp Client |
        """

        self._log('Closing ftp client on host %s' % self._client.hostname)
        self._client.ssh_connection.close()
        self._log_output()

    def close_all_ftp_clients(self):
        """Closes all running ftp clients.

        Can be used in [Teardown] section.

        Example:
        | Close All Ftp Clients |
        """

        self._log('Closing all running ftp clients')
        for ftp in self._connections:
            ftp.ssh_connection.close()

    def assert_output(self, output, expected_output):
        """Asserts command output.

        :Parameters:
            -`output`: output from given keyword.
            -`expected_output`: expected output.

        Example:
        | Assert Output | ${output} | ${expected_output} |
        """

        res = re.compile(r'%s' % expected_output, re.IGNORECASE)
        if not res.search(output):
            raise AssertionError('Expected data do not match returned data')

    def set_ftp_debug(self, level):
        """Toggle debugging mode of ftp client.

        When debugging is on, ftp prints each command sent to the remote
        machine, preceded by the string `-->`'.

        :Parameters:
            -`level`: debugging level. The default, 0, produces no debugging
                      output. A value of '1' produces a moderate amount of
                      debugging output, generally a single line per request.
                      A value of 2 or higher produces the maximum amount of
                      debugging output.

        Example:
        | Set Ftp Debug |
        """

        command = 'debug %s' % level
        self._log('Setting ftp debug')
        self._client.execute_in_session(command)
        self._log_output()

    def start_ftp_command(self, command):
        """Starts ftp command execution.

        :Parameters:
            -`command`: command to be started.

        This keyword doesn't return anything. Use Read Ftp Command Output
        to read the output generated from command execution.

        Note that the Read Ftp Command Output keyword always reads the output of
        the most recently started command.

        Example:
        | Start Ftp Command | some command |
        """

        self._client.execute_in_session(command)
        self._log_output()

    def read_ftp_command_output(self):
        """Reads and returns output of current command."""

        return self._process_output(self._client.output_dict)

    def enable_ftp_logging(self, logfile):
        """Enables logging of the output of each keyword to
        given `logfile`.

        :Parameters:
            -`logfile`: path to logfile.

        `logfile` can be relative or absolute path to a file that is writable by
        current user. In case that it already exists, it will be overwritten.
        """

        self.logger = ConnectionClient.enable_logging(logfile)
        self._log('Enabled logging to %s' % logfile)

    def enable_debug_logging(self, logfile):
        """All input and output of ftp client will be copied to the given
        file object.

        :Parameters:
            -`logfile`: path to logfile.

        Use Enable Debug Logging only after Start Ftp Client keword.
        Two different ftp clients can not log to the same `logfile`
        simultaneously with this keyword. Enable Debug Logging keyword
        overwrites the same `logfile`, which used by another ftp client.

        If you want to have logging from different ftp clients, use Enable
        Debug Logging keword with different logfiles after each Start Ftp
        Client keword.

        `loffile` is writable by current user.

        Example:
        | Start Ftp Client | username1 | password1 |
        | Enable Debug Logging | ftp1.log |
        | Start Ftp Client | username2 | password2 |
        | Enable Debug Logging | ftp2.log |
        """

        fout = file(logfile, 'w')
        self._client.ssh_connection.logfile = fout

    def _process_output(self, output):
        """Returns output of executed command."""
        return output[self._client.hostname][0].strip()

    def _create_local_dirs(self, dest):
        if not os.path.exists(dest):
            self._log("Creating missing local directories for path '%s'" \
                      % dest)
            try:
                os.makedirs(dest)
            except OSError, err:
                raise OSError(str(err) + "\nCouldn't create local directories" \
                                         " for path %s" % dest)

    def _get_get_file_destinations(self, sources, dest):
        if dest == '':
            dest = os.getcwd()
        else:
            if not dest.endswith(os.sep) and len(sources) > 1:
                raise ValueError('It is not possible to copy multiple source '
                                 'files to one destination file.')
            dest = os.path.split(dest)[0]
        dest = os.path.abspath(dest)
        self._create_local_dirs(dest)
        return [os.path.join(dest, os.path.split(file)[1]) for file in sources]

    def _get_get_file_sources(self, source):
        _, pattern = posixpath.split(source)
        command = 'nlist %s' % source
        self._client.execute_in_session(command)
        out = self._process_output(self._client.output_dict)
        out = out.split('\r\n')
        out.remove(command)
        sourcefiles = []
        for item in out:
            if item.endswith(pattern) or utils.matches(item, pattern):
                sourcefiles.append(item)
        if not sourcefiles:
            raise AssertionError("There were no source files matching '%s'" \
                                 % source)
        return sourcefiles

    def _get_put_file_destinations(self, sources, dest):
        dest = dest.replace('\\', '/')
        if dest == ' ':
            dest += '/'
        if len(sources) > 1 and dest[-1] != '/':
            raise ValueError('It is not possible to copy multiple source files '
                             'to one destination file.')
        dirpath, filename = self._parse_path_elements(dest)
        if filename:
            return [posixpath.join(dirpath, filename)]
        return [posixpath.join(dirpath, os.path.split(path)[1]) \
                for path in sources]

    def _parse_path_elements(self, dest):
        if not posixpath.isabs(dest):
            dest = posixpath.join('/', dest)
        return posixpath.split(dest)

    def _get_put_file_sources(self, source):
        sources = [file for file in glob.glob(source.replace('/', os.sep)) \
                   if os.path.isfile(file)]
        if not sources:
            raise AssertionError("There were no source files matching '%s'" \
                                 % source)
        return sources

    def _log(self, msg):
        msg = msg.strip()
        if msg != '':
            if self.logger is not None:
                if self._client:
                    self.logger.log(10, 'FTP[%s] %s' \
                                    % (self._client.hostname, msg))
                else:
                    self.logger.log(10, '%s' % (msg))

    def _log_output(self):
        self._log('*Output*\n' + self._process_output(self._client.output_dict))
