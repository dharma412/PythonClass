#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/imsandgraymailconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $


"""  SARF CLI ctor class for - imsandgraymailconfig command  """

import clictorbase as ccb
import sal.containers.yesnodefault as ynd

YES = ynd.YES
No = ynd.NO
DEFAULT = ccb.DEFAULT


class imsandgraymailconfig(ccb.IafCliConfiguratorBase):
    """
    esa-admin-cli> imsandgraymailconfig

    Choose the operation you want to perform:
    - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
    - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
    - GLOBALCONFIG - Common Global Configuration settings
    []>
    """

    def __call__(self, sub_option, batch_mode=False):
        self.clearbuf()
        if not batch_mode:
            self._writeln('imsandgraymailconfig')
            self._expect(['requires activation', 'Choose the operation'])
            if self._expectindex == 0:
                raise ccb.IafCliError('Feature is not activated. '
                                  'This feature requires activation with a software key')
            if self._expectindex == 1:
                self._query_response(sub_option)
                output = self._read_until('Choose the operation')
        else:
            output = 'batch mode'

        if sub_option == 'GRAYMAIL':
            return imsandgraymailconfigGraymail(self._get_sess(), output)
        elif sub_option == 'MULTISCAN':
            return imsandgraymailconfigMultiscan(self._get_sess(), output)
        elif sub_option == 'GLOBALCONFIG':
            return imsandgraymailconfigGlobalconfig(self._get_sess())
        else:
            raise ccb.IafCliError('Feature is not activated. Please make '
                                  'sure that featurekey is valid and the feature is bundled')


class imsandgraymailconfigGraymail(ccb.IafCliConfiguratorBase):
    _newline = 2

    def __init__(self, session, output):
        super(imsandgraymailconfigGraymail, self).__init__(session)
        self._output = output

        print self._output


    def setup(self, input_dict = None, **kwargs):
        """
        esa-admin-cli> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> graymail

        Graymail Detection: Disabled

        Choose the operation you want to perform:
        - SETUP - Configure Graymail.
        []> setup

        Would you like to use Graymail Detection? [Y]>

        Would you like to enable automatic updates for Graymail engine? [Y]>

        Graymail Safe Unsubscribe: Disabled
        Would you like to use Graymail Safe Unsubscribe? [Y]>
        """
        if 'batch_mode' in kwargs and kwargs['batch_mode']:
            batch_cmd = 'imsandgraymailconfig graymail setup '
            params = []
            if 'use_graymail_detection' in kwargs and ynd.is_yes(kwargs['use_graymail_detection']):
                params.append('enable')
                if 'use_graymail_safe_unsubscribe' in kwargs:
                    if ynd.is_yes(kwargs['use_graymail_safe_unsubscribe']):
                        params.append('--unsubscription_enabled')
                        params.append('1')
                    else:
                        params.append('--unsubscription_enabled')
                        params.append('0')

                if 'enable_automatic_updates' in kwargs:
                    if ynd.is_yes(kwargs['enable_automatic_updates']):
                        params.append('--autoupdate_enabled')
                        params.append('1')
                    else:
                        params.append('--autoupdate_enabled')
                        params.append('0')
            else:
                params.append('disable')
            batch_cmd += ' '.join(params)
            self._info('BATCH COMMAND to execute: %s' % batch_cmd)
            self._to_the_top(1)
            self.clearbuf()
            self._writeln(batch_cmd)
            self._wait_for_prompt()
            return self.getbuf()
        else:
            param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
            param_map['use_graymail_detection'] = ['use Graymail Detection', DEFAULT]
            param_map['enable_automatic_updates'] = ['enable automatic updates for Graymail engine',
                                                 DEFAULT]
            param_map['use_graymail_safe_unsubscribe'] = ['use Graymail Safe Unsubscribe', YES]
            param_map['sure_you_want_to_disable'] = ['sure you want to disable', YES]
            param_map['license_agreement'] = ['license agreement?', YES]
            param_map.update(input_dict or kwargs)

            self._query_response('SETUP')
            self._process_input(param_map)

    def is_enabled(self):
        """
        Looks for Graymail Detection: Disabled/Enabled string under imsandgraymailconfig -> graymail command's output
        :return: True/False
        """
        self._to_the_top(self._newline)
        return True if self._output.lower().find('graymail detection: enabled') > 0 else False


