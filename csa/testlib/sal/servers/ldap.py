#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/servers/ldap.py#1 $ $DataTime: $ $Author: aminath $

# : Reference Symbols: ldapserver, ldapclient

"""
ldapclient.py
    This module provides an API
        1. to add, delete, get entries under
          the dn: 'ou=Bingo, ou=mfc, dc=qa' in the openldap.qa ldap server.

        2. start/stop the ldap server

    This module contains an Ldap Client class and and Ldap Server class
    (for openldap and Wins AD servers).


   NOTES:
   The EUQ GUI will search the ldap store for authentication
   information when a user attempts to login.

    Example EUQ /usr/godspeed/config/euq.access/data.cfg on the MGA:
        server = (1,0,"","","172.17.0.204")
        method = (1,0,"","","ldap")
        port = (1,0,"","",389)

        ldap_server_type = (1,0,"","","openldap")
        ldap_credentials = (1,0,"","",("password",{"password":"ironport","user":"uid=adm in,ou=people,ou=corporate,dc=qa"}))
        ldap_query_base = (1,0,"","","dc=qa")
        ldap_uid_attr = (1,0,"","","uid")
        ldap_query_filter = (1,0,"","","(uid={u})")
        ldap_email_attr = (1,0,"","","mail")
        ldap_alias_email_attr = (1,0,"","","mailAlternateAddress")
        ldap_wins_name = (1,0,"","","__NOTSET__")
        transport = (1,0,"","","PLAINTEXT")
        default_domain = (1,0,"","","")

    Example LDIF file to add a user to ldap:
        #---------------------------------------------------------------------
        # This file has been generated on 05.23.2005 at 14:49 from sully.qa:389
        # by Softerra LDAP Browser 2.6 (http://www.ldapbrowser.com)
        #---------------------------------------------------------------------
        version: 1
        dn: uid=bingo_mikew2, ou=Bingo, ou=mfc, dc=qa
        objectClass: person
        objectClass: account
        objectClass: inetorgperson
        objectClass: mailrecipient
        sn: Surname is Wakabayashi
        cn: Common Name is Mike Wakabayashi
        uid: bingo_mikew2
        userPassword: bingo_mikew2
        mail: bingo_mikew2mail@qa19.qa
        mailAlternateAddress: bingo_mikew2a1
        mailAlternateAddress: bingo_mikew2a2@qa19.qa
        mailAlternateAddress: bingo_mikew2a3@qa19.qa
        mailAlternateAddress: bingo_mikew2a4@qa19.qa
        mailAlternateAddress: bingo_mikew2a5@qa19.qa
"""
from __future__ import absolute_import

from sal.exceptions import ConfigError
import ldap
import ldap.modlist
import socket
import os
import re

# for managing the server process
import sal.shell.base
import sal.net.sshlib

from common.util.ordered_dict import chunks

# Constants --------------------
debug = True
uid_index = 0  # : Current available uid index (see gen_uid)
gcn_index = 0  # : Current available group's cn index (see gen_group_cn)


# Utility Functions --------------------
def to_list(string_or_list):
    if isinstance(string_or_list, basestring):
        if string_or_list.find(',') >= 0:
            return map(lambda x: str(x.strip()), string_or_list.split(','))
        else:
            return str(string_or_list)
    else:
        return string_or_list


## Server Classes --------------------
class BaseLdapServer:
    def __init__(self, hostname):
        self._hostname = hostname

    def start(self):
        """Virtual method. Define in derived class."""
        pass

    def stop(self):
        """Virtual method. Define in derived class."""
        pass

    def restart(self):
        """Virtual method. Define in derived class."""
        pass

    def is_started(self):
        """Virtual method. Define in derived class."""
        pass

    def set_ldap_options(self, ldap_enable, ldaps_enable,
                         ldap_address, ldaps_address,
                         ldap_port, ldaps_port):
        """Virtual method. Define in derived class."""
        pass


