#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/threatfeedconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""
SARF CLI command: threatfeedconfig
"""

import re
import clictorbase

from clictorbase import DEFAULT, REQUIRED
from sal.containers.yesnodefault import is_yes, YES, NO

class threatfeedconfig(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, operation):
        """
        :params:
            operation: Initial operation user wants perform. As of now only
                SOURCECONFIG sub-command is available but in future something new
                may come.
        :return: Returns the relavent class object depending upon the operation
            user wants to perform
        """
        self._writeln(self.__class__.__name__)
        if operation == 'setup':
            self._query_response('SETUP')
            return Setup(self._get_sess())
        if operation == 'sourceconfig':
            self._query_response('SOURCECONFIG')
            return SourceConfig(self._get_sess())
        elif operation == 'something_else':
            # Place holder for any future enhancement
            # self._query_response('SOMETHINGELSE')
            # return SomethingElse(self._get_sess())
            pass

class Setup(threatfeedconfig):

    def threatfeed_status(self,):
        state = "UNKNOWN"
        ENABLED = 'External Threat Feeds: Disabled'
        DISABLED = 'External Threat Feeds: Enabled'
        options = (ENABLED, DISABLED)

        state = options[self._query(*options)]
        self._to_the_top(5)
        if state == "UNKNOWN":
            return state.upper()
        state = state.split(":")[1].strip()
        if state == "Enabled":
           return True
        else:
           return False

    def setup(self, input_dict=None, **kwargs):

        """
        Threatfeed config  setup
        Parameters:
            use_etf - enable External Threat feeds: [YES or NO]
            license_agreement - confirm licence agreement [YES or NO]
        """
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_etf']                = ['Would you like to use External Threat Feeds', YES]
        param_map['confirm_disable']        = ['The system will no longer scan messages for threats using External Threat Feeds', NO]
        param_map['license_agreement']      = ['license agreement?', YES]
        param_map['custom_header']          = ['Do you want to add a custom header', NO]
        param_map['header_name']            = ['Enter the header name', DEFAULT]
        param_map['header_content']         = ['Enter the header content', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._process_input(param_map)

class SourceConfig(threatfeedconfig):
    newlines = 3

    def add(self, input_dict=None, **kwargs):
        self._query_response('ADD')
        return PollUrl(self._get_sess()).add_poll_url(**kwargs)

    def list(self):
        self._query_response('LIST')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw.strip()

    def detail(self, poll_url_source_name=None):
        self._query_response('DETAIL')
        self._query_response(poll_url_source_name)
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw.strip()

    def edit(self, **kwargs):
        self._query_response('EDIT')
        return PollUrl(self._get_sess()).edit_poll_url(**kwargs)

    def suspend(self, **kwargs):
        self._query_response('SUSPEND')
        return PollUrl(self._get_sess()).suspend_poll_url(**kwargs)

    def resume(self, **kwargs):
        self._query_response('RESUME')
        return PollUrl(self._get_sess()).resume_poll_url(**kwargs)

    def delete(self, **kwargs):
        self._query_response('DELETE')
        return PollUrl(self._get_sess()).delete_poll_url(**kwargs)

class PollUrl(SourceConfig):
    def add_poll_url(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['poll_url_source_name'] = ['Enter a name for the external threat feed source', REQUIRED]
        param_map['poll_url_source_description'] = [
            'Enter a description for the external threat feed source (optional)', REQUIRED]
        param_map['poll_url_host_name'] = ['Enter the hostname for the external threat feed source', REQUIRED]
        param_map['poll_url_polling_path'] = ['Enter the polling path for the external threat feed source',REQUIRED]
        param_map['poll_url_collection_name'] = ['Enter the collection name for the external threat feed source',
                                                 REQUIRED]
        param_map['poll_url_polling_interval'] = [
            'Enter the polling interval',DEFAULT]
        param_map['poll_url_feed_age'] = [
            'Enter the age of the threat feed',DEFAULT]
        param_map['poll_url_poll_segment'] = [
            'Enter the time span for each poll segment',DEFAULT]
        param_map['poll_url_use_https'] = ['Do you want to use HTTPS', REQUIRED]
        param_map['poll_url_polling_port'] = ['Enter the polling port', DEFAULT]
        param_map['poll_url_enable_proxy'] = ['Do you want to use a proxy server for the threat feed source? ', DEFAULT]
        param_map['poll_url_configure_credentials'] = [
            'Do you want to configure user credentials for the external threat feed source?', DEFAULT]
        cfg_credentials = kwargs['poll_url_configure_credentials']
        if  cfg_credentials.lower() == 'y':
            param_map['poll_url_auth_method'] = ['Basic Authentication', DEFAULT, 1]
            param_map['poll_url_auth_username'] = ['Enter the username', REQUIRED]
            param_map['poll_url_auth_password'] = ['assword', REQUIRED]

        param_map.update(input_dict or kwargs)
        self._query_response('POLL URL')
        return self._process_input(param_map)

    def detail_poll_url(self, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose ')
        param_map['poll_url_source_name'] = [
            'Enter the name or number of the external threat feed sourc', REQUIRED, 1]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def edit_poll_url(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['poll_url_source_name'] = [
            'Enter the name or number of the external threat feed source', REQUIRED]
        param_map['poll_url_source_newname'] = ['Enter a name for the external threat feed source', DEFAULT]
        param_map['poll_url_source_description'] = [
            'Enter a description for the external threat feed source', DEFAULT]
        param_map['poll_url_host_name'] = ['Enter the hostname for the external threat feed source', DEFAULT]
        param_map['poll_url_polling_path'] = ['Enter the polling path for the external threat feed source', DEFAULT]
        param_map['poll_url_collection_name'] = ['Enter the collection name for the external threat feed source', DEFAULT]
        param_map['poll_url_polling_interval'] = [
            'Enter the polling interval', DEFAULT]
        param_map['poll_url_feed_age'] = [
            'Enter the age of the threat feed', DEFAULT]
        param_map['poll_url_poll_segment'] = [
            'Enter the time span for each poll segment',DEFAULT]
        param_map['poll_url_use_https'] = ['Do you want to use HTTPS', DEFAULT]
        param_map['poll_url_polling_port'] = ['Enter the polling port', DEFAULT]
        param_map['poll_url_enable_proxy'] = ['Do you want to use a proxy server', DEFAULT]
        param_map['poll_url_configure_credentials'] = [
            'Do you want to configure user credentials', DEFAULT]
        cfg_credentials = kwargs['poll_url_configure_credentials']
        if  cfg_credentials.lower() == 'y':
            param_map['poll_url_auth_method'] = ['Basic Authentication', DEFAULT, 1]
            param_map['poll_url_auth_username'] = ['Enter the username', DEFAULT]
            param_map['poll_url_auth_password'] = ['assword', DEFAULT]

        param_map.update(kwargs)
        return self._process_input(param_map)

    def suspend_poll_url(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose ')
        param_map['poll_url_source_name'] = [
            'Enter the name or number of the external threat feed source you want to suspend', REQUIRED, 1]
        param_map['confirm_suspend'] = ['Are you sure you want to suspend',
                                       REQUIRED]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def resume_poll_url(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose ')
        param_map['poll_url_source_name'] = [
            'Enter the name or number of the external threat feed source you want to resume', REQUIRED, 1]
        param_map['confirm_resume'] = ['Are you sure you want to resume',
                                       REQUIRED]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def delete_poll_url(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose ')
        param_map['poll_url_source_name'] = [
            'Enter the name or number of the external threat feed source you want to delete', REQUIRED, 1]
        param_map['confirm_delete'] = ['Are you sure you want to delete',
                                       REQUIRED]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)
