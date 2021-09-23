#!/usr/bin/env python

import commands
import re
import sal.deprecated.proctools
import sal.net.sshlib
import sal.time
import socket
import tempfile
import os

from sal import logging
from sal.containers import odict
from sal.containers.scalarlist import ScalarList
from sal.deprecated import expect
from sal.exceptions import TimeoutError

debug = True
# TODO:LOW: backdoor
parse_backdoor_port = False


# parse_backdoor_port = True

class SmtpSpamParams:
    """Store command-line arguments to the smtp_spam command.
    Use build_cmd() to generate complete smtp_spam command
    which can be passed to expect object for execution.  """

    def __init__(self, smtp_spam_port=None):
        self.smtp_spam_port = smtp_spam_port
        self.clear()
        self.set_defaults()

    def clear(self):
        """Set all smtp_spam_params to None"""
        param_names = (
            'inject-host=', 'rcpt-host-list=', 'num-msgs=', 'port=',
            'bind-ips=',
            'mail-from=', 'mail-from-in-list=', 'num-senders=',
            'msg-size=', 'msg-filename=', 'mbox-filename=',
            'mbox-header=', 'cache-mbox=', 'attach-filename=',
            'address-list=', 'repeat-address-list=',
            'addr-per-msg=', 'max-msgs-per-conn=',
            'concurrency=', 'duration=', 'delay=', 'timeout=',
            'bandwidth-cap=', 'connection-bandwidth-cap=',
            'auth-method=', 'user=', 'passwd=', 'smtpauth-file=', 'tls=',
            'DUT=', 'workq-target=', 'queue-target=',
            'merge-xmrg', 'merge-parts', 'merge-defs', 'workq-verbose',
            'debug', 'verbose', 'dot=', 'custom-header=', 'subject=',
            'msg-body=', 'tls-cert-file=', 'tls-key-file=',
            'journal-mail-to=', 'bounce-mailer=')
        self.smtp_spam_params = odict.odict()
        for param_name in param_names:
            self.smtp_spam_params[param_name] = None
        self.extra_opts = ''

    def __str__(self):
        s = ''
        for k, v in self.smtp_spam_params.items():
            if v == None:
                continue
            if k[-1] != '=' and not v:
                continue
            if k[-1] == '=':
                s += 'param: %s%s\n' % (k, v)
            else:
                s += 'param: %s\n' % k
        return s

    def set_defaults(self):
        """Sets params:
            inject-host=dut.ifc.public().address
            rcpt-host-list=socket.gethostname()
            port=cfg.smtp_spam.port"""

        # rcpt_host_list
        self.smtp_spam_params['rcpt-host-list='] = socket.gethostname()

        # port
        if self.smtp_spam_port:
            self.smtp_spam_params['port='] = str(self.smtp_spam_port)

    ### smtp_spam_param accessors (getter/setter)
    def get(self, name):
        return self.smtp_spam_params[name]

    def set(self, name, value):
        self.smtp_spam_params[name] = value

    def _normalize(self, name):
        """Normalize 'name' to make comparison with other names easier."""

        # hyphens converted to underscore
        name = name.replace('-', '_')
        # remove equal sign
        name = name.replace('=', '')
        # all lower case
        return name.lower()

    def _is_spam_param(self, name):
        """Is 'name' a key in the smtp_spam_params dictionary?.
        Return True or False"""
        for ssp_name in self.smtp_spam_params.keys():
            if self._normalize(name) == self._normalize(ssp_name):
                return True
        else:
            return False

    def get_name(self, name):
        """Get full cannonical smtp_spam parameter name.
        Use 'name' to find the exact key name in the smtp_spam_params
        dictionary.  Return cannonical smtp_spam param name."""
        for ssp_name in self.smtp_spam_params.keys():
            if self._normalize(name) == self._normalize(ssp_name):
                return ssp_name
        else:
            raise KeyError, name

    def build_cmd(self, full_path='/usr/godspeed/bin/smtp_spam', extra_opts='', **kwargs):
        """Build the smtp_spam command using parameters from various
        inputs (in order):
                self.smtp_spam_params
                kwargs
                extra_opts
        """
        self.extra_opts = extra_opts
        smtp_spam_params = ''

        # override default params
        if kwargs:
            for name, value in kwargs.items():
                if self._is_spam_param(name):
                    self.smtp_spam_params[self.get_name(name)] = value

        # eliminate inject_host, rcpt_host_list, and/or port
        # from self.smtp_spam_params if they are present in extra_opts
        for param in ('inject-host', 'rcpt-host-list', 'port'):
            if self.extra_opts.find('--%s=' % param) > -1:
                try:
                    del self.smtp_spam_params[param + '=']
                except KeyError:  # already not present, ignore
                    pass

        # build using smtp_spam_params
        for k, v in self.smtp_spam_params.items():
            if v == None:
                continue
            name = self.get_name(k)
            if name[-1] == '=':  # optname=optvalue
                if self._normalize(name) == 'inject_host':
                    # don't do anything if it is ip address
                    if not self._check_if_ipaddress(v):
                        if os.environ.has_key('IAF2_INETMODE') and os.environ['IAF2_INETMODE'] == 'ipv6':
                            v = socket.getaddrinfo(v, None, 28)[0][4][0]
                        else:
                            v = socket.gethostbyname(v)
                smtp_spam_params += ' --' + name + str(v)
            else:  # optname only
                if v:
                    smtp_spam_params += ' --' + name

        # append extra_opts (use full path to not depend on PATH)
        return ' '.join((full_path, smtp_spam_params, self.extra_opts))

    def _check_if_ipaddress(self, value):
        try:
            # check for ipv4 address
            socket.inet_aton(value)
            return True
        except socket.error:
            pass
        try:
            # check for ipv6 address
            socket.inet_pton(socket.AF_INET6, value)
            return True
        except socket.error:
            return False