class OpenLdapServer(BaseLdapServer):
    def __init__(self, hostname, deamon_script='/usr/local/etc/rc.d/slapd'):
        BaseLdapServer.__init__(self, hostname)
        self._rc_cmd = 'sudo %s' % (deamon_script,)
        self._user = 'testuser'
        self._password = 'ironport'
        self._tempdir = '/tmp'

        # args to set_ldap_options
        self.ldap_enable = True
        self.ldap_address = '0.0.0.0'
        self.ldap_port = 389
        self.tls_enable = True
        self.anon_enable = True
        self.ldaps_enable = False
        self.ldaps_address = '0.0.0.0'
        self.ldaps_port = 636
        self.save_old_local = True

        logfile_name = '/tmp/ldapserver.log'
        try:
            logfile = open(logfile_name, 'w')
            os.chmod(logfile_name, 0666)
        except OSError, e:  # failure probably from 'chmod permission denied'
            try:
                os.unlink(logfile_name)
            except:
                pass

        self.shell = sal.shell.base.get_shell(hostname=hostname,
                                              user=self._user, password=self._password,
                                              logfile=logfile)

    def __str__(self):
        s = 'Server Name(%s)\n' % (self._hostname)
        s += 'ldap (enable:%s,address:%s,port:%d)\n' \
             % (self.ldap_enable, self.ldap_address, self.ldap_port)
        s += 'ldaps(enable:%s,address:%s,port:%d)\n' \
             % (self.ldaps_enable, self.ldaps_address, self.ldaps_port)
        s += 'save_old_local:' + str(self.save_old_local)
        return s

    def start(self):
        # don't start again if we're already running
        if self.is_started():
            print 'other instance already running'
            return False
        print 'Starting slapd...'
        status = self.shell.send_cmd('%s start' % self._rc_cmd)
        print 'Start Status = %s' % (status,)
        return True

    def stop(self):
        # don't stop if we're already stopped
        if not self.is_started():
            print('slapd is already stopped, no action taken')
            return
        print('Stopping slapd...')
        status = self.shell.send_cmd('%s stop' % self._rc_cmd)
        print 'Stoping Status = %s' % (status,)

    def restart(self):
        # we can restart whether slapd is running or not
        print('Restarting slapd...')
        status = self.shell.send_cmd('%s restart' % self._rc_cmd)
        print "Restart Status = %s" % (status,)

    def is_started(self):
        """Is slapd running?"""
        # enter as self.user and see if slapd is running
        cmd_ps = 'ps auxwwww |grep slapd |grep -v grep'
        out = self.shell.send_cmd(cmd_ps)
        if out.find('ldap ') >= 0:  # slapd is run by user 'ldap'
            return True
        else:
            return False

    def upload_rc_local_and_restart(self, local_file=None):
        """
        Upload a file to the ldap server to serve as rc.conf.local,
        move it to /etc/rc.conf.local with sudo and restart the server.
        """

        print('Setting new options for slapd...')
        dst1 = '~/rc.conf.local'
        src = local_file or '%s/rc.conf.local.new' % self._tempdir
        dst = '%s@%s:%s' % (self._user, self._hostname, dst1)
        status = sal.net.sshlib.scp(src, dst, password=self._password)
        self.shell.send_cmd('sudo mv %s /etc/rc.conf.local' % dst1)

        # restart
        self.restart()

        print('New options set.')

    def restore_rc_local(self):
        """restore rc.conf.local on the ldap host and restart"""
        print('Restoring original slapd configuration...')
        rc_local = '%s/rc.conf.local' % self._tempdir
        if os.path.exists(rc_local):
            self.upload_rc_local_and_restart(rc_local)
            os.system('sudo rm %s' % rc_local)
        else:
            # just remove the file we uploaded instead
            self.shell.send_cmd('sudo rm /etc/rc.conf.local')

        print('Configuration restored.')
        self.restart()

    def set_ldap_options(self, ldap_enable=None, ldaps_enable=None,
                         tls_enable=None, anon_enable=None,
                         ldap_address=None, ldaps_address=None,
                         ldap_port=None, ldaps_port=None,
                         save_old_local=None):
        """
        Options such as secure/non-secure, address, and port must be set
        in the flags passed to slapd at startup.  So we create an
        rc.conf.local file with just the slapd_flags variable included
        and copy it over to /etc on the ldap server after saving whatever
        rc.conf.local file is there already.

        Currently no other flags are written out.  It would be good hygiene
        to restore the old rc.conf.local settings after you're done messing
        with things by using the restore_rc_local function.
        """

        # If arg is not-None save value for later use
        # If arg is None use the last stored value
        if ldap_enable != None:
            self.ldap_enable = ldap_enable
        if ldaps_enable != None:
            self.ldaps_enable = ldaps_enable
        if tls_enable != None:
            self.tls_enable = tls_enable
        if anon_enable != None:
            self.anon_enable = anon_enable
        if save_old_local != None:
            self.save_old_local = save_old_local
        self.ldap_address = ldap_address or self.ldap_address
        self.ldap_port = ldap_port or self.ldap_port
        self.ldaps_address = ldaps_address or self.ldaps_address
        self.ldaps_port = ldaps_port or self.ldaps_port

        hosts = ''
        if self.save_old_local:
            # copy rc.conf.local from ldap server to QA system if it's there
            src = '/etc/rc.conf.local'
            src = '%s@%s:%s' % (self._user, self._hostname, src)
            status = sal.net.sshlib.scp(src, self._tempdir, password=self._password)

        if (not self.ldap_enable) and (not self.ldaps_enable):
            raise ValueError, "Error: you must enable at least one protocol!"

        if self.ldap_enable:
            hosts = 'ldap://%s:%d/' % (self.ldap_address, int(self.ldap_port))

        if self.ldaps_enable:
            # add to plain ldap setting if you're using regular ldap as well
            if self.ldap_enable:
                hosts += ' ldaps://%s:%d/' % (self.ldaps_address,
                                              int(self.ldaps_port))
            else:
                hosts = 'ldaps://%s:%d/' % (self.ldaps_address,
                                            int(self.ldaps_port))

        # upload correct slapd.conf to ldap server
        dst1 = '~/slapd.conf'
        src = '%s/tests/testdata/openldap/slapd.conf' % os.environ['SARF_HOME']
        # use config without certs if tls & ssl should be disabled
        if (not self.tls_enable) and (not self.ldaps_enable):
            src += '.notls'

        # rewrite config without anonymous binding for userpassword if req
        if not self.anon_enable:
            inf = open(src, 'r')
            contents = inf.read()
            inf.close()
            contents = re.sub(r'(by\sself\swrite\n)\s+by\sanonymous\sread\n\s+by\s\*\sread',
                              '\\1        by users read\n        by anonymous auth', contents, re.S)
            src = '%s/slapd.conf' % self._tempdir
            of = open(src, 'w')
            of.write(contents)
            of.close()

        dst = '%s@%s:%s' % (self._user, self._hostname, dst1)
        status = sal.net.sshlib.scp(src, dst, password=self._password)
        self.shell.send_cmd('sudo mv %s /usr/local/etc/openldap' % dst1)

        # write the hosts string out to a file, then call
        # upload_rc_local_and_restart
        # to move it to the ldap server and restart it
        outfile = '%s/rc.conf.local.new' % self._tempdir
        of = open(outfile, 'w')
        of.write('slapd_flags=\'-h "%s"\'\n' % hosts)
        of.close()

        self.upload_rc_local_and_restart()
        os.system('sudo rm %s' % outfile)


