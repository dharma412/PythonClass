#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/smimeconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
import shlex
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX

from sal.containers.yesnodefault import YES, NO


class smimeconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 3

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('smimeconfig')
        return self

    def gatewayVerificationNewImport(self, profile_name, import_filename):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('1')
        self._query_response(import_filename)
        self._to_the_top(self.newlines)

    def gatewayVerificationNewPaste(self, profile_name, paste_certificate):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('2')
        self._writeln(paste_certificate)
        self._writeln('.')
        self._to_the_top(self.newlines)

    def gatewayVerificationEditImport(self, profile_number, import_filename):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('yes')
        self._query_response('1')
        self._query_response(import_filename)
        self._to_the_top(self.newlines)

    def gatewayVerificationEditPaste(self, profile_number, paste_certificate):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('yes')
        self._query_response('2')
        self._writeln(paste_certificate)
        self._writeln('.')
        self._to_the_top(self.newlines)

    def gatewayVerificationEdit(self, profile_number):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('no')
        self._to_the_top(self.newlines)

    def gatewayVerificationDelete(self, profile_number):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('DELETE')
        self._query_response(profile_number)
        self._query_response('yes')
        self._to_the_top(self.newlines)

    def gatewayVerificationExport(self, export_filename):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('EXPORT')
        self._query_response(export_filename)
        self._to_the_top(self.newlines)

    def gatewayVerificationImport(self, import_filename):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('IMPORT')
        self._query_response(import_filename)
        self._to_the_top(self.newlines)

    def gatewayVerificationPrint(self):
        self._query_response('GATEWAY')
        self._query_response('VERIFICATION')
        self._query_response('PRINT')
        self._to_the_top(self.newlines)

    def gatewaySendingNewEncrypt(self, profile_name, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('1')
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingNewSign(self, profile_name, smime_certificate, smime_signmode):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('2')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._to_the_top(self.newlines)

    def gatewaySendingNewTriple(self, profile_name, smime_certificate, smime_signmode, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('4')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingNewSignandEncrypt(self, profile_name, smime_certificate, smime_signmode, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('NEW')
        self._query_response(profile_name)
        self._query_response('3')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingEditEncrypt(self, profile_number, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('1')
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingEditSign(self, profile_number, smime_certificate, smime_signmode):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('2')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._to_the_top(self.newlines)

    def gatewaySendingEditTriple(self, profile_number, smime_certificate, smime_signmode, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('4')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingEditSignandEncrypt(self, profile_number, smime_certificate, smime_signmode, smime_action):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('EDIT')
        self._query_response(profile_number)
        self._query_response('3')
        self._query_response(smime_certificate)
        self._query_response(smime_signmode)
        self._query_response(smime_action)
        self._to_the_top(self.newlines)

    def gatewaySendingDelete(self, profile_number):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('DELETE')
        self._query_response(profile_number)
        self._to_the_top(self.newlines)

    def gatewaySendingExport(self, export_filename):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('EXPORT')
        self._query_response(export_filename)
        self._to_the_top(self.newlines)

    def gatewaySendingImport(self, import_filename):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('IMPORT')
        self._query_response(import_filename)
        self._to_the_top(self.newlines)

    def gatewaySendingPrint(self):
        self._query_response('GATEWAY')
        self._query_response('SENDING')
        self._query_response('PRINT')
        self._to_the_top(self.newlines)
