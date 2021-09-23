# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/graymailconfig.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

import re
from clictorbase import DEFAULT, REQUIRED, IafCliParamMap, IafCliConfiguratorBase
from sal.containers.yesnodefault import is_yes, YES, NO


class graymailconfig(IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('graymailconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        if not kwargs.keys():
            param_map['use_graymail_detection'] = ['use Graymail Detection', DEFAULT]
            param_map['maximum_message_scanning_size'] = ['Maximum Message Size to Scan', DEFAULT]
            param_map['message_scanning_timeout'] = ['Timeout for Scanning Single Message', DEFAULT]
            param_map['use_graymail_safe_unsubscribe'] = ['use Graymail Safe Unsubscribe', DEFAULT]
            param_map['enable_automatic_updates'] = ['enable automatic updates for Graymail engine', DEFAULT]
        else:
            param_map['use_graymail_detection'] = ['use Graymail Detection', REQUIRED]
            if is_yes(kwargs['use_graymail_detection']):
                param_map['use_graymail_detection'] = ['use Graymail Detection', YES]
                if kwargs.has_key('maximum_message_scanning_size'):
                    if re.match(r'^\d+(K|M)?$', kwargs['maximum_message_scanning_size'], re.I):
                        param_map['maximum_message_scanning_size'] = \
                            ['Maximum Message Size to Scan', kwargs['maximum_message_scanning_size']]
                        if kwargs.has_key('confirm_message_scanning_size'):
                            param_map['confirm_message_scanning_size'] = \
                                ['Are you sure that you want this set to', kwargs['confirm_message_scanning_size']]
                            if not is_yes(kwargs['confirm_message_scanning_size']):
                                param_map['maximum_message_scanning_size1'] = ['Maximum Message Size to Scan', DEFAULT]
                        else:
                            if kwargs['maximum_message_scanning_size'].lower() > '10m':
                                param_map['confirm_message_scanning_size'] = \
                                    ['Are you sure that you want this set to', NO]
                                param_map['maximum_message_scanning_size2'] = \
                                    ['Maximum Message Size to Scan', DEFAULT]
                            elif kwargs['maximum_message_scanning_size'].lower() > '10240k':
                                param_map['confirm_message_scanning_size'] = \
                                    ['Are you sure that you want this set to', NO]
                                param_map['maximum_message_scanning_size3'] = \
                                    ['Maximum Message Size to Scan', DEFAULT]
                    else:
                        raise ValueError("Illegal value for [maximum_message_scanning_size] param\n" \
                                         + "Message Scan Size should an integer with or without a trailing K or M")
                else:
                    param_map['maximum_message_scanning_size'] = ['Maximum Message Size to Scan', DEFAULT]

                if kwargs.has_key('message_scanning_timeout'):
                    if re.match(r'^\d+$', kwargs['message_scanning_timeout']):
                        param_map['message_scanning_timeout'] = \
                            ['Timeout for Scanning Single Message', kwargs['message_scanning_timeout']]
                    else:
                        raise ValueError("Illegal value for [maximum_message_scanning_size] param\n" \
                                         + "Timeout value should be between 1 and 60 seconds")
                else:
                    param_map['message_scanning_timeout'] = ['Timeout for Scanning Single Message', DEFAULT]

                if kwargs.has_key('use_graymail_safe_unsubscribe'):
                    if is_yes(kwargs['use_graymail_safe_unsubscribe']):
                        param_map['use_graymail_safe_unsubscribe'] = ['use Graymail Safe Unsubscribe', YES]
                        if kwargs.has_key('use_graymail_safe_unsubscribe'):
                            param_map['accept_safe_unsubscribe_license'] = \
                                ['accept the above license agreement?', kwargs['use_graymail_safe_unsubscribe']]
                        else:
                            param_map['accept_safe_unsubscribe_license'] = ['accept the above license agreement?', YES]
                    else:
                        param_map['use_graymail_safe_unsubscribe'] = \
                            ['use Graymail Safe Unsubscribe', kwargs['use_graymail_safe_unsubscribe']]
                        if kwargs.has_key('confirm_safe_unsubscribe_disable'):
                            param_map['confirm_safe_unsubscribe_disable'] = \
                                ['sure you want to disable', kwargs['confirm_safe_unsubscribe_disable']]
                        else:
                            param_map['confirm_safe_unsubscribe_disable'] = \
                                ['sure you want to disable', YES]
                else:
                    param_map['use_graymail_safe_unsubscribe'] = ['use Graymail Safe Unsubscribe', DEFAULT]

                if kwargs.has_key('enable_automatic_updates'):
                    param_map['enable_automatic_updates'] = \
                        ['enable automatic updates for Graymail engine', kwargs['enable_automatic_updates']]
                else:
                    param_map['enable_automatic_updates'] = ['enable automatic updates for Graymail engine', DEFAULT]
            else:
                param_map['use_graymail_detection'] = ['use Graymail Detection', NO]

        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        self._process_input(param_map)

    def batch_setup(self, input_dict=None, **kwargs):
        batch_cmd = 'graymailconfig setup '

        allowed_params = ['max_scan_size', 'scan_timeout', 'unsubscription_enable']

        params = input_dict or kwargs
        if not params:
            raise ConfigError("\"graymailconfig\" batch command requires at least one action, " \
                              + "enable or disable.\nFor \"enable\" following are the optional parameters: " \
                              + "\t\t* max_scan_size\n\t\t* scan_timeout\n\t\t* unsubscription_enable")

        action = params.get('action')
        if action.lower() == 'enable':
            batch_cmd += 'enable'

            for param in params.keys():
                if param == 'action': continue
                if param not in allowed_params:
                    raise ValueError('Invalid parameter [%s] passed to "graymailconfig" batch command' \
                                     % param)

            max_scan_size = params.get('max_scan_size')
            scan_timeout = params.get('scan_timeout')
            unsubscription_enable = params.get('unsubscription_enable')

            if max_scan_size is not None:
                batch_cmd += ' --max_scan_size=%s' % max_scan_size
            if scan_timeout is not None:
                batch_cmd += ' --scan_timeout=%s' % scan_timeout
            if unsubscription_enable is not None:
                batch_cmd += ' --unsubscription_enable=%s' % unsubscription_enable
        else:
            batch_cmd += 'disable'

        self._info('BATCH COMMAND to execute: %s' % batch_cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(batch_cmd)
        self._wait_for_prompt()
        return self.getbuf()

    def is_graymail_enabled(self):
        status = None
        try:
            buffer = self._read_until('Choose the operation')
            self._debug(buffer)
            status = re.search(r'Graymail Detection:\s+(\S+)', buffer).group(1).lower()
        except Exception as e:
            self._warn("Could not get Graymail Engine Status\n%s" % e.message)
        finally:
            self._to_the_top(1)

        return status == 'enabled'


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    gm = graymailconfig(cli_sess)
    gm().setup()
