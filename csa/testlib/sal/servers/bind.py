#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/servers/bind.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
This module uses dnspython module which is a third party module
Details at
http://www.dnspython.org/

Documentation at
http://www.dnspython.org/docs/1.10.0/html/

"""

import tempfile
import sys, os
import traceback
import socket
import subprocess
import string
import time
import sal.shell.base
import sal.net.sshlib
import dns.zone
from dns import *
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *
from dns.rdtypes import *
from dns.rdtypes.IN import *
from dns.rdtypes.ANY import *
from dns.rdataset import *
from dns.rdata import *
from dns.update import *

SARF_LOCAL_TMPDIR = os.path.join(os.getenv('SARF_HOME', '/'), 'tmp')


class BindServerManager(object):
    """ Class to manage bind server """

    DAEMON_NAME_PRINTABLE = 'Bind Daemon'

    def __init__(self, hostname, should_preserve_server_config=True):
        self._hostname = hostname
        bind_cmd = '/usr/sbin/named -t /var/named -u bind'
        self._dns_cmd = 'sudo %s' % (bind_cmd)
        self._user = 'testuser'
        self._password = 'ironport'

        self._tempdir = SARF_LOCAL_TMPDIR
        self._should_preserve_server_config = should_preserve_server_config
        self._is_connected = True
        self._pending_zones_list = []

        logfile_path = os.path.join(self._tempdir, 'dnsserver.log')
        self._write_log('%s shell debug log path: %s' % (self.DAEMON_NAME_PRINTABLE,
                                                         logfile_path))

        self.shell = sal.shell.base.get_shell(hostname=self._hostname,
                                              user=self._user, password=self._password,
                                              logfile=open(logfile_path, 'w'))

        if self._should_preserve_server_config:
            self.preserve_config()

    def _write_log(self, log_str):
        print '%s :: %s' % (time.asctime(), log_str)

    @property
    def is_connected(self):
        return self._is_connected

    def start(self):
        """ don't start again if we're already running """
        if self.is_started():
            print 'other instance already running'
            return False
        self._write_log('Starting %s..' % (self.DAEMON_NAME_PRINTABLE,))
        status = self.shell.send_cmd('%s' % self._dns_cmd)
        self._write_log('Start Status %s..' % (status,))
        return True

    def stop(self):
        """ don't stop if we're already stopped """
        if not self.is_started():
            self._write_log('%s is already stopped, no action taken' % (self.DAEMON_NAME_PRINTABLE,))
            return
        self._write_log('Stopping %s...' % (self.DAEMON_NAME_PRINTABLE,))
        cmd_ps = 'ps axww | grep "named -u bind" | grep -v grep'
        cmd_ps_out = self.shell.send_cmd(cmd_ps)

        if not cmd_ps_out:
            return []  # No process to kill.
        res = []
        for line in cmd_ps_out.splitlines():
            pid = line.split()[0]
            out_kill = self.shell.send_cmd('sudo kill -p %s' % (pid))
            if not out_kill:
                self._write_log('PID:%s killed.' % (pid,))
                res.append(pid)
            else:
                self._write_log('PID:%s: no such process.' % (pid,))

        self._write_log('Stoped bind servers = %s' % (res))

    def is_started(self):
        """Is bindrunning?"""
        cmd_ps = 'ps auxwwww |grep bind |grep -v grep'
        out = self.shell.send_cmd(cmd_ps)
        if out.find('bind ') >= 0:
            return True
        else:
            return False

    def restart(self):
        """ stops and starts the bind server """
        self.stop()
        self.start()

    def reload(self):
        """ sudo rndc reload"""
        cmd_ps = 'sudo rndc reload'
        out = self.shell.send_cmd(cmd_ps)
        if out.find('successful') >= 0:
            return True
        return False

    def preserve_config(self):
        """ Backs up the named.conf file """
        cmd1 = 'sudo rm /tmp/named.conf.original'
        cmd2 = 'sudo cp /etc/namedb/named.conf /tmp/named.conf.original'
        self.shell.send_cmd(cmd1)
        self.shell.send_cmd(cmd2)

    def restore_config(self):
        """ Restores the backed up named.conf file """
        cmd = 'sudo cp /tmp/named.conf.original /etc/namedb/named.conf'
        self.shell.send_cmd(cmd)

    def is_valid_named(self):
        """ named-checkconf - named configuration file syntax checking tool  """
        cmd = "sudo named-checkconf"
        cmd1 = "echo 'status='$?"
        out = self.shell.send_cmd_list([cmd, cmd1])
        if out.find('status=0') >= 0:
            return True
        else:
            raise SyntaxError('%s' % out)

    def is_valid_named_with_zones(self):
        """ named-checkconf - named configuration file syntax checking tool  """
        cmd = "sudo named-checkconf -z"
        cmd1 = "echo 'status='$?"
        out = self.shell.send_cmd_list([cmd, cmd1])
        if out.find('status=0') >= 0:
            return True
        else:
            raise SyntaxError('%s' % out)

    def is_valid_zone(self, zonename, filename):
        """ named-checkzone - zone file validity checking or converting tool  """
        cmd = "sudo named-checkzone %s %s " % (zonename, filename)
        cmd1 = "echo 'status='$?"
        out = self.shell.send_cmd_list([cmd, cmd1])
        if out.find('status=0') >= 0:
            return True
        else:
            raise SyntaxError('%s' % out)

    def create_zone(self, domain):
        """ Creates instance of ZoneManager Class and returns """
        return ZoneManager(domain)

    def update_record(self, zone, **kwargs):
        """ Adds a record to the ZoneManager instance """
        zone.update_record(**kwargs)

    def remove_record(self, zone, **kwargs):
        """ Removes a record from ZoneManager instance """
        zone.remove_record(**kwargs)

    def build_zones(self, *args):
        """ Writes the ZoneManager instance with record details to a file """
        for zoneobj in args:
            zoneobj._zone.to_file(zoneobj._zone_db_file)

    def _get_zones_wo_duplicates(self, zone_list):
        return dict([(v.domain, v) for v in zone_list]).values()

    def update_zones(self, should_preserve_zones=True, *args):
        """ Updates named.conf with zone details and copies zones files """
        dns_headers = [
            '',
            'options {',
            '\tdirectory "/etc/namedb";',
            '',
            '};',
            '',
            'zone "." {',
            '\ttype hint;',
            '\tfile "named.root";',
            '};',
        ]

        if should_preserve_zones:
            zones_to_add = self._get_zones_wo_duplicates(list(args) + self._pending_zones_list)
        else:
            zones_to_add = self._get_zones_wo_duplicates(list(args))
        self._pending_zones_list = zones_to_add

        self._namedfile = os.path.join(self._tempdir, 'named.conf')
        print args
        with open(self._namedfile, 'wt') as fp:
            fp.write('\n'.join(dns_headers) + '\n')
            for zone in self._pending_zones_list:
                fp.write(string.Template("""zone "$domain" {\n\ttype master;\n\tfile "master/$domain.db";\n};\n\n""") \
                         .substitute(domain=zone.domain))

        # local DNS, copy files and reload DNS
        src = self._namedfile
        dst = '/tmp/named.conf'
        fq_dst = '%s@%s:%s' % (self._user, self._hostname, dst)
        status = sal.net.sshlib.scp(src, fq_dst, password=self._password)
        self.shell.send_cmd('sudo mv -f %s /etc/namedb/named.conf' % (dst,))

        for zone in self._pending_zones_list:
            src = os.path.join(self._tempdir, '%s.db' % (zone.domain,))
            dst = '/tmp/%s.db' % (zone.domain,)
            fq_dst = '%s@%s:%s' % (self._user, self._hostname, dst)
            status = sal.net.sshlib.scp(src, fq_dst, password=self._password)
            self.shell.send_cmd('sudo mv -f %s /etc/namedb/master/%s.db' % (dst, zone.domain))
            self.is_valid_zone(zone._domain, '/etc/namedb/master/%s.db' % (zone.domain,))

        self.is_valid_named_with_zones()
        self.reload()

    def disconnect(self):
        if self._should_preserve_server_config:
            self.restore_config()
        self._is_connected = False
        self.shell.close()


class ZoneManager(object):
    """ Class to managea zone """

    def __init__(self, domain):
        self._domain = domain
        self._tempdir = SARF_LOCAL_TMPDIR
        self._zone_db_file = os.path.join(self._tempdir, '%s.db' % self._domain)

        self._zone_temp_file = tempfile.NamedTemporaryFile(delete=False)
        self._rdataset = None

        self._zone = dns.zone.from_file(self._zone_temp_file, check_origin=False)

    @property
    def domain(self):
        return self._domain

    def update_record(self, **kwargs):
        """ Updates a record to the zone """
        print kwargs
        recordname = kwargs.pop('recordname')
        recordtype = kwargs.pop('recordtype')
        _rdataset = self._zone.find_rdataset(recordname, recordtype, create=True)
        if recordtype == 'SOA':
            soa_values = {
                'serial': 100,
                'refresh': 200,
                'retry': 300,
                'expire': 400,
                'minimum': 500,
            }
            soa_values.update(kwargs)
            soa_values.update({'mname': dns.name.Name(kwargs['mname'].split('.')),
                               'rname': dns.name.Name(kwargs['rname'].split('.'))
                               })
            _rdata = dns.rdtypes.ANY.SOA.SOA(dns.rdataclass.from_text("IN"), \
                                             dns.rdatatype.from_text("SOA"), **soa_values)

        if recordtype == 'A':
            a_values = {}
            a_values['address'] = kwargs['address']
            _rdata = dns.rdtypes.IN.A.A(dns.rdataclass.from_text("IN"), \
                                        dns.rdatatype.from_text("A"), **a_values)

        if recordtype == 'AAAA':
            aaaa_values = {}
            aaaa_values['address'] = kwargs['address']
            _rdata = dns.rdtypes.IN.AAAA.AAAA(dns.rdataclass.from_text("IN"), \
                                              dns.rdatatype.from_text("AAAA"), **aaaa_values)

        if recordtype == 'NS':
            ns_values = {'target': dns.name.Name(kwargs['target'].split('.'))}
            _rdata = dns.rdtypes.ANY.NS.NS(dns.rdataclass.from_text("IN"), \
                                           dns.rdatatype.from_text("NS"), **ns_values)

        if recordtype == 'CNAME':
            cname_values = {'target': dns.name.Name(kwargs['target'].split('.'))}
            _rdata = dns.rdtypes.ANY.CNAME.CNAME(dns.rdataclass.from_text("IN"), \
                                                 dns.rdatatype.from_text("CNAME"), **cname_values)

        if recordtype == 'MX':
            mx_values = {
                'preference': 1,
            }
            mx_values.update(kwargs)
            mx_values.update({'exchange': dns.name.Name(kwargs['exchange'].split('.'))})
            _rdata = dns.rdtypes.ANY.MX.MX(dns.rdataclass.from_text("IN"), \
                                           dns.rdatatype.from_text("MX"), **mx_values)

        if recordtype == 'TXT':
            txt_values = {}
            txt_values['strings'] = kwargs['strings']
            _rdata = dns.rdtypes.ANY.TXT.TXT(dns.rdataclass.from_text("IN"), \
                                             dns.rdatatype.from_text("TXT"), **txt_values)

        _rdataset.add(_rdata, ttl=600)

    def remove_record(self, **kwargs):
        """ Removes a record from zone """
        recordname = kwargs.pop('recordname')
        recordtype = kwargs.pop('recordtype')
        if self._zone.get_rdataset(recordname, recordtype) is not None:
            self._zone.delete_rdataset(recordname, recordtype)
