#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/reportingconfig.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import clictorbase
import commit
from sal.containers.yesnodefault import NO, YES
DEFAULT = clictorbase.DEFAULT


class reportingconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('reportingconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command=\
                                               'Choose the operation')
        param_map['license_agreement'] = [
            'Do you accept the above license agreement', [YES, YES]]
        param_map['enable_email'] = ['enable Centralized Email Reporting', DEFAULT]
        param_map['enable_web'] = ['enable Centralized Web Reporting', DEFAULT]
        param_map['anonymize'] = ['anonymize usernames in reports', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def filters(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                        end_of_command='Choose the operation')
        param_map['groups'] = ['which groups to filter', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('FILTERS')
        return self._process_input(param_map)

    def alert_timeout(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                        end_of_command='Choose the operation')
        param_map['enable'] = ['timeout alerts to be enabled', DEFAULT]
        param_map['timeout'] = ['many minutes should an alert be sent', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('ALERT_TIMEOUT')
        return self._process_input(param_map)

    def domain(self):
        self._query_response('DOMAIN')
        return reportingDomain(self._get_sess())

class reportingDomain(clictorbase.IafCliConfiguratorBase):

    def tld(self):
        self._query_response('TLD')
        return reportingDomainTLD(self._get_sess())

    def hat_reject_info(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                        end_of_command='Choose the operation')
        param_map['include'] = ['Use message recipient HAT REJECT', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('HAT_REJECT_INFO')
        return self._process_input(param_map)

class reportingDomainTLD(clictorbase.IafCliConfiguratorBase):
    newlines = 3

    def _write_domains(self, domains):
        if domains is not None:
            if isinstance(domains, list) or isinstance(domains, tuple):
                self._writeln('\n'.join(domains))
            elif isinstance(domains, basestring):
                self._writeln(domains)
            else:
                raise ConfigError('List of domains must be one of the type: '\
                                  'string, list or tuple.')
        self._writeln('\n.\n')

    def add(self, domains=None):
        self._query_response('ADD')
        self._write_domains(domains)
        self._to_the_top(self.newlines)

    def replace(self, domains=None):
        self._query_response('REPLACE')
        self._write_domains(domains)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rc = reportingconfig(cli_sess)

    rc().setup()
    rc().setup(enable_email=YES, enable_web=NO)
    rc().setup(enable_email=NO, enable_web=YES)
    rc().filters(groups='1')
    rc().filters(groups='1, 2, 3')
    rc().alert_timeout(enable=YES, timeout=30)
    rc().alert_timeout(enable=NO)
    rc().domain().hat_reject_info(include=YES)
    rc().domain().hat_reject_info(include=NO)
    rc().domain().tld().add(('mail.qa',))
    rc().domain().tld().add(['test.com',])
    rc().domain().tld().replace('ironport.com')
    rc().domain().tld().clear()
