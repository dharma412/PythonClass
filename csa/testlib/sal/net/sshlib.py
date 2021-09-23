#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/sal/net/sshlib.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""Wrapper for the ssh program. Provides get_ssh, ssh_command, scp functions."""
from __future__ import absolute_import
from __future__ import with_statement

import os
import tempfile
import time
import stat
import sal.deprecated.proctools
from sal.exceptions import TimeoutError
import sal.irontools
from sal.deprecated import expect
import re
import warnings
import socket

#: Reference Symbols: sshlib

root_users = ['root', 'riaf', 'rtestuser']
debug = os.environ.has_key('DEBUG_SSHLIB') and os.environ['DEBUG_SSHLIB']

authorized_keys = os.environ['HOME'] + '/.ssh/authorized_keys'


class sshKeyFile(object):
    """Object to manage the iaf ssh key.  Lazily creates key file as
    needed.
    """
    iaf_dsa_key = """-----BEGIN DSA PRIVATE KEY-----
MIIBvAIBAAKBgQCpTJeG3gX/yQ+BebDcptJeSw0TFoR4R+6CsiT1s70ovw41Seh1
kJ4T6d2qtgjkbaXesjvLRMVw0ceVQcyNrJQQovqyGkOrFq+CHv2gK/xXV8nGz3Xi
scB2sEK+XrKnlm9Ps+fcA80jm5QMeEdSXxNh3S3ET8fRoRox8eeU/qmVbQIVAO40
LLDKXp/ntZrjz5hfYqTzp3DVAoGAeL6XmFTmfuk/aIV7iWo0UPHcYCA+NHL8Rp89
43tmPRDu32PILRWovJqI4odjG5G7en3aUvplhAyCEAIyzYu+Yofzjc/Dnwc75FM5
wHB40Ux61u7Uid17ZKcdNnXU/2w0ESyI+f1fP72PVrLn/pe4f+y781wmTqNSACC5
6aICtYICgYEAket7Jq8HFSyp3NTlZdQNeOB0K46VK7X1I8YzHfdILeAoXxNqFWEv
hB50iHw1390ETx3J9luGHtOze9JeAFr+m2HrkltfTwvUwyxbjX0yAHsXWvQ5xwXh
pV0nm1hOhxHg60/5QfXu75ZKhEAz/ZWKkteK0na+mWbFAnKMUG04TwICFQDBBo4x
Yih1ylEfDBiCCGAL9ICWzQ==
-----END DSA PRIVATE KEY-----
"""

    pub_iaf_dsa_key = """ssh-dss AAAAB3NzaC1kc3MAAACBAKlMl4beBf/JD4F5sNym0l5LDRMWhHhH7oKyJPWzvSi/DjVJ6HWQnhPp3aq2CORtpd6yO8tExXDRx5VBzI2slBCi+rIaQ6sWr4Ie/aAr/FdXycbPdeKxwHawQr5esqeWb0+z59wDzSOblAx4R1JfE2HdLcRPx9GhGjHx55T+qZVtAAAAFQDuNCywyl6f57Wa48+YX2Kk86dw1QAAAIB4vpeYVOZ+6T9ohXuJajRQ8dxgID40cvxGnz3je2Y9EO7fY8gtFai8mojih2Mbkbt6fdpS+mWEDIIQAjLNi75ih/ONz8OfBzvkUznAcHjRTHrW7tSJ3Xtkpx02ddT/bDQRLIj5/V8/vY9Wsuf+l7h/7LvzXCZOo1IAILnpogK1ggAAAIEAket7Jq8HFSyp3NTlZdQNeOB0K46VK7X1I8YzHfdILeAoXxNqFWEvhB50iHw1390ETx3J9luGHtOze9JeAFr+m2HrkltfTwvUwyxbjX0yAHsXWvQ5xwXhpV0nm1hOhxHg60/5QfXu75ZKhEAz/ZWKkteK0na+mWbFAnKMUG04TwI= iaf@vampire.eng"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.ssh_dir = os.path.join(self.base_dir, '.ssh')
        self.key_path = os.path.join(self.ssh_dir, 'iaf_dsa')
        self.public_key_path = os.path.join(self.ssh_dir, 'iaf_dsa.pub')

    def key_already_exists(self):
        """Check if the private ssh key file already exists.

        Does not check contents of key file.
        """
        return os.path.exists(self.key_path)

    def public_key_already_exists(self):
        """Check if the public ssh key file already exists.

        Does not check contents of key file.
        """
        return os.path.exists(self.public_key_path)

    def ensure_ssh_dir_exists(self):
        "Create the .ssh directory if it doesn't already exist."
        if not os.path.exists(self.ssh_dir):
            os.mkdir(self.ssh_dir)

    def ensure_correct_permissions(self):
        """Ensure key permissions are set to 0600, as required by ssh.
        """
        perms = os.stat(self.key_path)
        if oct(perms.st_mode & 0777) != '0600':
            os.chmod(self.key_path, 0600)

    @property
    def public_key(self):
        """If it doesn't already exist, create a local copy of IAF
        public key and return the path.
        """
        if not self.public_key_already_exists():
            print "Creating local copy of iaf_dsa public key"
            self.ensure_ssh_dir_exists()

            with open(self.public_key_path, 'w') as fh:
                fh.write(self.pub_iaf_dsa_key)

        return self.public_key_path

    @property
    def path(self):
        """If it doesn't already exist, create a local copy of IAF private
        key, chmod to 600, and return the path.
        """
        if not self.key_already_exists():
            # TODO: log instead of print
            print "Creating local copy of iaf_dsa private key"
            self.ensure_ssh_dir_exists()

            with open(self.key_path, 'w') as fh:
                fh.write(self.iaf_dsa_key)

        self.ensure_correct_permissions()
        return self.key_path


iaf_key = sshKeyFile(os.getenv('HOME'))


class SshRetry(RuntimeError): pass


class SshExpect(expect.Expect):
    # NOTE: new host messages can be restricted.
    def login(self, password=None, reset_password=False):
        e = ""
        if not password:
            # TODO: We still need to handle changed ssh key and new host
            #       messages.
            return  # do nothing

        # % is for case when password is specified but ssh is
        # unchallenged (sometimes this happens with testuser/ironport)
        #    adding # as well, for rtestuser i.e. root
        # TODO: Don't look for hard coded prompt

        self.expect(['ssword:', 'WARNING:', '%', 'authenticity of host', '#', 'Password for'],
                                                                    timeout=60)
        if self.expectindex == 0 or self.expectindex == 5:
            self.writeln(password)
            if reset_password:
                # Use the keyword Reset Passphrase On Expiry Reminder From Cli to handle this case
                self.expect(['change your password now', 'Old Password:', 'Last login'], timeout=60)
                if self.expectindex == 0:
                    print "GOT the password expiry reminder banner message and changing the password now"
                    # Handle the password expiry reminder banner message
                    self.writeline('Y')
                    if self.expect(['Old Password:'], timeout=60):
                        print "sent Y and entered old password"
                        self.writeline(password)
                        if self.expect(['New Password:'], timeout=60):
                            self.writeln(password)
                        if self.expect(['Retype New Password:'], timeout=60):
                            self.writeln(password)
                        if self.expect(['Last login'], timeout=60):
                            self.writeln(password)
                # Use the keyword Reset Expired Passphrase From Cli to handle this case
                elif self.expectindex == 1:
                    print "entered old password"
                    self.writeline(password)
                    if self.expect(['New Password:'], timeout=60):
                        self.writeln(password)
                    if self.expect(['Retype New Password:'], timeout=60):
                        self.writeln(password)
                    if self.expect(['Last login'], timeout=60):
                        print "Password changed successfully"
                elif self.expectindex == 2:
                    print "Passphrase not expired, Successfully logged in to CLI"
                    pass
            else:
                try:
                    self.expect(['change your password now', 'Last login', 'Welcome'], timeout=60)
                    if self.expectindex == 0:
                        print "GOT the alert banner message and not changing the password now"
                        self.writeline('N')
                        self.writeline(password)
                        if self.expect(['Last login'], timeout=60):
                            print "Login happened successfully without passphrase reset"
                    elif self.expectindex == 1:
                        print "Successfully logged in to CLI"
                except Exception as e:
                    # Added as part of fix to ESA code breakage
                    print ("Got exception : %s" % str(e))
                    pass
        elif self.expectindex == 1:
            raise SshRetry, 'SshExpect.login: try again, bad host key.'
        elif self.expectindex == 3:
            # Handle this case by always answering 'yes':
            # The authenticity of host 'qa64.qa (172.17.0.164)' can't be established.
            # DSA key fingerprint is 3d:ef:d4:56:ba:20:f5:e3:d5:41:09:16:b6:b2:2e:f9.
            # Are you sure you want to continue connecting (yes/no)? ^C
            self.writeln('yes')
            # try to login again
            self.login(password)
        # else do nothing (the '%' and '#' case
        # EXCEPTION if raised is returned.
        if e: return e


def get_ssh_safe(host, user=None, password=None, prompt=None, cmd='',
                 logfile=None, extraoptions='', devmode=False, force_prompt=None,
                 inet_mode=socket.AF_INET, reset_password=False):
    """
       inet_mode forces ssh to use ipv4 address if the value passed is socket.AF_INET.
       and it forces ssh to use ipv6 address if the value passed is socket.AF_INET6.
       Returns an SshExpect object.
    """

    address_family = {socket.AF_INET6: 6, socket.AF_INET: 4}

    # force dev mode to false if IAF2_DEVMODE not set
    if not os.environ.get('IAF2_DEVMODE'):
        devmode = False

    if user == 'riaf':
        warnings.warn("********Please try to use \'rtestuser\' instead of " \
                      "\'riaf\' user********", DeprecationWarning)

    if user in root_users:
        extraoptions += ' -i ' + iaf_key.path
        if not force_prompt:
            password = None
            prompt = force_prompt = sal.irontools.get_sh_root_prompt()

    pm = sal.deprecated.proctools.get_procmanager()
    if user:
        host = user + '@' + host

    if devmode == False:
        # command = 'ssh %s %s %s' % (extraoptions, host, cmd)
        # -t causes problems on OS X I think ##TODO:mikew
        command = 'ssh -%d -q -t -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no %s %s %s' \
                  % (address_family[inet_mode], extraoptions, host, cmd)
    else:
        # if we're on in "dev mode", start up a CLI in a regular shell
        # IPROOT must be set properly for this to work
        command = 'sh -c "cd %s/%s/cli && exec %s/bin/python cli.py"' \
                  % (os.environ['IPROOT'], os.environ['IPPROD'], os.environ['IPDATA'])

    if debug:
        print 'get_ssh_safe():command(', command, ')'
    sshproc = pm.spawnpty(command, logfile=logfile)
    ssh = SshExpect(sshproc)

    # no login required on a dev box,
    # instead wait for a CLI prompt at this point
    if devmode == False and password is not None:
        ssh.login(password, reset_password)

    ssh.set_prompt(prompt or '$')
    if force_prompt:
        if not cmd:
            ssh.set_prompt(expect.RegexUserMatch(
                re.compile('(^%s|\^C%s)' % \
                           (force_prompt, force_prompt), re.MULTILINE)))
            saved_exception = None
            for _ in xrange(2):
                # This may fail to set prompt for the first time because of
                # race conditions
                try:
                    ssh.writeln('env PS1=\"%s\" sh' % force_prompt)
                    ssh.wait_for_prompt(timeout=20)
                    break
                except TimeoutError as e:
                    saved_exception = e
            else:
                raise saved_exception

    return ssh


def get_ssh(host, user=None, password=None, prompt=None, cmd='',
            logfile=None, extraoptions='', devmode=False,
            force_prompt=None, inet_mode=socket.AF_INET,
            reset_password=False):
    """removes stale known_hosts entry, if required."""
    try:
        return get_ssh_safe(host, user, password, prompt, cmd,
                            logfile, extraoptions, devmode, force_prompt, inet_mode,
                            reset_password)

    except SshRetry:
        remove_known_host(host)
        return get_ssh_safe(host, user, password, prompt, cmd,
                            logfile, extraoptions, devmode, force_prompt, inet_mode,
                            reset_password)


get_ssh_unsafe = get_ssh  # alias


def scp(src, dst='.', password=None, extraopts='', logfile=None,
        inet_mode=socket.AF_INET):
    """
       Specify src, dst args like they're specified on the scp command line
       inet_mode forces scp to use ipv4 address if the value passed is socket.AF_INET.
       and forces scp to use ipv6 address if the value passed is socket.AF_INET6.
    """
    address_family = {socket.AF_INET6: 6, socket.AF_INET: 4}

    for user_at in [user + '@' for user in root_users]:
        if src.find(user_at) == 0 or dst.find(user_at) == 0:
            extraopts += ' -i ' + iaf_key.path
            break
    if src.find('riaf@') == 0 or dst.find('riaf@') == 0:
        warnings.warn("********Please try to use \'rtestuser\' instead of " \
                      "\'riaf\' user ********", DeprecationWarning)

    # Do recursive copy if src is a directory
    if os.path.isdir(src):
        extraopts += ' -r '
    cmd = 'scp -%d -q -o StrictHostKeyChecking=no %s %s %s' % (address_family[inet_mode], extraopts, src, dst)
    if debug:
        print 'scp():cmd(', cmd, ')'
    scp = sal.deprecated.proctools.spawnpty(cmd, logfile=logfile)

    # TODO: proctools throws a traceback if no password is specified
    # so we'll leave this if statement in for now.
    if password:
        SshExpect(scp).login(password)
        time.sleep(0.3)
    # On error, FreeBSD won't allow process to exit until buffer empty.
    scp.read()
    scp.close()
    return scp.exitstatus  # user can check exit status for success


def scp_remote_to_remote(src, dst, src_passwd=None, dst_passwd=None,
                         src_extraopts='', dst_extraopts='', inet_mode=socket.AF_INET):
    """Copy files from one remote machine to another via localhost"""
    tmp_file = tempfile.mkstemp()[1]

    for source, destination, password, extraopts in \
            ((src, tmp_file, src_passwd, src_extraopts),
             (tmp_file, dst, dst_passwd, dst_extraopts)):
        exitstatus = scp(source, destination, password, extraopts, inet_mode)
        if exitstatus.exitstatus != 0:
            break

    os.system('rm -f %s' % (tmp_file,))
    return exitstatus


def ssh_command(host, user=None, password=None, prompt=None, command='',
                logfile=None, devmode=False, force_prompt=None, inet_mode=socket.AF_INET):
    ssh = get_ssh(host, user=user, password=password, prompt=prompt,
                  cmd=command, logfile=logfile, extraoptions='', devmode=devmode,
                  force_prompt=None, inet_mode=inet_mode)
    rv = ssh.read()
    ssh.close()
    return rv


def remove_known_host(hostname):
    """removing hostname entry from the known_hosts file. """
    # read known_hosts
    fname = os.environ['HOME'] + '/.ssh/known_hosts'
    lines = file(fname).readlines()

    # remove hostname entries
    new = []
    for line in lines:
        if not line.startswith(hostname):
            new.append(line)

    # write file
    if len(new) < len(lines):
        file(fname, 'w').writelines(new)


def append_key_to_auth_keys(key, auth_key_file=authorized_keys):
    """Add key to authorized keys file.

    :Parameters:
        - `key`: key to be added.
        - `auth_key_file`: path to authorized keys file.
    """
    try:
        auth_keys_file = open(auth_key_file, 'a')
        auth_keys_file.write('\n' + key)
    finally:
        auth_keys_file.close()


def backup_auth_keys_file(auth_key_file=authorized_keys):
    """Backup authorized keys.

    :Parameters:
        - `auth_key_file`: path to authorized keys file to be backed up.

    :Return:
        Path to backup file on success, None in case of failure.
    """
    backup_file = tempfile.mkstemp()[1]
    if not os.system('cp %s %s' % (auth_key_file, backup_file)):
        return backup_file


def restore_auth_keys_file(backup_file, auth_key_file=authorized_keys):
    """Restore authorized keys file from backup.

    :Parameters:
        - `backup file`: path to backup file.
        - `auth_key_file`: path to keys file that must be restored.

    :Return:
        Zero value on success, non-zero otherwise.
    """
    for cmd in ('cp %s %s' % (backup_file, auth_key_file),
                'rm %s' % (backup_file,)):
        ret_val = os.system(cmd)

        if not ret_val:
            return ret_val

    return ret_val
