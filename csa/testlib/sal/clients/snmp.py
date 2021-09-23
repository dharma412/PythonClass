#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/snmp.py#2 $ $DateTime: 2019/08/21 22:26:12 $ $Author: saurgup5 $

import atexit
import fcntl
import os
import re
import socket
import subprocess
from subprocess import CalledProcessError, PIPE
import time
import warnings

import sal
import sal.time
from sal.exceptions import TimeoutError
from sal.exceptions import CalledProcessErrorStderr
from SSHLibrary import SSHLibrary

from credentials import RTESTUSER, RTESTUSER_PASSWORD


def cmd_list_to_str(args):
    assert (args)
    result_cmd = ''
    if not isinstance(args, basestring):
        for arg in map(str, args):
            if arg.find(' ') == -1:
                result_cmd += ' %s' % (arg,)
            else:
                result_cmd += ' "%s"' % (arg,)
        result_cmd = result_cmd[1:]
    else:
        result_cmd = str(args)
    return result_cmd


def run_cmd(args, should_raise_if_err=True):
    result_cmd = cmd_list_to_str(args)
    print 'Executing command "%s"...' % (result_cmd,)
    process_obj = subprocess.Popen(result_cmd, stdout=PIPE, stderr=PIPE,
                                   shell=True)
    stdout, stderr = process_obj.communicate()
    ret_code = process_obj.returncode
    if ret_code != 0 and should_raise_if_err:
        print 'stderr: ', stderr.strip()
        raise CalledProcessErrorStderr(ret_code, result_cmd, stderr.strip())
    else:
        return stdout.strip()


def non_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ''


get_hash_cmd = lambda path: \
    'python -c "import hashlib; print ' \
    'hashlib.sha256(open(\'%s\', \'rb\').read()).hexdigest()"' % (path,)

SNMP_MIBS_DIR = '/usr/share/snmp/mibs'
MIBS_ROOT = '/data/pub/configuration'
MIB_SIGNATURE = 'DEFINITIONS ::= BEGIN'