class SmtpSpam(object):
    "Provide API to start smtp_spam command locally or remotely"

    def __init__(self, smtp_spam_port=None, remote_host=None, log_dir=None):

        # all attributes created in constructor
        object.__setattr__(self, '_attr_lock', False)

        self._params = SmtpSpamParams(smtp_spam_port)
        self._expect = None
        # start smtp_spam on remote host? if self._rmt_host=None start locally

        # gotten from cfg.smtp_spam.remote_host
        self._rmt_host = remote_host

        self._backdoor_port = -1

        if not log_dir:
            log_dir = '%s/tmp/' % os.environ['SARF_HOME']
        self._logfile = logging.get_or_create_logger(log_dir,
                                                     'smtpspam_logger',
                                                     'smtpspam.log')

        # no new attributes can be added to this classes after this point
        self._attr_lock = True

    def __str__(self):
        s = str(self._params)
        return s

    def __getattr__(self, name):
        """When attribute names do not exist in this class
        search self._params."""
        if self.__dict__.has_key('_params') \
                and self._params._is_spam_param(name):
            return self._params.get(self._params.get_name(name))
        else:
            raise KeyError, name

    def __setattr__(self, name, value):
        """When attribute name exists in self._params set the
        value there. Otherwise set the instance attribute as usual."""
        if hasattr(self, '_params') and \
                self._params._is_spam_param(name):
            self._params.set(self._params.get_name(name), value)
        else:
            if self._attr_lock and not hasattr(self, name):
                # Prevent unknown null_smtpd parameters from being specified.
                raise RuntimeError, 'not allowed to add new attribute(%s:%s)' \
                                    % (name, value)
            object.__setattr__(self, name, value)

    def clear_params(self):
        self._params.clear()

    def set_defaults(self):
        self.clear_params()
        self._params.set_defaults()

    def set_remote_injector(self, host):
        self._rmt_host = host

    def clear_remote_injector(self):
        self._rmt_host = None

    def start(self, extra_opts='', **kwargs):
        """
        NOTE:
        1. When parameter `rcpt_host_list` receives more than one domain names
        select them by comma without any spaces.
            Ex.: start(rcpt_host_list='domain1.com,domain2.com,domain3.com',\
                       addr_per_msg=3, mail_from='mailer@some.com')
        """

        global parse_backdoor_port
        assert not self._expect, 'smtp_spam is already running'
        if self._rmt_host:
            # start smtp_spam on a remote host
            host = self._rmt_host
            full_name = sal.net.sshlib.ssh_command(host, user='root',
                                                   command='locate bin/smtp_spam', logfile=self._logfile).strip()
            if not full_name:
                raise ConfigError, 'Unknown location for null_smtpd'
            cmd = self._params.build_cmd(full_name, extra_opts, **kwargs)
            self._logfile.info('smtp_spam command:' + cmd)
            self._expect = self._remote_smtp_spam(host, user='root', cmd=cmd)
        else:
            # start smtp_spam locally
            full_name = commands.getoutput('locate bin/smtp_spam')
            if not full_name:
                raise ConfigError, 'Unknown location for smtp_spam'
            cmd = self._params.build_cmd(full_name, extra_opts, **kwargs)
            self._logfile.info('smtp_spam command:' + cmd)
            self._expect = self._local_smtp_spam(cmd)

        if parse_backdoor_port:
            self._set_backdoor_port()
        return self

    def _local_smtp_spam(self, cmd=None):
        if debug:
            print '_local_smtp_spam():cmd(', cmd, ')'
        pm = sal.deprecated.proctools.get_procmanager()
        proc = pm.spawnpty(cmd, logfile=self._logfile)
        exp = expect.Expect(proc)
        return exp

    def _remote_smtp_spam(self, host, user=None, password=None,
                          cmd=None):
        if debug:
            print '_remote_smtp_spam():cmd(', cmd, ')'
        exp = sal.net.sshlib.get_ssh(host, user, password, prompt=None,
                                     cmd=cmd, logfile=self._logfile, extraoptions='')
        return exp

    def _set_backdoor_port(self):
        "Thu Dec 15 15:31:35 2005 Backdoor started on port 8023"
        self._backdoor_port = -1

        line = self._expect.readline()  # read rest of line
        i = line.find('started on port')
        if i >= 0:
            mo = re.search('(\d+)', line)
            if mo:
                self._backdoor_port = int(mo.group(1))
                return
        else:
            full_output = line + self._expect.read()
            raise RuntimeError, 'Unable to determine backdoor port number - ' + \
                                'last line of smtpspam output was as ' + \
                                'follows:\n %s' % full_output.split('\r\n')[-2]

    def wait(self, timeout=0, read_sz=1024):
        """Wait for smtp_spam command to finish.
        timeout:  wait()  will for timeout seconds. Arg is ignored if 0.
        read_sz:        size of chunk of data to read (in bytes).

        TODO: NOTE:will read forever if smtp_spam injects forever.
        """
        assert self._expect, 'no expect session exists'
        tmr = sal.time.CountDownTimer(timeout).start()

        data = None
        while data or (data == None):
            data = self._expect.read(read_sz, timeout=0)
            if debug:
                print data
            if timeout != 0:
                if tmr.is_expired():
                    raise TimeoutError, 'NullSmtpd.wait() timeout after %ss' % timeout

        try:
            self._expect.close()
        except:
            pass
        self._expect = None

    def read(self, read_sz=512, timeout=30):
        """Read chunks of 512 bytes at a time"""
        assert self._expect, 'no expect session exists'
        data = self._expect.read(read_sz, timeout=timeout)
        if debug:
            print data
        return data

    def stop(self):
        assert self._expect, 'no expect session exists'
        try:
            self._expect.interrupt()
        except Exception, e:
            print 'stop(): Ignoring exception on interrupt():', str(e)

        try:  # for logging, read rest of smtp_spam output
            self._expect.read()
        except TimeoutError:
            print 'stop(): Ignoring exception on read():', str(e)

        try:
            self._expect.close()
        except:
            print 'stop(): Ignoring exception on close():', str(e)

        self._expect = None


