#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/licensesmart.py#1 $
# $DateTime: 2020/03/05 19:45:32 $
# $Author: sarukakk $

"""
SARF CLI command: smartlicense
"""
import re
import time

import clictorbase as ccb
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliError, IafCliParamMap, IafCliConfiguratorBase, IafUrlError
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_no

class licensesmart(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('license_smart')
        return self

    def enable(self):
        self._query_response('ENABLE')
        self._expect(['Type "Y" if you want to continue, or type "N"',], timeout=5)
        self._writeln('Y')
        self._to_the_top(1)

    def smartlicense_verify_menu_items(self, menu_item):
        self._to_the_top(1)
        self._writeln('license_smart')
        output = self._read_until(self._sub_prompt_user_match)
        menu_exists = re.search(menu_item, output)
        self._to_the_top(1)
        if menu_exists:
            self._debug("Menu Item {} exists under license smart command".format(menu_item))
            return True
        else:
            self._debug("Menu Item {} does not exists under license smart command".format(menu_item))
            return False

    def register(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command=self._get_prompt())
        param_map['reregister'] = ['Reregister this product instance', DEFAULT]
        param_map['token'] = ['Enter token to register the product', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('REGISTER')
        return self._process_input(param_map)

    def reregister(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command=self._get_prompt())
        param_map['remove_register'] = ['remove the existing product instance from Smart Software Manager',
                                       NO_DEFAULT]
        param_map['token'] = ['Enter token to register the product', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('REREGISTER')
        return self._process_input(param_map)

    def deregister(self):
        self._query_response('DEREGISTER')
        self._expect(['deregister the product instance from the CSSM',], timeout=5)
        self._writeln('YES')
        self._to_the_top(1)

    def renewid(self):
        self._query_response('RENEW_ID')
        self._to_the_top(1)

    def renewauth(self):
        self._query_response('RENEW_AUTH')
        self._to_the_top(1)

    def summary(self):
        self._query_response('SUMMARY')
        summary_output = self._read_until('Choose the operation')
        summary_dict = {}
        entl_msg = 'There are no active licenses to display'

        feature_list = ['Mail Handling',
            'Content Security Management Config Manager',
            'Content Security Management Web Reporting',
            'Content Security Management Master ISQ',
            'Content Security Management Centralized Tracking',
            'Content Security Management Centralized Reporting',
         ]

        status_lines = summary_output.split('\n')
        if summary_output.find(entl_msg) == -1:
            for line in range(0, len(status_lines)):
                for feature in feature_list:
                    if feature in status_lines[line]:
                        summary_dict[feature] = {}
                        license_status = re.search(r'([\w\s\-]+)',status_lines[line]).group(1)
                        license_status = re.split(" ", license_status.strip())[-1]
                        if license_status == 'Eval':
                             license_status = 'Eval'
                        elif license_status == 'In':
                             license_status = 'In Compliance'
                        elif license_status == 'Not':
                             license_status = 'Not requested'
                        elif license_status == 'Of':
                             license_status = 'Out Of Compliance'
                        else:
                             license_status = 'Request in progress'
                        summary_dict[feature]['Status'] = license_status

        else:
            summary_dict['Status'] = entl_msg
        self._debug(summary_dict)
        self._to_the_top(1)
        return summary_dict

    def url(self, transport_connection, gateway_url=None):

        self._query_response('URL')

        direct_url_msg = "Transport settings will be updated after commit"
        idx = self._query('Choose from the following menu options',
                          'Please deregister product to edit transport settings')
        transport_dict = {'DIRECT':1,'TRANSPORT_GATEWAY':2}

        if idx == 1:
            self._debug("The product is in registered state deregister the product")
            raise ConfigError, "Failed to configure URL, product in registered mode.Deregister the product"

        if idx == 0:
            for key,val in transport_dict.items():
                if transport_connection.lower() == key.lower():
                    self._writeln(val)
                    if transport_connection.lower() == 'direct':
                        self._expect(direct_url_msg)
                        self._debug("Transport Settings Changed to Direct Sucessfully")
                    if transport_connection.lower() == 'transport_gateway':
                        if gateway_url != None:
                            self._expect('Enter the gateway URL to connect')
                            try:
                                self._writeln(gateway_url)
                                self._expect(['Transport settings will be updated after commit',], timeout=5)
                                self._debug("Transport Settings Changed to gateway URL {} Successfully".format(gateway_url))
                            except ccb.IafUrlError:
                                self._to_the_top(1)
	                        raise ccb.IafUrlError("Entered Invalid Gateway URL: {}".format(gateway_url))

        self._to_the_top(1)

    def _status_key_val_parse(self, data):
        (key, value) = re.split(r':\s', data)
        key = key.strip()
        value = value.strip()
        return key, value

    def status(self):

        self._query_response('STATUS')

        try:
            self.full_status_output = self._read_until('Choose the operation')
            if(self.full_status_output.lower().find('enabled')):
                self._debug("Smartlicense Status Enabled")
        except:
            self.full_status_output = self._read_until('Choose the operation', timeout=120)
            self._debug(self.full_status_output)

        self.full_status_output = self.full_status_output.lower()
        self.smart_licensing_status = {}

        #Fetching registration expire date
        if 'registration expires' in self.full_status_output:
            self.smart_licensing_status.update({'registration expires on':''})
            reg_expire_on = re.search(r'registration expires(.*)license authorization status',
                                      self.full_status_output,re.DOTALL | re.MULTILINE).group(1)
            reg_expire_date = re.search(r'(\d+\s\w+\s.*\d{2}:\d{2})', reg_expire_on).group(1)
            self.smart_licensing_status['registration expires on'] = reg_expire_date.strip()

        self.full_status_output = self.full_status_output.split('\n')

        for data in self.full_status_output:
            match_url = re.match(r'[(./]', data, re.I)
            if match_url:
                self.smart_licensing_status.update({'transport_url':data.strip("()\r")})
            match = re.match(r'([\w\s]+):\s+\w+', data, re.I)
            if match:
                status_output_key, status_output_val = self._status_key_val_parse(data.strip())

                #Extracting only registration status and ommiting the date. Which is not required
                if 'registration expires' in status_output_val:
		    dateformat = re.search(r'([(]\s\d+\s\w+\s.*\d{2}:\d{2}\s[)])', status_output_val).group(1)
                    status_output_val = status_output_val.replace('registration expires',' ')
                    status_output_val = status_output_val.replace(dateformat,' ')
                    status_output_val = status_output_val.strip()

                #Extracting only license authorization status and ommitting date. Which is not required
                if 'out_of_compliance' in status_output_val or 'authorized' in status_output_val:
                    status_output_val = self._status_parse_replace_date(status_output_val, ' ')

                if 'authorized' in status_output_val:
                    status_output_val = status_output_val.rsplit(' ',1)[0].strip()

                self.smart_licensing_status.update({status_output_key:status_output_val})
                #changing the output with proper key name
                if status_output_key == 'expires on':
                    self.smart_licensing_status['authorization expires on'] = self.smart_licensing_status.pop('expires on')
                if status_output_key == 'smart licensing is':
                    self.smart_licensing_status['smart licensing status'] = self.smart_licensing_status.pop('smart licensing is')

        self._status_parse_auth_register_renewal_date()
        self._to_the_top(1)
        return self.smart_licensing_status

    def _status_parse_auth_register_renewal_date(self):
        #Splitting license authorization renewal field to fetch the renewal date.
        if 'no communication attempted' not in self.smart_licensing_status['last authorization renewal attempt']:
            self.smart_licensing_status.update({'last authorization renewal attempt date':''})
            last_auth_renew = self.smart_licensing_status['last authorization renewal attempt']
            auth_renew_status, auth_renew_date = re.split(r'on', last_auth_renew)
            self.smart_licensing_status['last authorization renewal attempt'] = auth_renew_status.strip()
            self.smart_licensing_status['last authorization renewal attempt date'] = auth_renew_date.strip()

        #Splitting registration renewal field to fetch renewal date
        if 'last registration renewal attempt status' in self.smart_licensing_status:
            self.smart_licensing_status.update({'last registration renewal attempt date':''})
            last_reg_renew = self.smart_licensing_status['last registration renewal attempt status']
            reg_renew_status, reg_renew_date = re.split(r'on', last_reg_renew)
            self.smart_licensing_status['last registration renewal attempt status'] = reg_renew_status.strip()
            self.smart_licensing_status['last registration renewal attempt date'] = reg_renew_date.strip()

    def _status_parse_replace_date(self, val, replace_val):
        return_val = val.replace(re.search(r'([(]\s\d+\s\w+\s.*\d{2}:\d{2}\s[)])',
                                 val).group(1), replace_val).strip()
        return return_val

    def get_license_list_available_for_request(self):
        features_dict={}

        self.clearbuf()
        self._writeln('REQUESTSMART_LICENSE')
        self._expect(['There are no licenses for activation', 'Enter the appropriate license'])
        entitlement_output = self.getbuf()
        if self._expectindex == 0:
            self._debug("There are no licenses for activation")
            self._to_the_top(1)
            return -1

        if self._expectindex == 1:
            lines = entitlement_output.split('\n')
            for line in lines:
                line = line.strip()
                match= re.match(r'(\d+)\.\s+(.*)', line, re.I)
                if match:
                    entitlement_name = re.search(r'(?<=\d.\s).+',line).group(0)
                    entitlement_numeric_val = re.search(r'(\d+).\s.*',line).group(1)
                    features_dict[entitlement_name] = entitlement_numeric_val.strip()

        self._to_the_top(2)
        self._debug(features_dict)
        return features_dict

    def get_license_list_releasesmart_license(self):
        features_dict={}

        self.clearbuf()
        self._writeln('RELEASESMART_LICENSE')
        self._expect(['There are no licenses for deactivation', 'Enter the appropriate license'])
        feature_list = ['Mail Handling',
            'Content Security Management Config Manager',
            'Content Security Management Web Reporting',
            'Content Security Management Master ISQ',
            'Content Security Management Centralized Tracking',
            'Content Security Management Centralized Reporting',
         ]
        entitlement_output = self.getbuf()
        print entitlement_output
        if self._expectindex == 0:
            self._debug("There are no licenses for deactivation")
            self._to_the_top(1)
            return -1

        if self._expectindex == 1:
            status_lines = entitlement_output.split('\n')
            for line in range(0, len(status_lines)):
                for feature in feature_list:
                    if feature in status_lines[line]:
                        features_dict[feature] = {}
                        license_status = re.search(r'([\w\s]+)',status_lines[line+1]).group(1)
                        features_dict[feature] = license_status.strip()
        self._to_the_top(2)
        self._debug(features_dict)
        return features_dict

    def requestsmart_entitlement(self, entitlement_list):
        self._info("Entitlements requested for activation: %s" % (entitlement_list))

        self.clearbuf()
        self._writeln('REQUESTSMART_LICENSE')
        self._expect(['There are no licenses for activation', 'Enter the appropriate license'])
        entitlement_output = self.getbuf()
        if self._expectindex == 0:
            raise ccb.IafCliValueError('Requested licenses are not '\
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
                raise ccb.IafCliValueError('Requested entitlements are not '\
                    'available for activation')
        self._to_the_top(1)

    def releasesmart_entitlement(self, entitlement_list):
        self._info("Entitlements requested for deactivation: %s" % (entitlement_list))

        self.clearbuf()
        self._writeln('RELEASESMART_LICENSE')
        self._expect(['There are no licenses for deactivation', 'Enter the appropriate license'])
        entitlement_output = self.getbuf()
        if self._expectindex == 0:
            raise ccb.IafCliValueError('Requested entitlements are not '\
                'available for deactivation')
            return -1
        if self._expectindex == 1:
            self._info(entitlement_output)

            entl_new_list = self._get_entitlement_list(entitlement_list, entitlement_output)
            if entl_new_list:
                self._info("Entitlements which will be deactivated are: %s" % entl_new_list)
                entl_new_list = ",".join(entl_new_list)
                self._writeln(entl_new_list)
                release_output = self._read_until('Choose the operation')
                if 'Product Base License which' in release_output:
                    raise ValueError("Product Base License which is requested by default"\
                        " and cannot be released")
            else:
                raise ccb.IafCliValueError('Requested entitlements are not '\
                    'available for deactivation')
        self._to_the_top(1)

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
        []>requestsmart_entitlement

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
            match= re.match(r'(\d+)\.\s+(.*)', line, re.I)
            if match:
                entitlement_numeric_val, entitlement_name = match.groups()
                entitlement_name = entitlement_name.strip()
                entitlement_dict[entitlement_name] = entitlement_numeric_val.strip()

        entl_new_list = [entitlement_dict[entl_name] for entl_name \
                         in entitlement_list if entl_name in entitlement_dict]
        return entl_new_list
