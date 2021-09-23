#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/samlconfig.py#1 $
# $DateTime: 2020/05/25 00:19:30 $
# $Author: sarukakk $

""" SARF ctor class for samlconfig CLI"""


from clictorbase import REQUIRED, DEFAULT, IafCliParamMap, IafCliConfiguratorBase
from clictorbase import IafCliError, IafUnknownOptionError
from sal.containers.yesnodefault import YES, NO, is_yes
from sal.deprecated.expect import REGEX, EXACT

class samlconfig(IafCliConfiguratorBase):
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('samlconfig')
        self._writeln('UILOGIN')
        return self

    def new(self, input_dict=None, **kwargs):
        self.new_lines = 3
        self._writeln('SP')
        self._writeln('NEW')
        self._query('Enter the SP profile Name')
        self._query_response(kwargs['sp_profile_name'])
        self._query('Enter the SP Entity Id')
        self._query_response(kwargs['sp_entity_id'])
        self._query('Enter Assertion Consumer URL')
        if 'assertion_consumer_url' in kwargs:
            self._query_response(kwargs['assertion_consumer_url'])
        else:
            self._query_response(DEFAULT)
        self._query('operation you want to perform')
        self._query_response('PASTE')
        self._query('Please paste the SP Certificate')
        self._writeln(kwargs['sp_certificate'])
        self._sess.write("\x04")
        self._query('Please paste the SP Certificate Key')
        self._writeln(kwargs['sp_certificate_key'])
        self._sess.write("\x04")

        param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform')
        param_map['sp_certificate_passphrase'] = ['Enter the SP Certificate Passpharse', DEFAULT]
        param_map['sp_sign_request'] = ['Do you want to Sign Requests', DEFAULT]
        param_map['sp_sign_assertion_request'] = ['Do you want to Sign Assertion Requests', DEFAULT]
        param_map['sp_technical_contact_id'] = ['Enter the Technical Contact Id', REQUIRED]
        param_map['sp_organization_url'] = ['Enter the Organization URL', REQUIRED]
        param_map['sp_organization_name'] = ['Enter the Organization Name', REQUIRED]
        param_map['sp_organization_display_name'] = ['Enter the Organization Display Name', REQUIRED]

        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map._map.keys():
                actual_dict[key] = kwargs[key]
        param_map.update(input_dict or actual_dict)
        self._process_input(param_map, do_restart=False)
        self._writeln('IDP')
        self._writeln('NEW')
        self._writeln(kwargs['idp_profile_name'])
        self._query('Paste the IDP Metadata XML')
        if kwargs['idp_metadata_action'].lower() == 'paste':
            self._writeln('PASTE')
            self._query('Please paste the IDP Metadata XML')
            self._writeln(kwargs['idp_metadata_xml'])
            self._sess.write("\x04")    # ^D (CTRL-D)
        elif kwargs['idp_metadata_action'].lower() == 'enter':
            self._writeln('ENTER')
            self._query('Enter the IDP Entiy Id')
            self._writeln(kwargs['idp_entity_id'])
            self._query('Enter the IDP SSO Url')
            self._writeln(kwargs['idp_sso_url'])
            self._query('Please paste the IDP Certificate')
            self._writeln(kwargs['idp_certificate'])
            self._sess.write("\x04")    # ^D (CTRL-D)
        else:
            raise IafUnknownOptionError("Unknown option [%s] passed for " \
                    "[idp_metadata_action] paramter" % (kwargs['idp_metadata_action']))
        self._to_the_top(self.new_lines)

    def edit_sp(self, input_dict=None, **kwargs):
        self.new_lines = 2
        self._query_response('SP')
        self._query_response('EDIT')

        self._query('Enter the SP profile Name')
        if 'sp_profile_name' in kwargs:
            self._query_response(kwargs['sp_profile_name'])
        else:
            self._query_response(DEFAULT)

        self._query('Enter the SP Entity Id')
        if 'sp_entity_id' in kwargs:
            self._query_response(kwargs['sp_entity_id'])
        else:
            self._query_response(DEFAULT)

        self._query('Enter Assertion Consumer URL')
        if 'assertion_consumer_url' in kwargs:
            self._query_response(kwargs['assertion_consumer_url'])
        else:
            self._query_response(DEFAULT)

        param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform')

        self._query('Choose the operation you want to perform')
        if 'sp_certificate_edit_option' in kwargs:
            self._query_response(kwargs['sp_certificate_edit_option'].upper())
            if kwargs['sp_certificate_edit_option'].lower() == 'replace':
                self._query('operation you want to perform')
                self._query_response('PASTE')
                self._query('Please paste the SP Certificate')
                self._writeln(kwargs['sp_certificate'])
                self._sess.write("\x04")
                self._query('Please paste the SP Certificate Key')
                self._writeln(kwargs['sp_certificate_key'])
                self._sess.write("\x04")

                param_map['sp_certificate_passphrase'] = ['Enter the SP Certificate Passpharse', DEFAULT]

            param_map['sp_sign_request'] = ['Do you want to Sign Requests', DEFAULT]
            param_map['sp_sign_assertion_request'] = ['Do you want to Sign Assertion Requests', DEFAULT]
            param_map['sp_technical_contact_id'] = ['Enter the Technical Contact Id', DEFAULT]
            param_map['sp_organization_url'] = ['Enter the Organization URL', DEFAULT]
            param_map['sp_organization_name'] = ['Enter the Organization Name', DEFAULT]
            param_map['sp_organization_display_name'] = ['Enter the Organization Display Name', DEFAULT]
            param_map['idp_profile_name'] = ['Enter the IDP Profile Name', DEFAULT]
            actual_dict = {}
            for key in kwargs.keys():
                if key in param_map._map.keys():
                    actual_dict[key] = kwargs[key]
            param_map.update(input_dict or actual_dict)
            self._process_input(param_map)
        else:
            raise IafCliError("'sp_certificate_option' parameter is mandatory. " \
                    "Allowed values are: USE or REPLACE")

    def edit_idp(self, input_dict=None, **kwargs):
        """keyword to edit the idp settings
        idp_certificate_action:
          *new :  for the new addition of idp_ceritificate
          *use:  Use the existing ceritificate configured
          *replace: replace the existing options with the new options provided
        idp_certificate_action: new is the default certificate action
        """
        self.new_lines = 3
        if not kwargs.has_key('idp_certificate_action'):
            kwargs['idp_certificate_action'] = 'new'

        self._query_response('IDP')
        self._query_response('EDIT')

        self._query('Enter the IDP Profile Name')
        if 'idp_profile_name' in kwargs:
            self._query_response(kwargs['idp_profile_name'])
        else:
            self._query_response(DEFAULT)

        self._query('Choose the operation you want to perform')
        if 'idp_metadata_edit_action' in kwargs:
            self._query_response(kwargs['idp_metadata_edit_action'].upper())
            if kwargs['idp_metadata_edit_action'].lower() == 'paste':
                self._query('Please paste the IDP Metadata XML')
                if 'idp_metadata_xml' in kwargs:
                    self._writeln(kwargs['idp_metadata_xml'])
                    self._sess.write("\x04")    # ^D (CTRL-D)
                else:
                    raise IafCliError("'idp_metadata_xml' paramter is required")
            elif kwargs['idp_metadata_edit_action'].lower() == 'enter':
                self._query('Enter the IDP Entiy Id')
                if 'idp_entity_id' in kwargs:
                    self._writeln(kwargs['idp_entity_id'])
                else:
                    self._writeln(DEFAULT)

                self._query('Enter the IDP SSO Url')
                if 'idp_sso_url' in kwargs:
                    self._writeln(kwargs['idp_sso_url'])
                else:
                    raise IafCliError("'idp_sso_url' parameter is required")

                if kwargs['idp_certificate_action'] == 'new' or kwargs['idp_certificate_action'] == 'replace':
                    if kwargs['idp_certificate_action'] == 'replace':
                        self._query_response('REPLACE')
                    self._query('Please paste the IDP Certificate')

                    if 'idp_certificate' in kwargs:
                        self._writeln(kwargs['idp_certificate'])
                        self._sess.write("\x04")    # ^D (CTRL-D)
                    else:
                        raise IafCliError("'idp_certificate' parameter is required")
                if kwargs['idp_certificate_action'].lower() == 'use':
                    self._query_response('USE')
            else:
                raise IafUnknownOptionError("Unknown option [%s] passed for " \
                        "[idp_metadata_edit_action] paramter" % (kwargs['idp_metadata_edit_action']))
        else:
            raise IafCliError("'idp_metadata_edit_action' parameter is mandatory. " \
                    "Allowed values are: PASTE or ENTER")
        self._to_the_top(self.new_lines)

    def delete(self):
        self.newlines = 2
        self._query_response('SP')
        self._query_response('DELETE')
        self._query_response('IDP')
        self._query_response('DELETE')
        self._to_the_top(self.newlines)