class SmtpSpamMult(ScalarList):
    """ Wrapper around SmtpSpam which deals with multiple/remote injectors:

        smtp_spam = SmtpSpamMult()
        # Start standart smtp_spam session locally or remotely
        smtp_spam.start()
        # Start smtm_session on third host defined in smtp_spam.remote_host
        # smtp_spam object in smtp_spam[1] will be created implicitly
        smtp_spam[2].start()
    """

    def __init__(self):
        # First list element will always be default SmtpSpam object
        self.append(SmtpSpam())

    def _expand_list(self, key):
        """ Override ScalarList method to add SmtpSpam objects to the list.
        """
        # expand list to be 'key' size
        curr_len = len(self)
        while curr_len <= key:
            # Get host from smtp_spam.remote_host
            try:
                remote_host = self._rmt_host.split(',')[curr_len]
            except Exception, e:
                raise KeyError, 'Not enough hosts specified in smtp_spam.remote_host'

            spam_obj = SmtpSpam()
            # Set remote host
            spam_obj.set_remote_injector(remote_host)
            # Append newly created SmtpSpam object to a list
            self.append(spam_obj)

            curr_len += 1


if __name__ == '__main__':
    smtp_spam = SmtpSpam()
    # smtp_spam.set_remote_injector(host='qa19.qa')
    smtp_spam.verbose = True

    # All hyphens in smtp_spam argument names must be converted to underscores
    # since smtp_spam.inject-host is not a valid python attribute name.
    smtp_spam.inject_host = 'd2.emily.qa'

    smtp_spam.start(num_msgs=1)
    smtp_spam.wait()

    #    #smtp_spam.set_defaults()
    #    smtp_spam.num_msgs = 10
    #    smtp_spam.start()
    #    smtp_spam.wait()
    #    #import pdb; pdb.set_trace()

    smtp_spam = SmtpSpamMult()
    smtp_spam.verbose = True
    smtp_spam.start(num_msgs=5)
    smtp_spam[0].verbose = False  # Same as smtp_spam.verbose
    smtp_spam.wait()

    smtp_spam[1].start(num_msgs=5)
    smtp_spam[1].wait()
