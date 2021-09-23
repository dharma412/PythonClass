#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/bounceconfig.py#1 $

"""
IAF 2 CLI command: bounceconfig
"""

import re
import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO, is_yes

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

        ending_strings = re.compile('Do you want to|Select default|undeliverable')
        param_map1 = ccb.IafCliParamMap(end_of_command=ending_strings)
        param_map1['name']                  = ['create a name', REQUIRED]
        param_map1['max_retries']           = ['maximum number of retries', DEFAULT]
        param_map1['max_queue_lifetime']    = ['stay in the queue', DEFAULT]
        param_map1['initial_retry']         = ['initial number', DEFAULT]
        param_map1['max_retry_timeout']     = ['maximum number of seconds', DEFAULT]
        param_map1['send_bounces_all']      = ['message sent for each hard bounce', DEFAULT]
        param_map1['use_dsn_bounce_format'] = ['DSN message', DEFAULT]
        param_map1['dsn_subject']           = ['subject to use', DEFAULT]

        self._query_response('NEW')

        actual_dict={}
        for param in input_dict.keys():
            if param in param_map1._map.keys():
                actual_dict[param] = input_dict[param]
        param_map1.update(actual_dict or kwargs)
        self._process_input(param_map1, do_restart=False)

        self._expect(['notification template', 'parse the DSN', 'after some interval'])

        if self._expectindex == 0:
            self._query_select_list_item(input_dict['default_bounce_notification_template'])
            self._query_response(input_dict['configure_language_specific_bounce_templates'])
            if input_dict['configure_language_specific_bounce_templates']:
                bounceconfigNotificationTemplate(self._get_sess()). \
                    add(input_dict['language_specific_bounce_templates'])

        ending_strings = re.compile('Please enter the minimum|Select default|Do you want hard bounce')
        param_map2 = ccb.IafCliParamMap(end_of_command=ending_strings)
        param_map2['parse_dsn']              = ['include in the DSN generated', DEFAULT]
        param_map2['send_warnings']          = ['send a delay', DEFAULT]
        param_map2['warnings_subject']       = ['Notification (Delay)', DEFAULT]
        actual_dict={}
        for param in input_dict.keys():
            if param in param_map2._map.keys():
                actual_dict[param] = input_dict[param]
        param_map2.update(actual_dict or kwargs)
        self._process_input(param_map2, do_restart=False)

        self._expect(['notification template', 'interval in ', 'an alternate address'])

        param_map3 = ccb.IafCliParamMap(end_of_command='Choose the operation')
        if is_yes(input_dict['send_warnings']):
            if self._expectindex == 0:
                self._query_select_list_item(input_dict['default_delay_notification_template'])
                self._query_response(input_dict['configure_language_specific_delay_templates'])
                if input_dict['configure_language_specific_delay_templates']:
                    bounceconfigNotificationTemplate(self._get_sess()). \
                        add(input_dict['language_specific_delay_templates'])
            param_map3['warnings_interval']      = ['seconds between delay warning', DEFAULT]
            param_map3['send_warnings_count']    = ['send per', DEFAULT]
        param_map3['send_warning_to_alt']    = ['instead of the sender', DEFAULT]
        param_map3['alt_address']            = ['email address', NO_DEFAULT]
        param_map3['msgs_signed']            = ['messages to be signed', DEFAULT]
        param_map3['send_warnings_interval'] = ['minimum interval', DEFAULT]

        actual_dict={}
        for param in input_dict.keys():
            if param in param_map3._map.keys():
                actual_dict[param] = input_dict[param]
        param_map3.update(actual_dict or kwargs)
        self._process_input(param_map3)
        print '-----------------------------'
        print self._sess.getbuf()
        print '-----------------------------'
        self.clearbuf()

    def edit(self, prof_numb, input_dict=None, **kwargs):
        global REQUIRED, DEFAULT

        input_dict['prof_numb'] = self._get_bounce_profile_number(prof_numb)

        ending_strings = re.compile('Do you want to|Select default|undeliverable')
        param_map1 = ccb.IafCliParamMap(end_of_command=ending_strings)
        param_map1['prof_numb']             = ['the profile to edit', REQUIRED]
        param_map1['name']                  = ['name for the profile', DEFAULT]
        param_map1['max_retries']           = ['maximum number of retries', DEFAULT]
        param_map1['max_queue_lifetime']    = ['stay in the queue', DEFAULT]
        param_map1['initial_retry']         = ['initial number', DEFAULT]
        param_map1['max_retry_timeout']     = ['maximum number of seconds', DEFAULT]
        param_map1['send_bounces_all']      = ['message sent for each hard bounce', DEFAULT]
        param_map1['use_dsn_bounce_format'] = ['DSN message', DEFAULT]
        param_map1['dsn_subject']           = ['subject to use', DEFAULT]

        self._query_response('EDIT')

        actual_dict={}
        for param in input_dict.keys():
            if param in param_map1._map.keys():
                actual_dict[param] = input_dict[param]
        param_map1.update(actual_dict or kwargs)
        self._process_input(param_map1, do_restart=False)

        self._expect(['notification template', 'parse the DSN', 'after some interval'])

        if self._expectindex == 0:
            self._query_select_list_item(input_dict['default_bounce_notification_template'])
            self._query_response(input_dict['configure_language_specific_bounce_templates'])
            if input_dict['configure_language_specific_bounce_templates']:
                bounceconfigNotificationTemplate(self._get_sess()). \
                    add(input_dict['language_specific_bounce_templates'])

        ending_strings = re.compile('Please enter the minimum|Select default|Do you want hard bounce')
        param_map2 = ccb.IafCliParamMap(end_of_command=ending_strings)
        param_map2['parse_dsn']              = ['include in the DSN generated', DEFAULT]
        param_map2['send_warnings']          = ['send a delay', DEFAULT]
        param_map2['warnings_subject']       = ['Notification (Delay)', DEFAULT]
        actual_dict={}
        for param in input_dict.keys():
            if param in param_map2._map.keys():
                actual_dict[param] = input_dict[param]
        param_map2.update(actual_dict or kwargs)
        self._process_input(param_map2, do_restart=False)

        self._expect(['notification template', 'interval in ', 'an alternate address'])

        param_map3 = ccb.IafCliParamMap(end_of_command='Choose the operation')
        if is_yes(input_dict['send_warnings']):
            if self._expectindex == 0:
                self._query_select_list_item(input_dict['default_delay_notification_template'])
                self._query_response(input_dict['configure_language_specific_delay_templates'])
                if input_dict['configure_language_specific_delay_templates']:
                    bounceconfigNotificationTemplate(self._get_sess()). \
                        add(input_dict['language_specific_delay_templates'])
            param_map3['warnings_interval']      = ['seconds between delay warning', DEFAULT]
            param_map3['send_warnings_count']    = ['send per', DEFAULT]
        param_map3['send_warning_to_alt']    = ['instead of the sender', DEFAULT]
        param_map3['alt_address']            = ['email address', NO_DEFAULT]
        param_map3['msgs_signed']            = ['messages to be signed', DEFAULT]
        param_map3['send_warnings_interval'] = ['minimum interval', DEFAULT]
        param_map3['host_initial_retry']      = \
                ['initial number of seconds to wait before retrying a host ', DEFAULT]
        param_map3['host_max_retry_timeout']  = \
                ['maximum number of seconds to wait before retrying a host', DEFAULT]
        param_map3['bounced_msg_size'] = ['original message (in bytes)', DEFAULT]

        actual_dict={}
        for param in input_dict.keys():
            if param in param_map3._map.keys():
                actual_dict[param] = input_dict[param]
        param_map3.update(actual_dict or kwargs)
        self._process_input(param_map3)
        print '-----------------------------'
        print self._sess.getbuf()
        print '-----------------------------'
        self.clearbuf()

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

    def batch(self, action, profile, input_dict=None, **kwargs):
        params = input_dict or kwargs

        allowed_params = [
            'max_retries',                  'max_queue_lifetime',
            'initial_retry',                'max_retry_timeout',
            'send_bounces',                 'use_dsn_bounce_format',
            'use_bounce_response_code',     'bounce_address',
            'bounce_subject',               'bounce_template',
            'send_warnings',                'send_warnings_count',
            'send_warnings_interval',       'delay_subject',
            'delay_template',               'sign_bounce_messages',
            'host_max_retry_timeout',       'host_initial_retry',
            'max_bounce_copy',
        ]
        batch_cmd = 'bounceconfig %s %s ' % (action, profile)
        if not params.keys():
            raise ValueError('bounceconfig %s batch command need atleast one parameter. \
                    Allowed parameters are: %s' % (action, allowed_params))
        for param in params.keys():
            if param not in allowed_params:
                raise ValueError('Wrong parameter [%s]. Allowed parameters are: %s'\
                        % (param, allowed_params))
            batch_cmd += param + '=' + params[param] + ' '
        self._info('BATCH COMMAND: %s' % batch_cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(batch_cmd)
        self._wait_for_prompt()
        print self._sess.getbuf()

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

class bounceconfigNotificationTemplate(ccb.IafCliConfiguratorBase):
    def __init__(self, sess):
        try:
            ccb.IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

    def add(self, template_dict={}):
        for language in template_dict.keys():
            self._query_response('ADD')
            self._query_select_list_item(language)
            self._query_select_list_item(template_dict[language])
        self._query_response("")

    def remove(self, template_dict={}):
        for language in template_dict.keys():
            self._query_response('REMOVE')
            self._query_select_list_item(language)
        self._to_the_top(1)


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
