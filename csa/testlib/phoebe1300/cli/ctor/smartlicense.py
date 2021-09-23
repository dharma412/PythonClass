#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/smartlicense.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: smartlicense
"""
import re
import time
import pprint

import clictorbase as ccb
from clictorbase import REQUIRED, DEFAULT, IafCliError, IafCliParamMap, IafCliConfiguratorBase
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_no


class smartlicense(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('smartlicense')
        return self

    def enable(self):
        self._query_response('ENABLE')
        self._to_the_top(1)

    def register(self, token_id=REQUIRED):
        self._query_response('REGISTER')
        self._query_response(token_id)
        self._to_the_top(1)

    def deregister(self):
        self._query_response('DEREGISTER')
        self._expect(['deregister the product instance from the CSSM', ], timeout=5)
        self._writeln('YES')
        self._to_the_top(1)

    def renewcert(self):
        self._query_response('RENEWCERT')
        self._to_the_top(1)

    def renewauth(self):
        self._query_response('RENEWAUTH')
        self._to_the_top(1)

    def reregister(self, token_id=REQUIRED):
        self._query_response('REREGISTER')
        self._query_response(token_id)
        self._to_the_top(1)

    def show_entitlement_status(self):
        self._query_response('SHOW_ENTITLEMENT_STATUS')
        output = self._read_until()

        dict = {}
        feature_list = ['Incoming Mail Handling', 'Sophos', 'McAfee', 'Outbreak Filters',
                        'File Analysis', 'File Reputation', 'IronPort Anti-Spam', 'Cloudmark SP',
                        'Delivery', 'IronPort Email Encryption', 'Graymail Safe Unsubscription',
                        'IronPort Image Analysis', 'Intelligent Multi-Scan']

        status_lines = output.split('\n')

        for line in range(0, len(status_lines)):
            for feature in feature_list:
                if feature in status_lines[line]:
                    dict[feature] = {}
                    expiry_date = re.search(r'.*(\d{4}[-].*\d{2})', status_lines[line + 1]).group(1)
                    license_count = re.search(r'.*(\d+)', status_lines[line + 1]).group(1)
                    license_status = re.search(feature + r'(.*)', status_lines[line]).group(1)
                    dict[feature]['Status'] = license_status.strip()
                    dict[feature]['ExpiryDate'] = expiry_date.strip()
                    dict[feature]['Count'] = license_count.strip()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dict)
        return dict

    def transport_setup(self, transport_connection, gateway_url=None):

        self._query_response('TRANSPORT_SETUP')

        self._expect(['Choose from the following menu options', ], timeout=5)
        transport_dict = {'DIRECT': 1, 'TRANSPORT_GATEWAY': 2}

        for key, val in transport_dict.items():
            if transport_connection.lower() == key.lower():
                self._writeln(transport_dict[key])
                if transport_connection.lower() == 'transport_gateway':
                    if gateway_url != None:
                        self._expect('Enter the gateway URL to connect')
                        self._writeln(gateway_url)

                        try:
                            idx = self._query('Gateway URL is not Valid')
                            if idx == 0:
                                raise ValueError
                        except ValueError:
                            print "FAIL - Entered Invalid Gateway URL: " + gateway_url
                            raise ValueError("Gateway URL is not Valid")
                        except:
                            print "PASS - Entered Valid Gateway URL: " + gateway_url
        self._to_the_top(1)

    def _status_key_val_parse(self, data):
        (key, value) = re.split(r':\s', data)
        return key, value

    def _status_licenses_details_parse(self):
        licenses = re.findall(r"\w+\s\(\w+\)", self.license_usage)
        license_dict = {}
        for i in range(0, len(licenses)):
            license_dict.update({licenses[i]: {}})

            if i == len(licenses) - 1:
                license_index = re.search(re.escape(licenses[i]) + '(.*)',
                                          self.license_usage, re.DOTALL | re.MULTILINE).group(1)
            else:
                license_index = re.search(re.escape(licenses[i]) + '(.*)' + re.escape(licenses[i + 1]),
                                          self.license_usage, re.DOTALL | re.MULTILINE).group(1)
            license_data = license_index.strip().split('\n')
            for data in license_data:
                if "application" not in data:
                    license_key, license_val = self._status_key_val_parse(data)
                    license_dict[licenses[i]][license_key.strip()] = license_val.strip()
        self.smart_license['License Usage'].update(license_dict)

    def status(self):

        self._query_response('STATUS')

        try:
            self.full_status_output = self._read_until()
            if (self.full_status_output.find('ENABLED')):
                print "Smartlicense Status Enabled"
        except:
            self.full_status_output = self._read_until(timeout=120)
            print self.full_status_output

        self.smart_license = {
            'Smart Licensing Status': {
                'Enabled': False,
                'Registration': {},
                'License Authorization': {},
                'Evaluation Period': {},
            },
            'License Usage': {
                'License Authorization Status': {}
            },
            'Product Information': {
                'UDI': {}
            },
            'Agent Version': {
                'Smart Agent for Licensing': {}
            },
            'Transport Configuration': {},
        }

        # below block fetches the license status Enabled or disabled
        license_status = re.search(r'Smart Licensing is (\S+)', self.full_status_output).group(1)
        if license_status == 'ENABLED':
            self.smart_license['Smart Licensing Status']['Enabled'] = True

        # Registration Block
        registration = re.search(r'Registration:(.*)License Authorization:', self.full_status_output,
                                 re.DOTALL | re.MULTILINE).group(1)
        registration_data = registration.strip().split('\n')
        for data in registration_data:
            reg_key, reg_val = self._status_key_val_parse(data)
            self.smart_license['Smart Licensing Status']['Registration'][
                reg_key.strip()] = reg_val.strip()

        # License Authorization communication Block
        authorization = re.search(
            r'License Authorization:(.*)Evaluation Period:', self.full_status_output,
            re.DOTALL | re.MULTILINE).group(1)

        authorization_data = authorization.strip().split('\n')
        for data in authorization_data:
            auth_key, auth_val = self._status_key_val_parse(data)
            self.smart_license['Smart Licensing Status']['License Authorization'][
                auth_key.strip()] = auth_val.strip()

        # Below code fetches License authorization status
        self.license_usage = re.search(
            r'License Usage(.*)Product Information', self.full_status_output,
            re.DOTALL | re.MULTILINE).group(1)

        license_auth = re.search(r'License Authorization Status:(\s.*)', self.license_usage).group(1)
        self.smart_license['License Usage']['License Authorization Status'] = license_auth.strip()

        # Licese Usage block. Returns list of licenses and their details
        if ("AUTHORIZED" in license_auth.strip()) or ("OUT_OF_COMPLIANCE" in license_auth.strip()):
            self._status_licenses_details_parse()

        # Evaluation period Block
        evaluation_period = re.search(
            r'Evaluation Period:(.*)License Usage', self.full_status_output,
            re.DOTALL | re.MULTILINE).group(1)

        evaluation_period_data = evaluation_period.strip().split('\n')
        for data in evaluation_period_data:
            eval_key, eval_val = self._status_key_val_parse(data)
            self.smart_license['Smart Licensing Status']['Evaluation Period'][
                eval_key.strip()] = eval_val.strip()

        # Product Information Block
        prod_info = re.search(r'Product Information(.*)Agent Version', self.full_status_output,
                              re.DOTALL | re.MULTILINE).group(1)
        pid = re.sub(r'[=|\n\r]', r'', prod_info)
        prod_key, prod_val = self._status_key_val_parse(pid)
        self.smart_license['Product Information'][prod_key.strip()] = prod_val.strip()

        # Agent version block
        agent_version = re.search(r'Smart Agent for Licensing:(\s\d\.?.*)',
                                  self.full_status_output).group(1)

        self.smart_license['Agent Version']['Smart Agent for Licensing'] = agent_version.strip()

        # Transport Configuration block
        transport_config = re.search(r'Transport Configuration(.*)', self.full_status_output,
                                     re.DOTALL | re.MULTILINE).group(1)
        transport_parse = re.sub(r'[=|\n\r]', r'', transport_config)
        transport_data = transport_parse.strip().split('URL:')
        for data in transport_data:
            if "Mode" in data:
                transport_key, transport_val = self._status_key_val_parse(data)
                self.smart_license['Transport Configuration'][transport_key.strip()] = transport_val.strip()
            else:
                self.smart_license['Transport Configuration']['URL'] = data.strip()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.smart_license)
        return self.smart_license

    def activate(self, entitlement_list):
        self._info("Entitlements requested for activation: %s" % (entitlement_list))

        self.clearbuf()
        self._writeln('activate_entitlement')
        self._expect(['There are no entitlements for activation', 'Enter the appropriate entitlement'])
        entitlement_output = self.getbuf()
        if self._expectindex == 0:
            raise ccb.IafCliValueError('Requested entitlements are not ' \
                                       'available for activation')
            return -1
        if self._expectindex == 1:
            self._info(entitlement_output)

            entl_new_list = self._get_entitlement_list(entitlement_list, entitlement_output)

            if entl_new_list:
                self._info("Entitlements which will be activated are: %s" % entl_new_list)
                entl_new_list = ",".join(entl_new_list)
                self._writeln(entl_new_list)
                self._to_the_top(1)
            else:
                raise ccb.IafCliValueError('Requested entitlements are not ' \
                                           'available for activation')

    def deactivate(self, entitlement_list):
        self._info("Entitlements requested for deactivation: %s" % (entitlement_list))

        self.clearbuf()
        self._writeln('deactivate_entitlement')
        self._expect(['There are no entitlements for deactivation', 'Enter the appropriate entitlement'])
        entitlement_output = self.getbuf()
        if self._expectindex == 0:
            raise ccb.IafCliValueError('Requested entitlements are not ' \
                                       'available for deactivation')
            return -1
        if self._expectindex == 1:
            self._info(entitlement_output)

            entl_new_list = self._get_entitlement_list(entitlement_list, entitlement_output)

            if entl_new_list:
                self._info("Entitlements which will be deactivated are: %s" % entl_new_list)
                entl_new_list = ",".join(entl_new_list)
                self._writeln(entl_new_list)
                self._to_the_top(1)
            else:
                raise ccb.IafCliValueError('Requested entitlements are not ' \
                                           'available for deactivation')

    def _get_entitlement_list(self, entitlement_list, entitlement_output):
        """
        auxiliary function for activate and deactivate.
        It reads the CLI output, creates a dictionary with entitlement name
        as key and entitlement number as value as:
        a)the pairing of entitlement number and name is dynamic
        b)CLI can accept only numeric value as input
        E.g:
        In below CLI output,
        Key  --> VOF (entitlement name)
        Value --> 1 (entitlement number)
        []> activate_entitlement

          Tag Name           Status
        --------------------------------------
        1. Outbreak Filters   AVAILABLE

        The calling function can pass any entitlement name(s) for activation
        or deactivation without checking if it is available for activation/
        deactivation or not, this function takes care of creating a new list
        of entitlement numbers including only those that are available for
        activation/deactivation
        """
        entitlement_dict = {}

        entitlement_data = entitlement_output.split('\n')
        for line in entitlement_data:
            line = line.strip()
            line1 = line.rsplit(' ', 1)[0]
            match = re.match(r'(\d+)\.\s+(.*)', line1, re.I)
            if match:
                entitlement_numeric_val, entitlement_name = match.groups()
                entitlement_name = entitlement_name.strip()
                entitlement_dict[entitlement_name] = entitlement_numeric_val.strip()

        entl_new_list = [entitlement_dict[entl_name] for entl_name \
                         in entitlement_list if entl_name in entitlement_dict]
        return entl_new_list
