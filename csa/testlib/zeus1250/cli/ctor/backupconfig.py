#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/backupconfig.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import clictorbase

from clictorbase import (DEFAULT, REQUIRED)
from sal.containers.yesnodefault import (NO, YES)
from sal.deprecated.expect import EXACT
from sal.exceptions import ConfigError

class BackupScheduleError(clictorbase.IafCliError): pass
class BackupScheduleErrorNoSpace(BackupScheduleError): pass

class backupconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('Error while trying to connect', EXACT): clictorbase.IafCliError,
             ('The IP address must be different', EXACT): ValueError,
             ('the same schedule already exists', EXACT): ValueError,
             ('There is not enough space', EXACT): BackupScheduleErrorNoSpace,
            })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def view(self):
        self._query_response('VIEW')
        self._expect('\n')
        current_view = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return current_view

    def verify(self, ip, name, user, passwd):
        self._query_response('VERIFY')
        self._query_response(ip)
        self._query_response(name)
        self._query_response(user)
        self._query_response(passwd)

        result = self._read_until('Choose the operation', timeout=120)
        self._to_the_top(self.newlines)
        return result

    def schedule(self, job_name, backup_type='repeating', period='daily',
            day_of_month='1', day_of_week='monday', rep_time=None,
            single_date=None, input_dict=None, **kwargs):

        valid_backups = ('repeating', 'single', 'now')
        rep_periods = ('daily', 'monthly', 'weekly')

        if backup_type not in valid_backups:
            raise ValueError('"%s" is invalid backup type. Possible values '\
                              'are %s' % (valid_backups,))

        if period not in rep_periods:
            raise ValueError('"%s" is invalid repeating period. Possible values '\
                              'are %s' % (rep_periods,))

        self._query_response('SCHEDULE')

        param_map = clictorbase.IafCliParamMap(end_of_command='Verifying target machine')
        param_map['ip'] = ['IP address of a machine', REQUIRED]
        param_map['name'] = ['name to identify the remote appliance', REQUIRED]
        param_map['user'] = ['Username:', REQUIRED]
        param_map['passwd'] = ['Passphrase:', REQUIRED]
        param_map['confirm_version'] = ['different AsyncOS version', 'Y']
        param_map['backup_all'] = ['backup all the data', DEFAULT]
        param_map['backup_isq'] = ['backup Spam Quarantine', DEFAULT]
        param_map['backup_email_tracking'] = ['backup Email Tracking', DEFAULT]
        param_map['backup_web_tracking'] = ['backup Web Tracking', DEFAULT]
        param_map['backup_reporting'] = ['backup Reporting', DEFAULT]
        param_map['backup_policy_quarantine'] = ['backup Policy Quarantine', DEFAULT]
        param_map['backup_slbl'] = ['backup Safelist/Blocklist', DEFAULT]
        param_map['backup_policy_quarantine'] = ['backup Policy Quarantine', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._process_input(param_map, do_restart=False, timeout=30)

        self._query_select_list_item(backup_type, timeout=60)

        if backup_type == 'repeating':
            self._query_select_list_item(period)
            if period == 'monthly':
                self._query_response(day_of_month)
            elif period == 'weekly':
                self._query_select_list_item(day_of_week)

            if rep_time is None:
                raise ConfigError('Time must be specified when scheduling '\
                                  'repeating backup')
            self._query_response(rep_time)
        elif backup_type == 'single':
            if single_date is None:
                raise ConfigError('Time and date must be specified when '\
                                  'scheduling single backup')
            self._query_response(single_date)

        self._query_response(job_name)

        self._to_the_top(self.newlines)

    def cancel(self, job_name):
        self._query_response('CANCEL')
        if self._query(['Select the name or number',\
                      'No scheduled backups']) == 0:
            self._query_response(job_name)
        else:
            raise ConfigError('There are no scheduled backup jobs')
        self._to_the_top(self.newlines)

    def status(self):
        self._query_response('STATUS')
        current_status = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return current_status


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    bc = backupconfig(cli_sess)

    print bc().status()
    print bc().view()