class imsandgraymailconfigMultiscan(ccb.IafCliConfiguratorBase):

    _newline = 2

    def __init__(self, session, output):
        super(imsandgraymailconfigMultiscan, self).__init__(session)
        self._output = output

        print self._output

    def setup(self, input_dict = None, **kwargs):
        """
        esa-admin-cli> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> multiscan

        IronPort Intelligent Multi-Scan: Disabled


        Choose the operation you want to perform:
        - SETUP - Edit Intelligent Multi-Scan settings.
        []> setup

        IronPort Intelligent Multi-Scan scanning: Disabled
        Would you like to use IronPort Intelligent Multi-Scan scanning? [Y]>

        Would you like to enable regional scanning? [N]>
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_ims_scanning'] = ['use IronPort Intelligent Multi-Scan scanning', DEFAULT]
        param_map['confirm_disable'] = ['Are you sure you want to disable', DEFAULT]
        param_map['enable_regional_scanning'] = ['enable regional scanning', DEFAULT]
        param_map['region'] = ['Choose your region', DEFAULT]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        self._process_input(param_map)

    def is_enabled(self):
        """
        Looks for Multi-Scan: Disabled/Enabled string in imsandgraymailconfig -> multiscan command's output
        :return: True/False
        """
        self._to_the_top(self._newline)
        return True if self._output.lower().find('multi-scan: enabled') > 0 else False


class imsandgraymailconfigGlobalconfig(ccb.IafCliConfiguratorBase):
    _newline = 1

    def setup(self, input_dict = None, **kwargs):
        """
        vm30esa0014.ibqa> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> globalconfig

        Choose the operation you want to perform:
        - SETUP - Configure Common Global settings
        []> setup

        Increasing the following size settings may result in decreased performance. Please consult documentation for size recommendations based on your environment.

        Never scan message larger than: (Add a trailing K for kilobytes, M for megabytes, or no letters for bytes.)
        [1M]>

        Always scan message smaller than: (Add a trailing K for kilobytes, M for megabytes, or no letters for bytes.)
        [512K]>

        Timeout for Scanning Single Message(in seconds):
        [60]>
        """
        if 'batch_mode' in kwargs and kwargs['batch_mode']:
            batch_cmd = 'imsandgraymailconfig globalconfig setup '
            params = []
            if 'always_scan_message_smaller_than' in kwargs:
                params.append('--advisory_scan_size')
                params.append(kwargs['always_scan_message_smaller_than'])

            if 'dont_scan_message_larger_than' in kwargs:
                params.append('--max_msg_size')
                params.append(kwargs['dont_scan_message_larger_than'])

            if 'single_message_scanning_timeout' in kwargs:
                params.append('--scan_timeout')
                params.append(kwargs['single_message_scanning_timeout'])

            batch_cmd += ' '.join(params)
            self._info('BATCH COMMAND to execute: %s' % batch_cmd)
            self._to_the_top(1)
            self.clearbuf()
            self._writeln(batch_cmd)
            self._wait_for_prompt()
            return self.getbuf()
        else:
            param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
            param_map['dont_scan_message_larger_than'] = ['Never scan message larger than', DEFAULT]
            param_map['confirm_message_scanning_size'] = ['Are you sure that you want this set', DEFAULT]
            if 'confirm_message_scanning_size' not in kwargs:
                param_map['re_enter_message_scanning_size'] = ['Never scan message larger than', DEFAULT]
            else:
                if ynd.is_no(kwargs['confirm_message_scanning_size']):
                    param_map['re_enter_message_scanning_size'] = ['Never scan message larger than', DEFAULT]
            param_map['always_scan_message_smaller_than'] = ['Always scan message smaller than',
                                                             DEFAULT]
            param_map['single_message_scanning_timeout'] = ['Timeout for Scanning Single Message',
                                                            DEFAULT]
            param_map.update(input_dict or kwargs)

            self._query_response('SETUP')
            self._process_input(param_map)
