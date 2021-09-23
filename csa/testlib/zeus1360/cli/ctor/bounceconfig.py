#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/bounceconfig.py#1 $

"""
IAF 2 CLI command: bounceconfig
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO

DEBUG = True
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
NO_DEFAULT = ccb.DEFAULT

class bounceconfig(ccb.IafCliConfiguratorBase):

    class ProfileNameExistError(ccb.IafCliError): pass
    class ProfileNameError(ccb.IafCliError): pass
    class DefaultProfileDeleteError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self.error_message = 'Specified profile does not exist.'

        self._set_local_err_dict({
            ('Profile name already in use', EXACT): self.ProfileNameExistError,
            ('The bounce profile name must start with a letter or underscore',
                                       EXACT): self.ProfileNameError,
            ('The default profile may not be deleted',
                                       EXACT): self.DefaultProfileDeleteError
            })

    def __call__(self):
        self._writeln('bounceconfig')

        output_string = self._read_until('Choose the operation')
        self._profiles = self._get_bounce_profiles(output_string)

        return self

    def new(self, input_dict=None, **kwargs):
        global REQUIRED, DEFAULT, NO_DEFAULT
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['name']                   = ['create a name', REQUIRED]
        param_map['max_retries']            = \
                                       ['maximum number of retries', DEFAULT]
        param_map['max_queue_lifetime']     = ['stay in the queue', DEFAULT]
        param_map['initial_retry']          = ['initial number', DEFAULT]
        param_map['max_retry_timeout']      = \
                                       ['maximum number of seconds', DEFAULT]
        param_map['send_bounces_all'] = ['message sent for each hard bounce',
                                                                DEFAULT]

        param_map['use_dsn_bounce_format']  = ['DSN message', DEFAULT]
        param_map['dsn_subject']            = \
                                            ['Notification (Failure)', DEFAULT]
        param_map['parse_dsn']              = ['parse the DSN', DEFAULT]
        param_map['send_warnings']          = ['send a delay', DEFAULT]
        param_map['warnings_subject']       = \
                                       ['Notification (Delay)', DEFAULT]
        param_map['warnings_interval']      = \
                                 ['seconds between delay warning', DEFAULT]
        param_map['send_warnings_count']    = ['send per', DEFAULT]
        param_map['send_warning_to_alt']    = ['instead of the sender', DEFAULT]
        param_map['alt_address']            = ['email address', NO_DEFAULT]
        param_map['msgs_signed']            = ['messages to be signed', DEFAULT]
        param_map['send_warnings_interval'] = ['minimum interval', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')

        return self._process_input(param_map)

    def edit(self, prof_numb, input_dict=None, **kwargs):
        global REQUIRED, DEFAULT

        input_dict['prof_numb'] = self._get_bounce_profile_number(prof_numb)

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['prof_numb']              = ['the profile to edit', REQUIRED]
        param_map['max_retries']            = \
                                       ['maximum number of retries', DEFAULT]
        param_map['max_queue_lifetime']     = ['stay in the queue', DEFAULT]
        param_map['initial_retry']          = ['initial number', DEFAULT]
        param_map['max_retry_timeout']      = \
                                       ['maximum number of seconds', DEFAULT]
        param_map['use_dsn_bounce_format']  = ['DSN message', DEFAULT]
        param_map['dsn_subject']            = \
                                       ['Enter the subject to use', DEFAULT]
        param_map['parse_dsn']              = ['parse the DSN', DEFAULT]
        param_map['send_warnings']          = ['send a delay', DEFAULT]
        param_map['send_warnings_count']    = ['send per', DEFAULT]
        param_map['warnings_subject']       = \
                                        ['Notification (Delay)', DEFAULT]
        param_map['send_warning_to_alt']    = ['alternate address', DEFAULT]
        param_map['alt_address']            = ['email address', NO_DEFAULT]
        param_map['msgs_signed']            = ['messages to be signed', DEFAULT]
        param_map['warnings_interval'] = ['minimum interval', DEFAULT]
        param_map['host_initial_retry']     = \
        ['initial number of seconds to wait before retrying a host ', DEFAULT]
        param_map['host_max_retry_timeout'] = \
        ['maximum number of seconds to wait before retrying a host', DEFAULT]
        param_map['send_bounces_all'] = ['message sent for each hard bounce',
                                                DEFAULT]
        param_map['bounced_msg_size'] = ['original message (in bytes)', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        return self._process_input(param_map)

    def setup(self, input_dict=None, **kwargs):
        global DEFAULT
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['bounce_enqueued_messages'] = \
                 ['bounce all enqueued messages bound for a domain', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def delete(self, prof_numb, input_dict=None, **kwargs):
        global REQUIRED, DEFAULT

        input_dict['prof_numb'] = self._get_bounce_profile_number(prof_numb)

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['prof_numb']              = ['profile to delete', REQUIRED]
        param_map['confirmation']           = \
                                 ['Are you sure you want to delete', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')

        return self._process_input(param_map)

    def _get_bounce_profiles(self, output_string):
        profile_string = output_string[output_string.find('1. Default'):output_string.rfind('\n')]
        profile_string = profile_string.replace('\n','').replace('. ','.')
        profiles = dict( (key,value) for value,key in (temp.split('.') \
                for temp in profile_string.split() ))

        return profiles

    def _get_bounce_profile_number(self, profile_name):
        try:
            return self._profiles[profile_name]
        except:
            print profile_name
            raise ValueError(self.error_message)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    bc = bounceconfig(cli_sess)

    bc().new(name='test')
    bc().new(name='test123', max_queue_lifetime='234', use_alt_address=YES,
               alt_address='sa@asd.er', send_warnings=YES)
    bc().edit(prof_numb='2',max_retries='65', max_retry_timeout='80',
               use_alt_address=NO)
    bc().delete(prof_numb='2')
    bc().edit(prof_numb='1', host_initial_retry='61',
                             host_max_retry_timeout='122')
