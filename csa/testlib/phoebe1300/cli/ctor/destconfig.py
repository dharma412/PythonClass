#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/destconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO

DEBUG = True


class destconfig(clictorbase.IafCliConfiguratorBase):
    class ValidationProfileNameError(IafCliError):
        pass

    class TableActionError(IafCliError):
        pass

    class ProfileNameError(IafCliError):
        pass

    class DomainFindError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('was not found in the destination', EXACT): self.DomainFindError,
            ('No destination control table action for',
             EXACT): self.TableActionError,
            ('bounce profile name must start with',
             EXACT): self.ProfileNameError,
            ('Invalid profile name', EXACT): self.ValidationProfileNameError,
        })

    def __call__(self):
        self._writeln('destconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['domain'] = \
            ['domain you wish to configure', REQUIRED]
        param_map['concurrency_config'] = \
            ['to configure a concurrency limit', DEFAULT]
        param_map['concurrency'] = ['max concurrency limit', DEFAULT]
        param_map['limit_config'] = ['apply a recipient limit', DEFAULT]
        param_map['limit'] = \
            ['measure the recipient limit', DEFAULT]
        param_map['recipients'] = \
            ['max number of recipients', REQUIRED]
        param_map['limits_apply'] = \
            ['to apply the limits for', DEFAULT, True]
        param_map['limits_enforced'] = \
            ['limits will be enforced', DEFAULT, True]
        param_map['messages_apply'] = \
            ['apply a messages-per-connection limit', DEFAULT]
        param_map['messages_limit'] = \
            ['max number of messages', DEFAULT]
        param_map['tls_apply'] = \
            ['to apply a specific TLS setting', DEFAULT]
        param_map['tls_use'] = ['use TLS support', DEFAULT, True]
        param_map['dane_apply'] = \
            ['wish to configure DANE Support', DEFAULT]
        param_map['dane_use'] = ['choose a DANE option', DEFAULT, True]
        param_map['demo_certificate'] = \
            ['have not entered a certificate', DEFAULT]
        param_map['address_apply'] = \
            ['apply a specific bounce verification', DEFAULT]
        param_map['address_perform'] = \
            ['bounce verification address tagging', DEFAULT]
        param_map['profile_apply'] = \
            ['apply a specific bounce profile', DEFAULT]
        param_map['profile'] = \
            ['bounce profile to apply', DEFAULT, True]
        param_map['profile_name'] = ['name of a profile', REQUIRED]
        param_map['ip_preference_apply'] = \
            ['apply a specific IP sort preference', DEFAULT]
        param_map['ip_preference'] = \
            ['sort IP addresses within an MX', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['domain'] = ['domain you wish to edit', REQUIRED]
        param_map['concurrency_config'] = \
            ['configure a concurrency limit', DEFAULT]
        param_map['concurrency'] = ['max concurrency limit', DEFAULT]
        param_map['limit_config'] = ['apply a recipient limit', DEFAULT]
        param_map['limit'] = \
            ['measure the recipient limit', DEFAULT]
        param_map['recipients'] = ['max number of recipients', DEFAULT]
        param_map['limits_apply'] = \
            ['to apply the limits for', DEFAULT, True]
        param_map['limits_enforced'] = \
            ['limits will be enforced', DEFAULT, True]
        param_map['messages_apply'] = \
            ['apply a messages-per-connection limit', DEFAULT]
        param_map['messages_limit'] = \
            ['max number of messages', DEFAULT]
        param_map['tls_apply'] = \
            ['to apply a specific TLS setting', DEFAULT]
        param_map['tls_use'] = \
            ['use TLS support', DEFAULT, True]
        param_map['dane_apply'] = \
            ['wish to configure DANE Support', DEFAULT]
        param_map['dane_use'] = ['choose a DANE option', DEFAULT, True]
        param_map['demo_certificate'] = \
            ['have not entered a certificate', DEFAULT]
        param_map['address_apply'] = \
            ['apply a specific bounce verification address', DEFAULT]
        param_map['address_perform'] = \
            ['bounce verification address tagging', DEFAULT]
        param_map['profile_apply'] = \
            ['apply a specific bounce profile', DEFAULT]
        param_map['profile'] = \
            ['bounce profile to apply', DEFAULT, True]
        param_map['profile_name'] = ['name of a profile', REQUIRED]
        param_map['ip_preference_apply'] = \
            ['apply a specific IP sort preference', DEFAULT]
        param_map['ip_preference'] = \
            ['sort IP addresses within an MX', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        return self._process_input(param_map)

    def default(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['concurrency'] = \
            ['default maximum concurrency limit', DEFAULT]
        param_map['limit_config'] = \
            ['specify a default recipient limit', DEFAULT]
        param_map['limit'] = \
            ['measure recipient limit', DEFAULT]
        param_map['recipients'] = \
            ['Enter number of recipients', DEFAULT]
        param_map['limits_apply'] = \
            ['apply the limits for', DEFAULT, True]
        param_map['limits_enforced'] = \
            ['limits will be enforced', DEFAULT, True]
        param_map['messages_limit'] = \
            ['maximum number of messages', DEFAULT]
        param_map['tls_use'] = ['use TLS support', DEFAULT, True]
        param_map['dane_use'] = ['use DANE Support', DEFAULT, True]
        param_map['demo_certificate'] = \
            ['have not entered a certificate', DEFAULT]
        param_map['address_perform'] = \
            ['verification address tagging', DEFAULT]
        param_map['ip_preference'] = \
            ['sort IP addresses within an MX', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('DEFAULT')
        return self._process_input(param_map)

    def detail(self, domain=None):
        self.level = 1
        self._query_response('DETAIL')
        self._query_response(domain)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def list(self):
        self.level = 1
        self._query_response('LIST')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def delete(self, domain=None):
        self.level = 1
        self._query_response('DELETE')
        self._query_response(domain)
        self._to_the_top(self.level)

    def clear(self):
        self.level = 1
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['cert_name'] = ['Please choose the certificate', DEFAULT, True]
        param_map['send_alert'] = ['send an alert when a required TLS', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    import clear

    clr = clear.clear(cli_sess)
    clr()
    destc = destconfig(cli_sess)

    destc().new(domain='191.1.1.1', concurrency_config=YES, concurrency='400',
                limit_config=YES, limit='40', recipients='300',
                limits_apply='Separate limit',
                limits_enforced='System Wide', tls_apply=YES,
                tls_use='Preferred', profile_apply=YES,
                profile='New Profile', profile_name='profile',
                ip_preference_apply=YES, ip_preference='Require IPv6')
    destc().new(domain='191.1.1.2', limit_config=NO, limits_apply='1',
                limits_enforced='Per Virtual Gateway',
                profile_apply=YES, profile='New Profile',
                profile_name='profile2')
    destc().edit(domain='191.1.1.2', concurrency_config=YES,
                 concurrency='123', limit_config=YES, limit='40',
                 recipients='300', limits_apply='One limit',
                 limits_enforced='Per Virtual Gateway(tm)', tls_apply=YES,
                 tls_use='Preferred - Verify', profile_apply=YES, profile='2',
                 profile_name='profile3')
    destc().default(concurrency='123', limit_config=YES, limit='40',
                    recipients='300', limits_apply='One limit',
                    limits_enforced='Per Virtual Gateway',
                    tls_use='Preferred - Verify')
    print destc().detail(domain='all')
    print destc().list()
    destc().delete(domain='191.1.1.1')
    destc().clear()
