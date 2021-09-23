#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/encryptionconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: encryptionconfig
"""
from sal.containers import cfgholder
from sal.containers.yesnodefault import YES, NO, is_yes
import clictorbase

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT
EXACT = clictorbase.EXACT


class encryptionconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    class ProvisionError(clictorbase.IafCliError): pass

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Unable to provision profile', EXACT): self.ProvisionError,
        })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['use_pxe'] = ['use PXE Email Encryption?', REQUIRED]
        param_map['confirm_disable'] = ['want to disable', YES]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['max_enc_msg_size'] = ['Maximum message size for encryption', DEFAULT]
        param_map['email_address'] = ['email address of the encryption account administrator', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def profiles(self):
        self._query_response('PROFILES')
        return encryptionconfigProfiles(self._get_sess())

    def provision(self, name=''):
        self._query_response('PROVISION')
        self._query_select_list_item(name)
        self._to_the_top(self.newlines)


class encryptionconfigProfiles(clictorbase.IafCliConfiguratorBase):
    """ encryptionconfig -> PROFILES """

    newlines = 2

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['type'] = ['Choose a key service', DEFAULT, True]
        param_map['name'] = ['name for this encryption profile', REQUIRED]
        param_map['alter_cisco_url'] = \
            ['alter the Cisco Registered Envelope Service URL?', DEFAULT]
        param_map['cisco_url'] = ['Please enter the new URL', DEFAULT]
        param_map['external_url'] = ['Please enter an external URL', REQUIRED]
        param_map['internal_url'] = ['Please enter an internal URL', REQUIRED]
        param_map['use_proxy'] = \
            ['use the configured key server proxy?', DEFAULT]
        param_map['algorithm'] = \
            ['enter the encryption algorithm', DEFAULT, True]
        param_map['enable_read_receipts'] = ['enable read receipts?', DEFAULT]
        param_map['security_level'] = \
            ['envelope security level', DEFAULT, True]
        param_map['enable_secure_reply'] = \
            ['enable "Secure Reply All"?', DEFAULT]
        param_map['enable_secure_forward'] = \
            ['enable "Secure Forward"?', DEFAULT]
        param_map['logo_url'] = \
            ['link for the envelope logo image', DEFAULT]
        param_map['max_sec_in_queue'] = ['message could remain queued', DEFAULT]
        param_map['fail_notification'] = \
            ['subject to use for failure notifications', DEFAULT]
        param_map['notif_tmpl'] = \
            ['Select a text notification template', DEFAULT, True]
        param_map['notif_html_tmpl'] = \
            ['Select an HTML notification template', DEFAULT, True]
        param_map['payload_url'] = \
            ['Configure the Payload Transport URL', DEFAULT]
        param_map['separate_url'] = \
            ['Enter a URL for payload transport', REQUIRED]
        param_map['env_filename'] = \
            ['file name of the envelope attached ', DEFAULT]
        param_map['assign_user'] = ['assign any user roles', DEFAULT]
        param_map['action'] = \
            ['Choose the operation you want to perform', DEFAULT]
        param_map['role'] = \
            ['Select one or more user role names', REQUIRED]
        param_map['display_language'] = \
            ['envelopes to be displayed in a language other than English', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, name):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        return encryptionconfigProfilesEdit(self._get_sess())

    def delete(self, name):
        self._query_response('DELETE')
        self._query_select_list_item(name)
        self._to_the_top(self.newlines)

    def print_profiles(self, raw=NO):
        """
        Returns a List of parsed data unless raw=True.
        """
        self._query_response('PRINT')
        self._query('\n')
        raw_out = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        if is_yes(raw):
            return raw_out
        return self._parse_print_out(raw_out)

    def clear(self):
        self._query_response('CLEAR')
        self._query_response(YES)
        self._to_the_top(self.newlines)

    def proxy(self, input_dict=None, **kwargs):
        _tmp = input_dict or kwargs
        _passwd = _tmp.pop('password', DEFAULT)
        param_map = \
            clictorbase.IafCliParamMap \
                (end_of_command='Please enter the proxy passphrase')
        param_map['type'] = ['Choose the type of proxy', DEFAULT, True]
        param_map['hostname'] = ['enter the proxy hostname', DEFAULT]
        param_map['port'] = ['enter the proxy port', DEFAULT]
        param_map['user'] = ['enter the proxy user', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('PROXY')
        self._process_input(param_map, do_restart=False)
        self._writeln(_passwd)
        self._to_the_top(self.newlines)

    def _parse_print_out(self, raw_out):
        """ Parses Print() commad output like:

            Profile Name         Key Service            Proxied     Provision Status
            ------------         -----------            -------     ----------------
            LocalKeyService      Encryption Appliance   No          N/A
            CiscoKeyService      Encryption Appliance   No          N/A
            Proxy: Not Configured


            Returns following stucture:
                [ {'key_service': 'Encryption Appliance',
                   'profile_name': 'LocalKeyService',
                   'proxied': 'No',
                   'proxy': 'Not Configured',
                   'provision_status': 'N/A'},
                  {'key_service': 'Encryption Appliance',
                   'profile_name': 'CiscoKeyService',
                   'proxied': 'No',
                   'provision_status': 'N/A',
                   'proxy': 'Not Configured',}
                ]
        """

        # Stip lines and remove blank lines
        raw_out = filter(lambda line: len(line) > 0,
                         map(lambda line: line.strip(),
                             raw_out.split('\n')))
        res_list = []
        data_lines = False
        for i, line in enumerate(raw_out):
            if line.strip().endswith('---'):
                data_lines = True
                # Fetch and normalize keys
                keys = map(lambda item: item.lower().strip().replace(' ', '_'),
                           filter(lambda item: len(item) > 0,
                                  raw_out[i - 1].split('  ')))
            elif line.startswith('Proxy: '):
                for indx, dic in enumerate(res_list):
                    res_list[indx]['proxy'] = line[len('Proxy: '):]

                break
            elif data_lines:
                # Fetch and normalize values
                values = map(lambda item: item.strip(),
                             filter(lambda item: len(item) > 0,
                                    line.strip().split('  ')))
                assert len(values) == 4, \
                    'Unable to parse configuration profile output'
                res_list.append(cfgholder.CfgHolder(dict(zip(keys, values))))
        return res_list


class encryptionconfigProfilesEdit(clictorbase.IafCliConfiguratorBase):
    """ encryptionconfig -> PROFILES -> EDIT """

    newlines = 3

    def name(self, new_name=DEFAULT):
        self._query_response('NAME')
        self._query_response(new_name)
        self._to_the_top(self.newlines)

    def external(self, url=DEFAULT):
        self._query_response('EXTERNAL')
        self._query_response(url)
        self._to_the_top(self.newlines)

    def internal(self, url=DEFAULT):
        self._query_response('INTERNAL')
        self._query_response(url)
        self._to_the_top(self.newlines)

    def proxy(self, use_proxy=DEFAULT):
        self._query_response('PROXY')
        self._query_response(use_proxy)
        self._to_the_top(self.newlines)

    def algorithm(self, algorithm=DEFAULT):
        self._query_response('ALGORITHM')
        self._query_select_list_item(algorithm)
        self._to_the_top(self.newlines)

    def payload(self, payload_url=DEFAULT, separate_url=DEFAULT):
        self._query_response('PAYLOAD')
        idx = self._query_select_list_item(payload_url)
        if idx == 3:
            self._query_response(separate_url)
        self._to_the_top(self.newlines)

    def receipt(self, enable=DEFAULT):
        self._query_response('RECEIPT')
        self._query_response(enable)
        self._to_the_top(self.newlines)

    def security(self, level=DEFAULT):
        self._query_response('SECURITY')
        self._query_select_list_item(level)
        self._to_the_top(self.newlines)

    def forward(self, enable=DEFAULT):
        self._query_response('FORWARD')
        self._query_response(enable)
        self._to_the_top(self.newlines)

    def replyall(self, enable=DEFAULT):
        self._query_response('REPLYALL')
        self._query_response(enable)
        self._to_the_top(self.newlines)

    def applet(self, suppress=DEFAULT):
        self._query_response('APPLET')
        self._query_response(suppress)
        self._to_the_top(self.newlines)

    def logo_url(self, logo_url=DEFAULT):
        self._query_response('URL')
        self._query_response(logo_url)
        self._to_the_top(self.newlines)

    def timeout(self, timeout=DEFAULT):
        self._query_response('TIMEOUT')
        self._query_response(timeout)
        self._to_the_top(self.newlines)

    def bounce_subject(self, subject=DEFAULT):
        self._query_response('BOUNCE_SUBJECT')
        self._query_response(subject)
        self._to_the_top(self.newlines)

    def filename(self, filename=DEFAULT):
        self._query_response('FILENAME')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def assign(self, action=None, role=DEFAULT):
        self._query_response('ASSIGN')
        self._query_response(action)
        self._query_response(role)
        self._to_the_top(self.newlines)

    def localized_envelope(self, display_language=DEFAULT):
        self._query_response('LOCALIZED_ENVELOPE')
        self._query_response(display_language)
        self._to_the_top(self.newlines)

    def default_locale(self, language=None):
        self._query_response('DEFAULT_LOCALE')
        self._query_select_list_item(language)
        self._to_the_top(self.newlines)
