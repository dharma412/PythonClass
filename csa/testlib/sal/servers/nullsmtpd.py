#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/sal/servers/nullsmtpd.py#2 $ $DataTime:$ $Author: revlaksh $

# This module uses these config settings from iafcfg.get_cfg():
#    null_smtpd.remote_host
#    null_smtpd.remote_user
#    null_smtpd.remote_password
#    null_smtpd.port
#    log_dir

##TODO:LOW
##  1. qabackdoor port
##  3. remote mbox log reading

import commands
import email
import mailbox
import os
import re
import sal.deprecated.proctools
import sal.irontools
import sal.net.socket
import sal.net.sshlib
import sal.time
import signal
import socket
import time
from subprocess import call

from sal import logging
from sal.containers import odict
from sal.deprecated import expect
from sal.exceptions import ConfigError
from sal.exceptions import TimeoutError

DEFAULT_PORT = 25
DEFAULT_LOG_DIR = os.path.join(os.getenv('SARF_HOME', '/'), 'tmp')
GET_PIDS_COMMAND = 'lsof -Pnl +M -i4 | grep null_smtp | grep LISTEN'
debug = True
parse_backdoor_port = True
_all_drains = []


def msg_factory(fp):
    try:
        return email.message_from_file(fp)
    except email.Errors.MessageParseError:
        return ''


class NullSmtpdParams:
    """Store command-line arguments to the null_smtpd command.
    Use build_cmd() to generate complete null_smtpd command
    which can be passed to expect object for execution.  """

    def __init__(self, port=None, bind_ip=None):
        self.clear()
        if port:
            self.null_smtpd_params['port='] = str(port)
        if bind_ip:
            self.null_smtpd_params['bind-ip='] = str(bind_ip)

    def __str__(self):
        raise NotImplementedError  ##TODO

    def clear(self):
        """Set all null_smtpd_params to None"""
        param_names = ('nostats', 'oldstats', 'grumpy', 'zipf=',
                       'port=', 'bind-ip=', 'sleep=', 'helo-sleep=',
                       'connection-bandwidth-cap=', 'bandwidth-cap=',
                       'collect=', 'drop=', 'sleep-domains=', 'max-message-size=',
                       'obs-real-world-file=', 'chop=', 'soft_bounce=',
                       'hard_bounce=', 'soft_bounce_rcpt=', 'hard_bounce_rcpt=',
                       'helo=', 'mail=', 'data=', 'rcpt=', 'message=',
                       'rset=', 'sleep', 'max-msgs-per-conn=',
                       'tls=', 'tls-required', 'tls-fail', 'tls-fail2', 'monitor',
                       'log=', 'log-ips', 'offer-smtpauth', 'offer-plain-only',
                       'offer-login-only', 'smtpauth-sleep', 'smtpauth-pct-succeed=',
                       'debug=', 'tls-certfile=', 'tls-keyfile='
                       # --repsonse-### option is not supported because:
                       #   See cvs log for godspeed/hammer/null_smtpd.py cvs-rev 1.20.
                       #   1) API would have to be modified to support this option
                       #   2) automated tests should not be using this since
                       #       it is only used to verify a bug.
                       # 'response-###=',
                       )
        self.null_smtpd_params = odict.odict()
        for param_name in param_names:
            # NOTE!! params set to None will be ignored by build_cmd()
            self.null_smtpd_params[param_name] = None
        self.extra_opts = ''

    ### get/set params
    def get(self, name):
        return self.null_smtpd_params[name]

    def set(self, name, value):
        self.null_smtpd_params[name] = value

    def _normalize(self, name):
        """Normalize 'name' to make comparison with other names easier."""

        # hyphens converted to underscore
        name = name.replace('-', '_')
        # remove equal sign
        name = name.replace('=', '')
        # all lower case
        return name.lower()

    def _is_null_smtpd_param(self, name):
        """Is 'name' a key in the null_smtpd_params dictionary?.
        Return True or False"""
        for ssp_name in self.null_smtpd_params.keys():
            if self._normalize(name) == self._normalize(ssp_name):
                return True
        else:
            if name.find('response_') == 0:  # is the "--response-###" option
                # see NOTES section regarding this option.
                raise ConfigError, name + ' option is not supported'
            else:
                return False

    def get_name(self, name):
        """Get full cannonical null_smtpd parameter name.
        Use 'name' to find the exact key name in the null_smtpd_params
        dictionary.  Return cannonical null_smtpd param name."""
        for nsp_name in self.null_smtpd_params.keys():
            if self._normalize(name) == self._normalize(nsp_name):
                return nsp_name
        else:
            raise KeyError, name

    def build_cmd(self, full_path='/usr/local/bin/null_smtpd', extra_opts='', **kwargs):
        """Build the null_smtpd command using parameters from various
        inputs (in order):
                self.null_smtpd_params
                kwargs
                extra_opts
        """
        self.extra_opts = extra_opts
        null_smtpd_params = ''
        # override default params
        if kwargs:
            for name, value in kwargs.items():
                if self._is_null_smtpd_param(name):
                    self.null_smtpd_params[self.get_name(name)] = value

        # build using null_smtpd_params
        for k, v in self.null_smtpd_params.items():
            if v == None:
                continue
            name = self.get_name(k)
            if name[-1] == '=':  # optname=optvalue
                if self._normalize(name) == 'inject_host':
                    # IPv6 Not implemented yet.
                    # if os.environ.has_key('IAF2_INETMODE') and os.environ['IAF2_INETMODE']=='ipv6':
                    #     v = socket.getaddrinfo(value, None, 28)[0][4][0]
                    # else:
                    v = socket.gethostbyname(v)
                null_smtpd_params += ' --' + name + str(v)
            else:  # optname only
                if v:
                    null_smtpd_params += ' --' + name

        # append extra_opts
        return ' '.join((full_path, null_smtpd_params, self.extra_opts))