# # NOTE: ActiveDirectory Ldap Server cannot be controlled remotely.
# class AdLdapServer(BaseLdapServer):
#    def __init__(self, hostname, port=None):
#        BaseLdapServer.__init__(self, hostname, port)
#    def start(self):
#        pass
#    def stop(self):
#        pass
#    def restart(self):
#        pass
#    def is_started(self):
#        pass
#    def set_ldap_options(self, ldap_enable=None, ldaps_enable=None,
#                               tls_enable=None,
#                               ldap_address=None, ldaps_address=None,
#                               ldap_port=None, ldaps_port=None):
#        pass

## Client Classes --------------------

MODOPS_FLAG = 'MODOPS'
SEPARATOR_FLAG = 'SEPARATOR'
DEFAULT_SEPARATOR = ','
ID_AUTOGEN_FLAG = 'AUTO'


class OpenLdapClient:
    def __init__(self, host, port=None, binddn=None,
                 password=None, basedn=None, do_connect=True):
        self._host = host
        self._port = port or 389
        self._binddn = binddn or 'uid=rblaes,ou=people,ou=corporate,dc=qa'
        self._password = password or 'rblaes'
        self._basedn = basedn or 'ou=testdata, dc=qa'

        if do_connect:
            self.connect()

    def connect(self):
        # open ldap connection
        self._ldap = ldap.open(self._host, int(self._port))
        self._ldap.simple_bind_s(self._binddn, self._password)
        return self

    def disconnect(self):
        # close ldap connection
        self._ldap.unbind()

    def _parse_mod_op_str(self, mod_op_str):
        OPS_MAPPING = {'ADD': ldap.MOD_ADD,
                       'DELETE': ldap.MOD_DELETE,
                       'REPLACE': ldap.MOD_REPLACE}
        return OPS_MAPPING[mod_op_str.upper()]

    def _parse_modlist_str(self, multiplier, separator, args_list):
        assert (multiplier in (2, 3))
        result = []
        if len(args_list) % multiplier != 0:
            raise ValueError('Arguments list count should be a multiple of %d. ' \
                             'Current argumnets count is %d.' % (multiplier,
                                                                 len(args_list)))
        if len(args_list) < multiplier:
            raise ValueError('Arguments list count should be not less then %d. ' \
                             'Current argumnets count is %d.' % (multiplier,
                                                                 len(args_list)))
        for chunk in chunks(args_list, multiplier):
            mod_op = None
            attr_name = None
            attr_value = None
            if multiplier == 3:
                mod_op, attr_name, attr_value = tuple(chunk)
                mod_op = self._parse_mod_op_str(mod_op)
                if attr_value.upper() == ID_AUTOGEN_FLAG:
                    attr_value = self.gen_group_gid()
                else:
                    attr_value = map(lambda x: x.strip(), attr_value.split(separator))
                result.append((mod_op, attr_name, attr_value))
            else:
                attr_name, attr_value = tuple(chunk)
                if attr_value.upper() == ID_AUTOGEN_FLAG:
                    attr_value = self.gen_group_gid()
                else:
                    attr_value = map(lambda x: x.strip(), attr_value.split(separator))
                result.append((attr_name, attr_value))
        return result

    def create_modlist(self, *args):
        has_mod_ops = bool(filter(lambda x: x == MODOPS_FLAG, args))
        separator = filter(lambda x: x.find(SEPARATOR_FLAG) == 0, args)
        if separator:
            separator = separator[0].split('=')[-1].strip()
        else:
            separator = DEFAULT_SEPARATOR
        if has_mod_ops or separator != DEFAULT_SEPARATOR:
            args_for_process = filter(
                lambda x: x.find(SEPARATOR_FLAG) != 0 and x != MODOPS_FLAG, args)
        else:
            args_for_process = args
        if has_mod_ops:
            return self._parse_modlist_str(3, separator, args_for_process)
        else:
            return self._parse_modlist_str(2, separator, args_for_process)

    def add_custom_entry(self, dn, modlist):
        self._ldap.add_s(dn, modlist)

    def modify_custom_entry(self, dn, modlist):
        self._ldap.modify_s(dn, modlist)

    def search_custom_entries(self, base, scope, filterstr, timeout=60):
        SCOPE_MAPPING = {'BASE': ldap.SCOPE_BASE,
                         'ONELEVEL': ldap.SCOPE_ONELEVEL,
                         'SUBTREE': ldap.SCOPE_SUBTREE}
        return self._ldap.search_st(base,
                                    SCOPE_MAPPING[scope.upper()],
                                    filterstr,
                                    timeout=timeout)

    def delete_custom_entry(self, dn):
        self._ldap.delete_s(dn)

    def add_user(self, uid, password, mail=None, mail_alternate_address=None,
                 mail_local_address=None, mail_routing_address=None, basedn=None, **kwargs):
        # build modlist

        entry = {}
        # For backward compatibility of the keyword
        if not kwargs.has_key('objectclass'):
            entry['objectClass'] = ['person', 'account', 'inetorgperson', \
                                    'mailrecipient', 'inetlocalmailrecipient']
        else:
            entry['objectClass'] = kwargs['objectclass'].lower().split(',')

        if any(kwargs):
            if kwargs.get('posixAccount', None):
                entry['objectClass'].append('posixAccount')
                entry['uidNumber'] = kwargs.get('uidNumber', self.gen_group_gid())
                entry['gidNumber'] = kwargs.get('gidNumber', self.gen_group_gid())
                entry['homeDirectory'] = kwargs.get('homeDirectory', '/home/%s' % uid)
        if mail:
            entry['mail'] = to_list(mail)
            entry['mailHost'] = to_list(mail.split('@')[1])
        if mail_alternate_address != None:
            entry['mailAlternateAddress'] = to_list(mail_alternate_address)
        if mail_local_address is not None:
            entry['mailLocalAddress'] = to_list(mail_local_address)
        if mail_routing_address is not None:
            entry['mailRoutingAddress'] = to_list(mail_routing_address)
        entry['uid'] = to_list(uid)
        if 'person' in entry['objectClass'] or 'inetorgperson' in entry['objectClass']:
            entry['sn'] = entry['uid']
        entry['cn'] = entry['uid']
        entry['userPassword'] = to_list(password)

        modlist = ldap.modlist.addModlist(entry)
        if debug:
            print modlist

        # synchronous ldapadd
        self._ldap.add_s('uid=%s' % uid + ', ' + (basedn or self._basedn), modlist)

    def add_group(self, cn, gid=None, members=None, basedn=None):
        """Adds new group to LDAP database
        :Parameters:
            - `cn`: Unique in the basedn group identifier
            - `gid`: Group ID
            - `members`: Tuple of user IDs
        """
        # build modlist
        entry = {}
        entry['objectClass'] = ['posixGroup']
        entry['cn'] = to_list(str(cn))
        gid = gid or self.gen_group_gid()
        entry['gidNumber'] = to_list(str(gid))
        if members:
            entry['memberUid'] = to_list(str(members))
        modlist = ldap.modlist.addModlist(entry)
        if debug:
            print modlist

        # synchronous ldapadd
        self._ldap.add_s('cn=%s, %s' % (cn, basedn or self._basedn), modlist)

    def delete_user(self, uid, basedn=None):
        """Deletes a user with uid provided
        :Parameters:
            - `uid`: User's idenifier
        """
        dn = 'uid=%s,' % (uid) + (basedn or self._basedn)
        self._ldap.delete_s(dn)

    def delete_group(self, cn, basedn=None):
        """Deletes a group with cn provided
        :Parameters:
            - `cn`: Group's common name
        """
        dn = 'cn=%s, %s' % (cn, basedn or self._basedn)
        self._ldap.delete_s(dn)

    def modify_user(self, uid, mod_param_name, mod_param_value, mod_add=False,
                    basedn=None):
        """ If mod_add is True - will use MOD_ADD instaed of MOD_REPLACE"""
        dn = 'uid=%s' % uid + ', ' + (basedn or self._basedn)
        if mod_add:
            self._ldap.modify_s(dn,
                                [(ldap.MOD_ADD, str(mod_param_name), mod_param_value)])
        else:
            self._ldap.modify_s(dn,
                                [(ldap.MOD_REPLACE, str(mod_param_name), mod_param_value)])

    def modify_group(self, cn, mod_param_name, mod_param_value, basedn=None):
        """Modifies a group with cn provided
        :Parameters:
            - `cn`: Group's common name
            - `mod_param_name`: LDAP attribute to be modified
            - `mod_param_value`: new value
        """
        dn = 'cn=%s, %s' % (cn, basedn or self._basedn)
        self._ldap.modify_s(dn,
                            [(ldap.MOD_REPLACE, str(mod_param_name), mod_param_value)])

    def create_user(self,
                    uid,
                    password,
                    mail=None,
                    mail_alternate_address=None,
                    mail_local_address=None,
                    mail_routing_address=None,
                    use_mod_add_for=None, basedn=None, **kwargs):
        """
        Adds user with additional attrs to the LDAP server.
        additional attrs = mailLocalAddress, mailRoutingAddress.
        If 'use_mod_add_for' is given  - will add values
        (only those from 'use_mod_add_for') using MOD_ADD instead of MOD_REPLACE.
        example:
        use_mod_add_for=('mail_alternate_address', 'mail_routing_address')
        """
        result = self.get_user(uid, basedn)
        if not use_mod_add_for:
            use_mod_add_for = []
        else:
            use_mod_add_for = use_mod_add_for.lower()
        if result and result[0][0] != None:
            if not to_list(password) == result[0][1]['userPassword']:
                self.modify_user(uid, 'userPassword', password)
            if mail:
                if not to_list(mail) == result[0][1]['mail']:
                    if 'mail' in use_mod_add_for:
                        self.modify_user(uid, 'mail', mail, mod_add=True)
                    else:
                        self.modify_user(uid, 'mail', mail)
            if mail_alternate_address:
                if not to_list(mail_alternate_address) == \
                       result[0][1]['mailAlternateAddress']:
                    if 'mail_alternate_address' in use_mod_add_for:
                        self.modify_user(uid, 'mailAlternateAddress',
                                         to_list(mail_alternate_address),
                                         mod_add=True)
                    else:
                        self.modify_user(uid, 'mailAlternateAddress',
                                         to_list(mail_alternate_address))

            if mail_local_address and not to_list(mail_local_address) == \
                                          result[0][1]['mailLocalAddress']:
                if 'mail_local_address' in use_mod_add_for:
                    self.modify_user(uid, 'mailLocalAddress',
                                     to_list(mail_local_address),
                                     mod_add=True)
                else:
                    self.modify_user(uid, 'mailLocalAddress',
                                     to_list(mail_local_address))
            if mail_routing_address and not to_list(mail_routing_address) == \
                                            result[0][1]['mailRoutingAddress']:
                if 'mail_routing_address' in use_mod_add_for:
                    self.modify_user(uid,
                                     'mailRoutingAddress',
                                     to_list(mail_routing_address), mod_add=True)
                else:
                    self.modify_user(uid,
                                     'mailRoutingAddress',
                                     to_list(mail_routing_address))
        else:
            self.add_user(uid,
                          password,
                          mail,
                          mail_alternate_address,
                          mail_local_address,
                          mail_routing_address, basedn=None, **kwargs)

    def create_group(self, cn, gid=None, members=None, basedn=None):
        """Updates existing or adds new group with parameters provided
        :Parameters:
            - `cn`: Group's common name
        """
        result = self.get_group(cn, basedn)
        if result and result[0][0] != None:
            # Group already exists. Just update attributes
            record = result[0][1]
            if gid:
                if not to_list(gid) == record['gidNumber']:
                    self.modify_group(cn, 'gidNumber', gid, basedn=basedn)
            if not to_list(members) == record['memberUid']:
                self.modify_group(cn, 'memberUid', members, basedn=basedn)
        else:
            self.add_group(cn, gid, members, basedn=basedn)

    def get_user(self, uid=None, basedn=None):
        """ Returns the LDAP records of users.

        If uid is not None the record of particular user will be returned
        :Parameters:
            - `uid`: unique user identifier.
        :Return:
            tuple of found LDAP records
        """
        if uid is None:
            filter = 'uid=*'
        else:
            filter = 'uid=%s' % str(uid)

        # ldapsearch

        results = self._ldap.search_st(basedn or self._basedn,
                                       scope=ldap.SCOPE_ONELEVEL, filterstr=filter, timeout=60)
        return results

    def get_group(self, cn=None, basedn=None):
        """ Returns the LDAP records of groups.

        If cn is not None the record of particular group will be returned
        :Parameters:
            - `cn`: unique group identifier.
        :Return:
            Tuple of found LDAP records
        """
        if cn is None:
            filter = '(objectClass=posixGroup)'
        else:
            filter = '(&(cn=%s)(objectClass=posixGroup))' % (cn,)

        # ldapsearch
        results = self._ldap.search_st(basedn or self._basedn,
                                       scope=ldap.SCOPE_ONELEVEL, filterstr=filter, timeout=60)

        return results

    @staticmethod
    def gen_uid(i=None):
        """return a unique string: <USER><hostname><i>
        'i' starts at 0 and increments each call (while i is None).
        """
        global uid_index
        uid = ''
        hname = socket.gethostname()
        user = os.environ['USER']
        pid = os.getpid()
        if i == None:
            i = uid_index
            uid_index += 1
        uid = user + str(i) + hname
        uid = re.sub('\.', '', uid)
        return uid

    @staticmethod
    def gen_group_cn(i=None):
        """return a unique string: group<USER><hostname><i>
        'i' starts at 0 and increments each call (while i is None).
        """
        global gcn_index
        cn = ''
        hname = socket.gethostname()
        user = os.environ['USER']
        if i is None:
            i = gcn_index
            gcn_index += 1
        cn = 'group' + user + str(i) + hname
        cn = re.sub('\.', '', cn)
        return cn

    def gen_group_gid(self, method='last'):
        """return the available group id
        "method" stands for a way of searching the available gid:
        - last: next after last existing
        - first: first available
        """
        # search for any group in current basedn
        results = self.get_group()

        if results and results[0][0] != None:
            if method == 'last':
                max_val = 0
                for result in results:
                    gidNumber = int(result[1]['gidNumber'][0])
                    max_val = max(gidNumber, max_val)
                gid = max_val + 1

            elif method == 'first':
                gids = set()
                for result in results:
                    gids.add(int(result[1]['gidNumber'][0]))
                gid = 1
                while gid in gids:
                    gid += 1

            else:
                raise ConfigError, 'Unknown searching method'
        else:
            gid = 1

        return str(gid)

    @staticmethod
    def gen_password():
        return 'ironport'

    @staticmethod
    def get_uid_index():
        return uid_index

    @staticmethod
    def gen_mail_addresses(user, domain, qty=1):
        """(username, domain, repeat=0)
        Return a string or list based on the input parameters, username,
        repeat and domain For example,
           Create_mailaddress (daniely, qa57.qa, 5)
           The return list with be
           {daniely1@qa57.qa, daniely2@qa57.qa, daniely3@qa57.qa,
            daniel4@qa57.qa, daniel5@qa57.qa}
        """
        if qty == 1:
            return user + str(qty) + '@' + domain

        addr_list = []
        for i in range(qty):
            addr_list.append(user + str(i) + '@' + domain)
        return addr_list


