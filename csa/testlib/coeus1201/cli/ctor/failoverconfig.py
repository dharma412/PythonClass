# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/failoverconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import time
import sys

from sal.exceptions import ConfigError
import clictorbase
from clictorbase import IafCliError, REQUIRED, DEFAULT, EXACT, REGEX, EOL_REGEX, \
    IafCliParamMap, IafCliConfiguratorBase, \
    IafCliValueError
TIMEOUT=10

class failoverconfig(clictorbase.IafCliConfiguratorBase):
    # guestimate for getting back out to top level prompt
    level = 1
    errors = {
        ('Value must be an integer from 1 to 255.', \
             EXACT): IafCliValueError,
        ('Invalid CIDR address. Netmask is required, consisting ' + EOL_REGEX, \
             REGEX): IafCliValueError,
        ('The selected interface does not match the failover IP.', \
             EXACT): IafCliValueError,
        ('The secret cannot contain any whitespace and maximum length ' + EOL_REGEX, \
             REGEX): IafCliValueError,
        ('Passhprases do not match. Please try again', \
             EXACT): IafCliValueError,
        ('The failover IP address should match the following' + EOL_REGEX,  \
             REGEX): IafCliValueError,
        ('Invalid arguments when processing failoverconfig', \
             EXACT): IafCliValueError,
        ('This IP address is already in use', \
             EXACT): IafCliValueError,
        ('The value must not already be in use' + EOL_REGEX, \
             REGEX): IafCliValueError,
        }
    def __init__(self, sess):
        super(failoverconfig, self).__init__(sess)
        self._set_local_err_dict(self.errors)

    def __call__(self):
        self.clearbuf()
        self._writeln('failoverconfig')
        return self

    def new(self, **kwargs):
        return self._new_or_edit(**kwargs)

    def edit(self, **kwargs):
        return self._new_or_edit(new=False, **kwargs)

    def _get_confirmation(self, confirmation='passphrase_confirm',
                          backup='passphrase', **kwargs):
        pswd = None
        if kwargs.get(confirmation):
            pswd = kwargs.get(confirmation)
        if backup and pswd is None:
            # here because there was no password_confirm so use passphrase
            if kwargs.get(backup):
                pswd = kwargs.get(backup)
        if pswd is None:
            pswd = DEFAULT
        return pswd

    def _new_or_edit(self, new=True, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        newly_required= REQUIRED if new else DEFAULT
        if new:
            param_map['groupid'] = ['Failover group ID', REQUIRED]
        else:
            param_map['groupid'] = ['Failover group ID to edit', REQUIRED]
            param_map['new_groupid'] = ['Failover group ID:', DEFAULT]
        param_map['enable'] = ['Enable this failover group', DEFAULT]
        param_map['hostname'] = ['Hostname', newly_required]
        param_map['ip'] = ['Virtual IPv4 or IPv6 address and netmask', newly_required]
        param_map['interface'] = ['Interface:', DEFAULT, True]
        param_map['priority'] = ['Priority', DEFAULT]
        param_map['interval'] = ['Advertisement interval', DEFAULT]
        param_map['passphrase'] = ['Passphrase for message authentication', DEFAULT]
        pswd = self._get_confirmation(**kwargs)
        if pswd:
            param_map['passphrase_confirm'] = \
             ['Re-enter the passphrase for message authentication', pswd]
        if 'passphrase_confirm' in kwargs:
            del kwargs['passphrase_confirm']
        param_map['description'] = ['Failover group description', DEFAULT]
        param_map.update(kwargs)
        self.clearbuf()
        action = 'NEW' if new else 'EDIT'
        self._query_response(action, timeout=TIMEOUT)
        self._process_input(param_map, timeout=TIMEOUT)
        self._end_command()
        return self.getbuf()

    def delete(self, groupid):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['groupid'] = ['Failover group ID to delete', REQUIRED]
        param_map.update({'groupid':groupid})
        self.clearbuf()
        self._query_response('DELETE', timeout=TIMEOUT)
        self._process_input(param_map, timeout=TIMEOUT)
        self._end_command()
        return self.getbuf()

    def preemptive(self, enable):
        self.clearbuf()
        self._query_response('PREEMPTIVE')
        self._expect(
            ['is currently enabled', 'is currently disabled'],
            timeout=TIMEOUT)
        index = self._get_expectindex()
        if (index==1 and enable) or (index==0 and not enable):
            answer = 'Y'
        else:
            answer = 'N'
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['action'] = ['Do you want to', REQUIRED]
        param_map.update({'action':answer})
        self._process_input(param_map, timeout=TIMEOUT)
        self._end_command()
        return self.getbuf()

    def test(self, groupid, elapse_seconds):
        self.clearbuf()
        try:
            self._query_response('TESTFAILOVERGROUP')
            self._query_response(groupid)
            time.sleep(int(elapse_seconds))
            self.interrupt()
            self._expect('Choose the operation',timeout=TIMEOUT)
            self._end_command()
            return self.getbuf()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback
        finally:
            self.interrupt()
            self.interrupt()
            self._restart_nosave()