def singleton(self, host, port):
    for drain in _all_drains:
        if (drain != self and drain.port == str(port) and drain.get_hostname() == host):
            try:
                # Stop the drain if already running
                # it raises AssertionError is not running
                drain.stop()
                # Sometimes process is still running even after stopping the drain
                if drain.is_server_running():
                    if self._is_local():
                        os.system("kill -9 %s" % self._expect.fileobject().childpid)
                    else:
                        pid = self._get_remote_nullsmtp_pid()
                        sal.net.sshlib.ssh_command(self.get_hostname(), user='root',
                                                   command='kill -9 %s' % (pid))
            except AssertionError:
                pass
            _all_drains.remove(drain)
        break
    return self


class NullSmtpdBase(object):
    "Provide API to start null_smtpd command locally or remotely"

    def __init__(self, port=None, bind_ip=None, remote_host=None, log_dir=None):
        # All attributes must be created in this constructor.
        # Attempts to create a new attribute dynamically will
        # result in an exception raised by __setattr__().
        object.__setattr__(self, '_attr_lock', False)
        _all_drains.append(self)

        if port == None:
            self._params = NullSmtpdParams(DEFAULT_PORT, bind_ip)
        else:
            self._params = NullSmtpdParams(port, bind_ip)

        self._expect = None
        self._bd = None

        if log_dir == None:
            self._log_dir = DEFAULT_LOG_DIR
        else:
            self._log_dir = log_dir

        self._rmt_host = None

        # start null_smtpd on remote host? if self._rmt_host=None start locally
        if remote_host:
            # If multiple remote hosts defined, take first one
            self._rmt_host = remote_host.split(',')[0]

        self._backdoor_port = -1
        self._logfile = logging.get_or_create_logger(self._log_dir,
                                                     'nullsmtpd_logger', 'nullsmtpd.log')

        self._mbox_filename = None
        self._mbox = None

        # no new attributes can be added to this classes after this point
        self._attr_lock = True

    def __del__(self):
        try:
            # Call the base class __del__ when overriding
            object.__del__(self)
            self.stop()
            if self._expect:
                self._expect.close()
        except AttributeError:
            pass

    def __getattr__(self, name):
        """When attribute names do not exist in this class
        search self._params for them."""
        if self.__dict__.has_key('_params') \
                and self._params._is_null_smtpd_param(name):
            return self._params.get(self._params.get_name(name))
        else:
            raise KeyError, name

    def __setattr__(self, name, value):
        """When attribute name exists in self._params set the
        value there. Otherwise set the instance attribute as usual."""
        if hasattr(self, '_params') and \
                self._params._is_null_smtpd_param(name):
            self._params.set(self._params.get_name(name), value)
        else:
            if self._attr_lock and not hasattr(self, name):
                # Prevent unknown null_smtpd parameters from being specified.
                raise RuntimeError, 'not allowed to add new attribute(%s:%s)', \
                    (name, value)
            object.__setattr__(self, name, value)

    def clear_params(self):
        self._params.clear()

    def set_defaults(self, port=None):
        'No default params set for null_smtpd'
        self._params.clear()
        if port:
            self._params.set("port=", str(port))

    def set_remote_drain(self, host):
        self._rmt_host = host

    def clear_remote_drain(self):
        self._rmt_host = None

    def _is_local(self):
        return self._rmt_host == None

    def get_stats(self, stat_name):
        self._bd = sal.irontools.get_toolbackdoor(self.get_hostname(),
                                                  self._backdoor_port)

        if not hasattr(self._bd, stat_name):
            raise ValueError, "No null_smtpd backdoor " \
                              "method for: %s" % stat_name

        return eval('self._bd.%s()' % stat_name)

    def reset_stats(self):
        sal.irontools.reset_drain_counters(self.get_hostname())

    def delete_mbox(self, mbox_filename):
        if not self._is_local():
            sal.irontools.remote_command(self.get_hostname(),
                                         command='rm -f %s 2>/dev/null' % mbox_filename,
                                         user='testuser',
                                         password='ironport')
            return
        try:
            os.unlink(mbox_filename)
            return
        except:
            pass
        os.system('rm -f %s 2>/dev/null' % mbox_filename)

    def get_mbox_filename(self, idx=0):
        mbox_filename = self._log_dir + '/nullsmtpd/mbox%02d.log' % idx

        dir_name = os.path.dirname(mbox_filename)
        if not os.path.exists(dir_name):
            logging.create_dir(dir_name)
        return mbox_filename

    def set_mbox(self, mbox_filename, do_delete=True):
        """Sets self._mbox by creating an mbox object."""
        if do_delete:
            self.delete_mbox(mbox_filename)

        self._mbox_filename = mbox_filename

    def next_msg(self, timeout, string=False):
        """Get next message in the mbox"""
        if not self._is_local():
            raise NotImplementedError  ##TODO:LOW

        self.handle_mbox_rollover()

        assert self._mbox, 'Must call set_mbox() first!'
        if timeout <= 0:
            return self._mbox.next()

        tmr = sal.time.CountDownTimer(timeout).start()
        while tmr.is_active():
            msg = self._mbox.next()
            if msg:
                if string:
                    return str(msg)
                else:
                    return msg
            time.sleep(1)
        else:
            return None

    def handle_mbox_rollover(self):
        """null_smtpd will automatically rollover the mbox specified by
        the --log argument when the mbox reaches 250MB (250*1024*1024).

        This method will open and start reading the new mbox file if
        the inode associated with self._mbox_filename has changed.
        """
        assert self._mbox
        assert self._mbox_filename

        # bad practise to directly access internal file pointer
        fnbr = self._mbox.fp.fileno()
        inode1 = os.fstat(fnbr).st_ino
        inode2 = os.stat(self._mbox_filename).st_ino
        if inode1 == inode2:
            return
        # mbox has rolled over.
        mb = self._mbox
        del mb
        self._mbox = None
        self._mbox = mailbox.PortableUnixMailbox(
            open(self._mbox_filename, 'rb'), msg_factory)

    def start(self, extra_opts='', **kwargs):
        global parse_backdoor_port
        assert not self._expect, 'null_smtpd is already running'

        ##TODO: if --log or --port is specified in extra_opts
        ##      override the default values
        if self._is_local():
            # start null_smtpd locally
            full_name = commands.getoutput('locate bin/null_smtpd')
            if not full_name:
                full_name = commands.getoutput('which null_smtpd')
                if not full_name:
                    raise ConfigError, 'Unknown location for null_smtpd'
            print 'null_smtpd binary location - %s' % full_name
            cmd = self._params.build_cmd(full_name, extra_opts, **kwargs)
            #            if self._logfile:
            #                self._logfile.info('null_smtpd command:' + cmd)
            singleton(self, self.get_hostname(), self.get_port())
            self._expect = self._start_local_null_smtpd(cmd)
        else:
            # start null_smtpd on a remote host
            host = self._rmt_host
            full_name = sal.net.sshlib.ssh_command(host, user='root',
                                                   command='locate bin/null_smtpd', logfile=self._logfile).strip()
            if not full_name:
                full_name = sal.net.sshlib.ssh_command(host, user='root',
                                                       command='which null_smtpd', logfile=self._logfile).strip()
                if not full_name:
                    raise ConfigError, 'Unknown location for null_smtpd'
            print 'null_smtpd binary location - %s' % full_name
            cmd = self._params.build_cmd(full_name, extra_opts, **kwargs)
            #            if self._logfile:
            #                self._logfile.info('null_smtpd command:' + cmd)
            # Start all remote drains as root to avoid setting up
            # individual SSH keys
            singleton(self, self.get_hostname(), self.get_port())
            self._expect = self._start_remote_null_smtpd(host,
                                                         user='root', cmd=cmd)

        # set backdoor port
        if parse_backdoor_port:
            self._set_backdoor_port()

        print 'NullSmtpdBase.start(): sleep to let drain finish initialization'
        check_host = self.get_hostname()
        LISTEN_TIMEOUT = 60 * 5
        tmr = sal.time.CountDownTimer(LISTEN_TIMEOUT).start()
        while tmr.is_active():
            if self._is_port_opened(check_host, self.get_port()):
                break
            time.sleep(1)
        else:
            raise RuntimeError('Drain is not listening on port %s within the %d' \
                               ' seconds timeout' % (self.get_port(),
                                                     LISTEN_TIMEOUT))
        print 'Drain is successfully started and is listening on port %s' % \
              (self.get_port(),)

        if (self._is_local() and self._mbox_filename):
            # if non-default log filename is used check for correct mbox
            if kwargs.has_key('log'):
                self._mbox_filename = kwargs['log']
            tmr = sal.time.CountDownTimer(60).start()
            while tmr.is_active():
                if os.path.exists(self._mbox_filename):
                    # open file in binary mode per mailbox pydoc
                    self._mbox = mailbox.PortableUnixMailbox(open(
                        self._mbox_filename, 'rb'), msg_factory)
                    print "INFO::Mbox:", self._mbox_filename
                    break
            else:
                raise RuntimeError, 'timed out waiting for mbox creation'

        # no need to check pid -- disabled for lightsmtpd
        # if not self.pid_file_exists():
        #    raise RuntimeError, 'No null_smtpd pidfile exists. Failed to start!'
        return self

    def _is_port_opened(self, host, port):
        if self._check_if_ipv6address(host):
            inet_mode = socket.AF_INET6
        else:
            inet_mode = socket.AF_INET
        s = socket.socket(inet_mode, socket.SOCK_STREAM)
        try:
            s.connect((host, int(port)))
            s.shutdown(2)
            return True
        except Exception as error:
            return False

    def _check_if_ipv4address(self, value):
        try:
            # check for ipv4 address
            socket.inet_aton(value)
            return True
        except socket.error:
            return False

    def _check_if_ipv6address(self, value):
        try:
            # check for ipv6 address
            socket.inet_pton(socket.AF_INET6, value)
            return True
        except socket.error:
            return False

    def pid_file_exists(self):
        # pid file is only created if smtp listener has started.
        if not self._expect:
            return False
        if self._is_local():
            tmr = sal.time.CountDownTimer(15).start()
            while tmr.is_active():
                pid = self._expect.fileobject().childpid
                if os.path.exists('/tmp/null_smtpd.%d' % pid):
                    return True
                time.sleep(1)
            else:
                return False
        else:
            return True  ##TODO: always return true for now!

    def _get_remote_nullsmtp_pid(self):
        cmd_output = sal.net.sshlib.ssh_command(self.get_hostname(), user='root',
                                                command=(GET_PIDS_COMMAND)).strip().split('\n')
        for output in cmd_output:
            if not "WARNING" in output:
                pid = output.split(' ')[1]
                return pid
        return None

    def is_server_running(self):
        if not self._expect:
            return False

        stats = None
        if self._is_local():
            pid = self._expect.fileobject().childpid
            stats = self._expect.fileobject().stat().stats
        # if drain is remote
        else:
            pid = self._get_remote_nullsmtp_pid()
            if pid:
                stats = sal.net.sshlib.ssh_command(self.get_hostname(), user='root',
                                                   command='ps -p %s|grep %s' % (pid, pid)).strip()
        if stats:
            return True
        else:
            return False

    def _start_local_null_smtpd(self, cmd=None):
        if debug:
            print '_start_local_null_smtpd():cmd(', cmd, ')'
        pm = sal.deprecated.proctools.get_procmanager()
        proc = pm.spawnpty(cmd, logfile=self._logfile)
        exp = expect.Expect(proc)
        return exp

    def _start_remote_null_smtpd(self, host, user=None, password=None,
                                 cmd=None):
        if debug:
            print '_start_remote_null_smtpd():cmd(', cmd, ')'

        exp = sal.net.sshlib.get_ssh(host, user, password, prompt=None,
                                     cmd=cmd, logfile=self._logfile, extraoptions='')
        return exp

    def _set_backdoor_port(self):
        "Thu Dec 15 15:31:35 2005 Backdoor started on port 8023"
        # set default value. -1 means it's not set.
        self._backdoor_port = -1

        try:
            mo = self._expect.expect('Backdoor started on port', timeout=5)
        except TimeoutError:
            return

        line = self._expect.readline()  # read rest of line
        mo = re.search('(\d+)', line)
        if mo:
            self._backdoor_port = int(mo.group(1))

    def get_backdoor_port(self):
        """return -1 if bd port not set. Otherwise return
        integer specifying bd port on local or remote drain host."""
        return self._backdoor_port

    def local_rollover(self):
        """Rollover  mbox log file.
        Only works for --log files on the local disk.
        Send USR1 signal to null_smtpd to initiate rollover."""
        if self._is_local():
            self._expect.fileobject().kill(signal.SIGUSR1)

    def get_hostname(self):
        """return 'localhost' or name of remote drain host"""
        if self.bind_ip:
            return self.bind_ip
        else:
            return self._rmt_host or 'localhost'

    def get_port(self):
        """return smtp port"""
        return self._params.get(self._params.get_name('port'))

    def read(self, read_sz=512, timeout=10):
        """Read chunks of 512 bytes at a time.

        Return empty string if expect finds EOF."""
        assert self._expect, 'no expect session exists'
        data = self._expect.read(read_sz, timeout=timeout)
        return data

    def read_for_duration(self, duration=30, read_sz=512, timeout=5):
        """Read from drain for 'duration' seconds.
        The data is read in multiple small chunks. The
        size of the chunk and amount of time to wait for
        the chunk of data to be read is controlled by 'read_sz'
        and 'timeout'.

        Return: data read from the drain.
                The returned data may be less than read_sz.
        """

        assert self._expect, 'no expect session exists'
        tmr = sal.time.CountDownTimer(duration).start()
        data = ''
        while tmr.is_active():
            try:
                data += self.read(read_sz=read_sz, timeout=timeout)
            except TimeoutError:
                pass
            print len(data)
            if len(data) >= read_sz:
                return data
        else:
            return data

    def read_all(self, timeout=60):
        """Read complete output from drain.

        Return: data read from the drain.
        """

        assert self._expect, 'no expect session exists'

        data = ''
        while 1:
            try:
                time.sleep(3)
                line = self._expect.readline()
            except TimeoutError:
                break
            data += line
            i = line.find('221')
            if i >= 0:
                break
        return data

    def stop(self):
        """stop is called from __del__().
        This means the global modules in sys.modules may
        no longer exist when this method is running!
        """

        assert self._expect, 'no expect session exists'
        try:
            self._expect.interrupt()
        except Exception, e:
            print 'NullSmtpdBase.stop(): Ignoring exception on interrupt():', str(e)

        rv = ''
        try:  # for logging, read rest of null_smtpd output
            rv = self._expect.read(timeout=1)
        except Exception, e:
            print 'NullSmtpdBase.stop(): Ignoring exception on read():', str(e)

        try:
            self._expect.close()
        except Exception, e:
            print 'NullSmtpdBase.stop(): Ignoring exception on close():', str(e)

        self._expect = None
        return rv