class EuqOpenLdapClient(OpenLdapClient):
    def __init__(self, host, port=None, binddn=None,
                 password=None, basedn=None, do_connect=True):
        self._host = host
        self._port = port or 389
        self._binddn = binddn or 'uid=rblaes,ou=people,ou=corporate,dc=qa'
        self._password = password or 'rblaes'
        self._basedn = basedn or 'ou=Bingo, ou=mfc, dc=qa'

        if do_connect:
            self.connect()

    pass


class EuqSunOneLdapClient(EuqOpenLdapClient):
    """Assuming openldap.qa has same schema has sunone.qa"""
    pass


# #TODO:LOW
# #
# # This class is incomplete. We need to research how to add and
# # delete users on an AD server.
#####
class EuqAdLdapClient:
    """MS-Windows Acitve Directory Ldap client"""

    def __init__(self, host=None, port=None, binddn=None,
                 password=None, basedn=None, do_connect=True):
        self._host = host or None
        self._port = port or 389
        self._binddn = binddn or None
        self._password = password or None
        self._basedn = basedn or None

        if do_connect:
            self.connect()

    def connect(self):
        # open ldap connection
        self._ldap = ldap.open(self._host, int(self._port))
        self._ldap.simple_bind(self._binddn, self._password)
        return self

    def add_user(self, uid, password, mail, mail_alternate_address=None,
                 basedn=None):
        # build modlist
        entry = {}
        entry[None] = to_list(uid)
        entry[None] = to_list(password)
        entry[None] = to_list(mail)
        if mail_alternate_address != None:
            entry[None] = to_list(mail_alternate_address)
        modlist = ldap.modlist.addModlist(entry)

        # synchronous ldapadd
        self._ldap.add_s(basedn or self._basedn, modlist)

    def delete_user(self, uid, basedn=None):
        dn = None  # #TODO:LOW'=%s,'% (uid) + self._basedn
        self._ldap.delete_s(dn)

    def get_user(self, uid=None, basedn=None):
        if uid == None:
            filter = None  # #TODO:LOW'=*'
        else:
            filter = None  # #TODO:LOW '=%s' % str(uid)

        # ldapsearch
        results = self._ldap.search_st(basedn or self._basedn,
                                       scope=ldap.SCOPE_ONELEVEL, filterstr=filter, timeout=60)

        return results