class SNMPToolsClient(object):
    SNMPWALK = 'snmpwalk'
    SNMPGET = 'snmpget'
    SNMPTRAPD = 'snmptrapd'
    SNMPTRAPD_PRINTABLE = 'snmptrapd'

    # Only one instance of snmptrapd could be
    # executed at the same time
    RUNNING_TRAP = None

    def snmpwalk(self, *args):
        cmd_args = [self.SNMPWALK] + list(args)
        return run_cmd(cmd_args)

    def snmpget(self, *args):
        cmd_args = [self.SNMPGET] + list(args)
        return run_cmd(cmd_args)

    def _run_snmptrapd(self, *args):
        basic_cmd_args = ['sudo', self.SNMPTRAPD, '-f', '-Lo']
        cmd_args = basic_cmd_args + map(str, args)
        if self.RUNNING_TRAP is not None:
            warnings.warn('The %s daemon has not been properly ' \
                          'terminated previously. Forcing restart...' % \
                          (self.SNMPTRAPD_PRINTABLE,))
            self.RUNNING_TRAP = None
        run_cmd(['sudo', 'killall', '-9', os.path.basename(self.SNMPTRAPD)],
                False)
        print 'Executing command "%s"...' % (' '.join(cmd_args),)
        self.RUNNING_TRAP = subprocess.Popen(cmd_args, stdout=PIPE, stderr=PIPE)
        self._full_trap_output = ''
        return self.RUNNING_TRAP

    def wait_for_trap(self, proc_obj, search_pattern, timeout=180,
                      should_kill_daemon=True):
        assert (bool(search_pattern))
        is_exception_happened = False
        try:
            tmr = sal.time.CountDownTimer(timeout).start()
            while tmr.is_active():
                output = non_block_read(proc_obj.stdout).strip()
                print '%s stdout: %s' % (self.SNMPTRAPD_PRINTABLE, output)
                if output:
                    if self._full_trap_output:
                        self._full_trap_output += '\n' + output
                    else:
                        self._full_trap_output += output
                    if isinstance(search_pattern, basestring):
                        matches = re.findall(search_pattern,
                                             self._full_trap_output, re.I)
                        if matches:
                            result_output = self._full_trap_output
                            self._full_trap_output = ''
                            return result_output
                    elif isinstance(search_pattern, dict):
                        are_matches_found = []
                        for pattern, count in search_pattern.iteritems():
                            count = int(count)
                            matches = re.findall(pattern,
                                                 self._full_trap_output, re.I)
                            are_matches_found.append(matches \
                                                     and len(matches) == count)
                        if all(are_matches_found):
                            result_output = self._full_trap_output
                            self._full_trap_output = ''
                            return result_output
                    else:
                        raise ValueError('search_pattern should be either string ' \
                                         'or dict instance. But given %s' % \
                                         (type(search_pattern),))
                time.sleep(2)
            else:
                raise TimeoutError('Failed to get the "%s" pattern(s) ' \
                                   'from %s output within %d seconds timeout. ' \
                                   'Full daemon output:\n%s' % \
                                   (search_pattern, self.SNMPTRAPD_PRINTABLE, timeout,
                                    self._full_trap_output))
        except Exception as e:
            is_exception_happened = True
            raise e
        finally:
            if should_kill_daemon or is_exception_happened:
                run_cmd(['sudo', 'killall', '-9', os.path.basename(self.SNMPTRAPD)])
                self.RUNNING_TRAP = None

    def snmptrapd_async(self, *args):
        return self._run_snmptrapd(*args)

    def snmptrapd_sync(self, search_pattern, timeout=180, *args):
        proc_obj = self._run_snmptrapd(*args)
        self.wait_for_trap(proc_obj, search_pattern, timeout)

    def load_mibs_from_dut(self, src_dut, dst_dir=SNMP_MIBS_DIR):
        shell = SSHLibrary()
        shell.open_connection(host=src_dut,
                              timeout=25,
                              prompt=']')
        try:
            shell.login(RTESTUSER, RTESTUSER_PASSWORD)
            grep_cmd = 'grep -R "%s" "%s" | awk \'BEGIN { FS=":" }; { print $1 }\'' % \
                       (MIB_SIGNATURE, MIBS_ROOT)
            mib_paths = shell.execute_command(grep_cmd).splitlines()
            copied_mibs = []
            for src_path in mib_paths:
                dst_path = os.path.join(dst_dir, os.path.basename(src_path))
                if os.path.exists(dst_path):
                    remote_mib_digest = shell.execute_command(get_hash_cmd(src_path))
                    local_mib_digest = run_cmd(get_hash_cmd(dst_path))
                    if remote_mib_digest.strip() == local_mib_digest.strip():
                        print 'Hashes are equal. The MIB file already exists locally. ' \
                              'Skipping copy.'
                        continue
                host_ip = socket.gethostbyname(socket.gethostname())
                scp_cmd = 'scp "%s" %s@%s:%s' % (src_path, RTESTUSER,
                                                 host_ip, dst_dir)
                shell.write(text=scp_cmd)
                try:
                    shell.read_until(expected='Are you sure you want to continue ' \
                                              'connecting (yes/no)?')
                    shell.write(text='yes')
                    shell.read_until(expected='Password:')
                except:
                    pass
                shell.write(text=RTESTUSER_PASSWORD)
                shell.read_until_prompt()
                run_cmd(['sudo', 'chmod', '444',
                         os.path.join(dst_dir, os.path.basename(src_path))])
                copied_mibs.append(os.path.basename(src_path))
            return copied_mibs
        finally:
            shell.close_connection()

    def load_mibs_from_files(self, dst_dir=SNMP_MIBS_DIR, *src_paths):
        copied_mibs = []
        for src_path in src_paths:
            if os.path.isfile(src_path):
                dst_path = os.path.join(dst_dir, os.path.basename(src_path))
                if os.path.exists(dst_path):
                    other_mib_digest = run_cmd(get_hash_cmd(src_path))
                    local_mib_digest = run_cmd(get_hash_cmd(dst_path))
                    if other_mib_digest.strip() == local_mib_digest.strip():
                        print 'Hashes are equal. The MIB file already exists locally. ' \
                              'Skipping copy.'
                        continue
                run_cmd(['sudo', 'cp', '-f', src_path, dst_dir])
                run_cmd(['sudo', 'chmod', '444',
                         os.path.join(dst_dir, os.path.basename(src_path))])
                copied_mibs.append(os.path.basename(src_path))
            else:
                raise ValueError('The %s is not valid file path' % (src_path,))
        return copied_mibs


@atexit.register
def terminate_async_trap():
    if SNMPToolsClient.RUNNING_TRAP is not None:
        run_cmd(['sudo', 'killall', '-9', os.path.basename(SNMPToolsClient.SNMPTRAPD)])


if __name__ == '__main__':
    client = SNMPToolsClient()
    DEST_HOST = 'vm10esa0029.qa'

    print client.snmpwalk('-v3', '-c', 'ironport', '-mALL',
                          '-l', 'authNoPriv', '-A', 'ironport',
                          '-u', 'v3get', DEST_HOST, 'ASYNCOS-MAIL-MIB::keyExpirationTable')

    try:
        client.snmptrapd_sync('aaa', timeout=10)
    except TimeoutError as e:
        print e
    process = client.snmptrapd_async()
    try:
        client.wait_for_trap(process, 'coldStart', timeout=10)
    except TimeoutError as e:
        print e
    client.load_mibs_from_dut(DEST_HOST)