class NullSmtpd(NullSmtpdBase):
    def __init__(self, port=None, bind_ip=None, remote_host=None, log_dir=None, mbox_log_idx=0, do_mbox_delete=True):
        NullSmtpdBase.__init__(self, port, bind_ip, remote_host, log_dir)
        # Only create logging mboxes on the local machine
        if self._is_local():
            self.log = self.get_mbox_filename(mbox_log_idx)
            self.set_mbox(self.log, do_mbox_delete)


class Drain:
    def __init__(self, logfile=None, preserve_drain=False):
        self.logfile = logfile or "/tmp/%s-drain.log" % os.getenv('USER')
        if not preserve_drain:
            self.remove_logfile()

        # start the drain
        self.drain = NullSmtpd()
        self.drain.set_mbox(self.logfile)
        # I added the --log-ips option just because it's useful
        self.drain.start("--log=%s --log-ips" % (self.logfile))
        # it takes a couple of secs for the drain to start and open the file.
        print 'Drain: sleep 3s'
        time.sleep(3)
        self.mbox = mailbox.UnixMailbox(open(self.logfile), msg_factory)

    def remove_logfile(self):
        try:
            os.system('sudo rm %s 2>/dev/null' % self.logfile)
        except OSError:
            pass

    def next(self, timeout=10):
        return self._next(timeout)

    def _next(self, timeout):
        """Get next message in the mbox. Return None if no new messages.
           If timeout != 0, wait up to timeout seconds for the next
           message to arrive.
        """
        if not timeout:
            return self.mbox.next()

        tmr = sal.time.CountDownTimer(timeout).start()
        msg_obj = None
        while tmr.is_active() and (not msg_obj):
            msg_obj = self.mbox.next()
        return msg_obj

    def messages(self):
        """Sets and returns self.mbox as an iterator object.
        Call this in a 'for' loop to get a list of messages in the mbox.
        (see example at the bottom).
        """
        return self.mbox

    def close(self):
        self.drain.stop()
