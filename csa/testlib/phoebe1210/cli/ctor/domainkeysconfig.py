#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/domainkeysconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
SARF CLI command: domainkeysconfig
"""

import clictorbase
from clictorbase import IafCliError, REQUIRED, DEFAULT, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.exceptions import TimeoutError
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO, is_yes
from curses.ascii import ctrl
import re

DEBUG = True


class domainkeysconfig(clictorbase.IafCliConfiguratorBase):
    level = 1

    def __call__(self):
        import handlecluster

        self._writeln(self.__class__.__name__)

        # to handle clustered environment
        handlecluster.handle_cluster_questions(self._sess)

        return self

    def setup(self, enable=DEFAULT):
        self._query_response('SETUP')
        self._query_response(enable)
        self._to_the_top(self.level)

    def profiles(self):
        self._query_response('PROFILES')
        return domainkeysconfigProfiles(self._get_sess())

    def keys(self):
        self._query_response('KEYS')
        return domainkeysconfigKeys(self._get_sess())

    def search(self, profile_or_key=REQUIRED):
        self._query_response('SEARCH')
        self._query_response(profile_or_key)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw


class domainkeysconfigProfiles(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Profiles"""

    class DomainProfileKeyNameError(IafCliError):
        pass

    class DomainNameError(IafCliError):
        pass

    class SelectorError(IafCliError):
        pass

    class KeyGeneratingError(IafCliError):
        pass

    class UserError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class UserDomainMatchError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    class AlgorithmError(IafCliError):
        pass

    class ExportError(IafCliError):
        pass

    class ImportError(IafCliError):
        pass

    level = 2

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('DomainKeys profile and key names must',
             EXACT): self.DomainProfileKeyNameError,
            ('A DomainKeys "domain" is a string', EXACT): self.DomainNameError,
            ('A DomainKeys "selector" is a string', EXACT): self.SelectorError,
            ('A DKIM "selector" record is a string', EXACT): self.SelectorError,
            ('Failed to generate public key', EXACT): self.KeyGeneratingError,
            ('A DomainKeys "user" is a string', EXACT): self.UserError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('User \S+ does not match domain',
             REGEX): self.UserDomainMatchError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
            ('The canonicalization algorithm can be either',
             EXACT): self.AlgorithmError,
            ('Export failed', EXACT): self.ExportError,
            ('Error: the file \S+ does not exist', REGEX): self.ImportError,
            ('Error: Expecting ', EXACT): self.ImportError, })

    def signing(self):
        self._query_response('SIGNING')
        return domainkeysconfigProfilesSigning(self._get_sess())

    def verification(self):
        self._query_response('VERIFICATION')
        return domainkeysconfigProfilesVerification(self._get_sess())


# This needs to be extended for future
class domainkeysconfigProfilesVerification(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Profiles -> Verification"""

    class DomainProfileKeyNameError(IafCliError):
        pass

    class DomainNameError(IafCliError):
        pass

    class SelectorError(IafCliError):
        pass

    class KeyGeneratingError(IafCliError):
        pass

    class UserError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class UserDomainMatchError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    class AlgorithmError(IafCliError):
        pass

    class ExportError(IafCliError):
        pass

    class ImportError(IafCliError):
        pass

    level = 3

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('DomainKeys profile and key names must',
             EXACT): self.DomainProfileKeyNameError,
            ('A DomainKeys "domain" is a string', EXACT): self.DomainNameError,
            ('A DomainKeys "selector" is a string', EXACT): self.SelectorError,
            ('A DKIM "selector" record is a string', EXACT): self.SelectorError,
            ('Failed to generate public key', EXACT): self.KeyGeneratingError,
            ('A DomainKeys "user" is a string', EXACT): self.UserError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('User \S+ does not match domain',
             REGEX): self.UserDomainMatchError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
            ('The canonicalization algorithm can be either',
             EXACT): self.AlgorithmError,
            ('Export failed', EXACT): self.ExportError,
            ('Error: the file \S+ does not exist', REGEX): self.ImportError,
            ('Error: Expecting ', EXACT): self.ImportError,
        })

    def new(self,
            name=REQUIRED,
            small_key=DEFAULT,
            largest_key=DEFAULT,
            max_signatures=DEFAULT,
            time_out=DEFAULT,
            tolerate=DEFAULT,
            body_length=DEFAULT,
            SMTP_action_temp=DEFAULT,
            SMTP_response_code_temp=DEFAULT,
            SMTP_response_text_temp=DEFAULT,
            SMTP_action_perm=DEFAULT,
            SMTP_response_code_perm=DEFAULT,
            SMTP_response_text_perm=DEFAULT):
        self._query_response('NEW')
        self._query_response(name)
        self._new_edit(small_key,
                       largest_key, max_signatures,
                       time_out,
                       tolerate,
                       body_length,
                       SMTP_action_temp,
                       SMTP_response_code_temp,
                       SMTP_response_text_temp,
                       SMTP_action_perm,
                       SMTP_response_code_perm,
                       SMTP_response_text_perm)

    def edit(self,
             name=REQUIRED,
             new_name=DEFAULT,
             small_key=DEFAULT,
             largest_key=DEFAULT,
             max_signatures=DEFAULT,
             time_out=DEFAULT,
             tolerate=DEFAULT,
             body_length=DEFAULT,
             SMTP_action_temp=DEFAULT,
             SMTP_response_code_temp=DEFAULT,
             SMTP_response_text_temp=DEFAULT,
             SMTP_action_perm=DEFAULT,
             SMTP_response_code_perm=DEFAULT,
             SMTP_response_text_perm=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        self._query_response(new_name)
        self._new_edit(small_key,
                       largest_key,
                       max_signatures,
                       time_out,
                       tolerate,
                       body_length,
                       SMTP_action_temp,
                       SMTP_response_code_temp,
                       SMTP_response_text_temp,
                       SMTP_action_perm,
                       SMTP_response_code_perm,
                       SMTP_response_text_perm)

    def _new_edit(self,
                  small_key=DEFAULT,
                  largest_key=DEFAULT,
                  max_signatures=DEFAULT,
                  time_out=DEFAULT,
                  tolerate=DEFAULT,
                  body_length=DEFAULT,
                  SMTP_action_temp=DEFAULT,
                  SMTP_response_code_temp=DEFAULT,
                  SMTP_response_text_temp=DEFAULT,
                  SMTP_action_perm=DEFAULT,
                  SMTP_response_code_perm=DEFAULT,
                  SMTP_response_text_perm=DEFAULT):
        self._query_select_list_item(small_key)
        self._query_select_list_item(largest_key)
        self._query_response(max_signatures)
        self._query_response(time_out)
        self._query_response(tolerate)
        self._query_response(body_length)
        self._query_select_list_item(SMTP_action_temp)
        if SMTP_action_temp:
            if (SMTP_action_temp == '2') | (SMTP_action_temp == 'Reject'):
                self._query_response(SMTP_response_code_temp)
                self._query_response(SMTP_response_text_temp)
        self._query_select_list_item(SMTP_action_perm)
        if SMTP_action_perm:
            if (SMTP_action_perm == '2') | (SMTP_action_perm == 'Reject'):
                self._query_response(SMTP_response_code_perm)
                self._query_response(SMTP_response_text_temp)
        self._to_the_top(self.level)

    def print_profiles(self, name=DEFAULT):
        self.clearbuf()
        self._query_response('PRINT')
        self._query_select_list_item(name)
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def list_profiles(self):
        self.clearbuf()
        self._query_response('LIST')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def clear(self, confirm=DEFAULT):
        self._query_response('CLEAR')
        self._query_response(confirm)
        self._to_the_top(self.level)

    def import_profiles(self, filename=REQUIRED):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def export_profiles(self, filename=REQUIRED):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def delete(self, name=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(name)
        self._to_the_top(self.level)


class domainkeysconfigProfilesSigning(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Profiles -> Signing"""

    class DomainProfileKeyNameError(IafCliError):
        pass

    class DomainNameError(IafCliError):
        pass

    class SelectorError(IafCliError):
        pass

    class KeyGeneratingError(IafCliError):
        pass

    class UserError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class UserDomainMatchError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    class AlgorithmError(IafCliError):
        pass

    class ExportError(IafCliError):
        pass

    class ImportError(IafCliError):
        pass

    level = 3

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('DomainKeys profile and key names must',
             EXACT): self.DomainProfileKeyNameError,
            ('A DomainKeys "domain" is a string', EXACT): self.DomainNameError,
            ('A DomainKeys "selector" is a string', EXACT): self.SelectorError,
            ('A DKIM "selector" record is a string', EXACT): self.SelectorError,
            ('Failed to generate public key', EXACT): self.KeyGeneratingError,
            ('A DomainKeys "user" is a string', EXACT): self.UserError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('User \S+ does not match domain',
             REGEX): self.UserDomainMatchError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
            ('The canonicalization algorithm can be either',
             EXACT): self.AlgorithmError,
            ('Export failed', EXACT): self.ExportError,
            ('Error: the file \S+ does not exist', REGEX): self.ImportError,
            ('Error: Expecting ', EXACT): self.ImportError,
        })

    def new(self,
            name=REQUIRED,
            profile_type='2',
            domain_name=REQUIRED,
            canonicalization_algorithm=DEFAULT,
            key_method='1',
            key_name=REQUIRED,
            rsa_key=REQUIRED,
            key_size='3',
            dkim_hdrs_algorithm=DEFAULT,
            dkim_body_algorithm=DEFAULT,
            dkim_sign_hdrs=DEFAULT,
            dkim_custom_hdrs=DEFAULT,
            dkim_body_length=DEFAULT,
            dkim_custom_body_length=REQUIRED,
            dkim_tag_tune=DEFAULT,
            i_tag=DEFAULT,
            dkim_identity_user=DEFAULT,
            q_tag=DEFAULT,
            t_tag=DEFAULT,
            x_tag=DEFAULT,
            z_tag=DEFAULT,
            dkim_expire_time=DEFAULT,
            user=DEFAULT,
            existing_key=DEFAULT,
            selector=REQUIRED):
        import time
        another_user = NO
        self._query_response('NEW')
        self._query_response(name)
        _profile_type = self._query_select_list_item(profile_type)
        self._query_response(domain_name)
        self._query_response(selector)
        if (_profile_type == 1) | (profile_type == 'dk'):
            self._query_select_list_item(canonicalization_algorithm)
        _key_method = self._query_select_list_item(key_method)
        if key_method:
            if (_key_method == 1) | (key_method == 'Create new key'):
                self._query_response(key_name)
                self._query_response(key_size)
            elif (_key_method == 2) | (key_method == 'Paste in key'):
                self._query_response(key_name)
                # break up writes to write smaller chunks of text
                # because writing a large block of
                # text causes TimeoutError exceptions to be raised.
                for line in rsa_key.split('\n'):
                    self._sess.write(line + '\n')
                    time.sleep(0.5)
                self._sess.write(ctrl('d'))
                time.sleep(0.5)
                self._sess.write(user)
                time.sleep(0.5)
                self._writeln()
            elif (_key_method == 4) | (key_method == 'Select existing key'):
                self._query_select_list_item(existing_key)
            if (_profile_type == 2) | (profile_type == 'dkim'):
                self._query_select_list_item(dkim_hdrs_algorithm)
                self._query_select_list_item(dkim_body_algorithm)
                _dkim_sign_hdrs = self._query_select_list_item(dkim_sign_hdrs)
                if (_dkim_sign_hdrs == 3):
                    self._query_response(dkim_custom_hdrs)
                _dkim_body_length = self._query_select_list_item(dkim_body_length)
                if (_dkim_body_length == 3):
                    self._query_response(dkim_custom_body_length)
                self._query_response(dkim_tag_tune)
                if (dkim_tag_tune):
                    self._query_response(i_tag)
                    self._query_response(dkim_identity_user)
                    self._query_response(q_tag)
                    self._query_response(t_tag)
                    self._query_response(x_tag)
                    self._query_response(dkim_expire_time)
                    self._query_response(z_tag)

        else:
            self._query_response(key_name)
            self._query_select_list_item(key_size)
        if (_key_method != 2) & (key_method != 'Paste in key'):
            self._query_response(user)
        if user:
            self._query_response(another_user)
        self._to_the_top(self.level)

    def edit(self, name=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        return domainkeysconfigProfilesEdit(self._get_sess())

    def print_profiles(self):
        self.clearbuf()
        self._query_response('PRINT')
        self._expect('\n')
        self._expect(['-Press Any Key For More-', 'Choose the operation'],
                     timeout=10)
        raw = self.getbuf()
        while self._expectindex == 0:
            self._writeln('')
            self._expect(['-Press Any Key For More-', 'Choose the operation'],
                         timeout=10)
            raw = self.getbuf()
        self._to_the_top(self.level)
        return raw

    def list_profiles(self):
        self.clearbuf()
        self._query_response('LIST')
        self._expect('\n')
        self._expect(['-Press Any Key For More-', 'Choose the operation'],
                     timeout=10)
        raw = self.getbuf()
        while self._expectindex == 0:
            self._writeln('')
            self._expect(['-Press Any Key For More-', 'Choose the operation'],
                         timeout=10)
            raw = self.getbuf()
        self._to_the_top(self.level)
        return raw

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def import_profiles(self, filename=REQUIRED):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def export_profiles(self, filename=REQUIRED):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def delete(self, name=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(name)
        self._to_the_top(self.level)

    def test(self, name=DEFAULT):
        self._query_response('TEST')
        self._query_select_list_item(name)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def dnstxt(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['name'] = \
            ['the name or number of a domain profile', DEFAULT, True]
        param_map['g_tag'] = \
            ['information about this profile. Do you wish to constrain the local ' \
             'part of the sending', DEFAULT]
        param_map['local_part'] = \
            ['Enter the local part of a sending address', DEFAULT]
        param_map['n_tag'] = \
            ['include notes that may be of interest to a human', DEFAULT]
        param_map['note'] = \
            ['Enter your note:', DEFAULT]
        param_map['t_tag'] = \
            ['want to indicate the "testing mode"?', DEFAULT]
        param_map['disable_signing_subdomains'] = \
            ['wish to disable signing by subdomains of this', DEFAULT]
        param_map['i_tag'] = \
            ['Do you wish to constrain the local part of the signing identities',
             DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DNSTXT')
        self._process_input(param_map)
        raw = self.getbuf()
        match_obj = re.search(r'The (DKIM|DomainKey) DNS TXT record is:(.*)There',
                              raw, re.MULTILINE | re.DOTALL)
        return match_obj.group(2).strip()


class domainkeysconfigKeys(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Keys"""

    class DomainProfileKeyNameError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class PublicKeyError(IafCliError):
        pass

    class ImportError(IafCliError):
        pass

    class ExportError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    level = 2

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('DomainKeys profile and key names must',
             EXACT): self.DomainProfileKeyNameError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('Failed to generate public key', EXACT): self.PublicKeyError,
            ('Error: the file \S+ does not exist', REGEX): self.ImportError,
            ('Error: Expecting ', EXACT): self.ImportError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('Export failed', EXACT): self.ExportError,
        })

    def new(self,
            name=REQUIRED,
            key_method=DEFAULT,
            rsa_key=REQUIRED,
            size=DEFAULT):
        import time
        self._query_response('NEW')
        self._query_response(name)
        idx = self._query_select_list_item(key_method)
        if idx:
            if idx == 1:
                self._query_select_list_item(size, exact_match=True)
            elif idx == 2:
                # break up writes to write smaller chunks of text
                # because writing a large block of
                # text causes TimeoutError exceptions to be raised.
                for line in rsa_key.split('\n'):
                    self._sess.write(line + '\n')
                    time.sleep(0.5)
                self._sess.write(ctrl('d'))
                time.sleep(0.5)
        else:
            self._query_select_list_item(size)
        self._to_the_top(self.level)

    def edit(self, name=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(name)
        return domainkeysconfigKeysEdit(self._get_sess())

    def print_keys(self, as_dictionary=NO):
        self.clearbuf()
        self._query_response('PRINT')
        self._expect('\n')
        self._expect(['-Press Any Key For More-', 'Choose the operation'],
                     timeout=3)
        raw = self.getbuf()
        while self._expectindex == 0:
            self._writeln('')
            self._expect(['-Press Any Key For More-', 'Choose the operation'],
                         timeout=3)
            raw = self.getbuf()
        self._to_the_top(self.level)
        return raw

    def list_keys(self):
        self.clearbuf()
        self._query_response('LIST')
        self._to_the_top(self.level)
        raw = self.getbuf()
        return raw

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def import_keys(self, filename=REQUIRED):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def export_keys(self, filename=REQUIRED):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.level)

    def delete(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['name'] = \
            ['name or number of a signing', DEFAULT, True]
        param_map['confirm'] = ['Delete this signing key?', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        return self._process_input(param_map)

    def publickey(self, name=DEFAULT):
        self._query_response('PUBLICKEY')
        self._query_select_list_item(name)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        try:
            # rawstr = r"""(?P<public_key>-----BEGIN PUBLIC KEY-----.*-----END PUBLIC KEY-----)"""
            rawstr = r"""(?P<public_key>-----BEGIN PUBLIC KEY.*END PUBLIC KEY-----)"""
            public_key = re.search(rawstr, raw, re.MULTILINE | re.DOTALL).group('public_key')
            return public_key
        except Exception as err:
            self._warn("Failed to get formatted publickey: %s" % err)
        return raw


class domainkeysconfigProfilesEdit(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Profiles ->Edit"""

    class DomainNameError(IafCliError):
        pass

    class SelectorError(IafCliError):
        pass

    class KeyGeneratingError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class UserDomainMatchError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    class DomainProfileExistsError(IafCliError):
        pass

    class UserAlreadyAddedError(IafCliError):
        pass

    class UserPartDomainError(IafCliError):
        pass

    level = 4

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('That domain profile already exists',
             EXACT): self.DomainProfileExistsError,
            ('A DomainKeys "domain" is a string', EXACT): self.DomainNameError,
            ('User \S+ does not match domain',
             REGEX): self.UserDomainMatchError,
            ('A DomainKeys "selector" is a string', EXACT): self.SelectorError,
            ('Failed to generate public key', EXACT): self.KeyGeneratingError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
            ('Error: \S+ has already been added to domain',
             REGEX): self.UserAlreadyAddedError,
            ('Error: \S+ is already part of domain profile',
             REGEX): self.UserPartDomainError
        })

    def new(self, user=REQUIRED):
        another_user = NO
        self._query_response('NEW')
        self._query_response(user)
        self._query_response(another_user)
        self._to_the_top(self.level)

    def print_list(self):
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def delete(self, user=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(user)
        self._to_the_top(self.level)

    def key(self,
            key_method=DEFAULT,
            key_name=REQUIRED,
            key_size=DEFAULT,
            existing_key=DEFAULT,
            rsa_key=REQUIRED):
        self._query_response('KEY')
        _key_method = self._query_select_list_item(key_method)
        if key_method:
            if _key_method == 1 | (key_method == 'Create new key'):
                self._query_response(key_name)
                self._query_select_list_item(key_size)
            if _key_method == 2 | (key_method == 'Paste in key'):
                self._query_response(key_name)
                self._writeln(rsa_key + '\n' + ctrl('d'))
            if _key_method == 4 | (key_method == 'Select existing key'):
                self._query_select_list_item(existing_key)
        else:
            self._query_response(key_name)
            self._query_select_list_item(key_size)
        self._to_the_top(self.level)

    def canonicalization(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['canonicalization_algorithm'] = \
            ['a new canonicalization algorithm', DEFAULT, True]
        param_map['dkim_hdrs_algorithm'] = \
            ['canonicalization algorithm for headers', DEFAULT, True]
        param_map['dkim_body_algorithm'] = \
            ['canonicalization algorithm for body', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        self._query_response('CANONICALIZATION')
        self._process_input(param_map)

    def selector(self, selector=DEFAULT):
        self._query_response('SELECTOR')
        self._query_response(selector)
        self._to_the_top(self.level)

    def domain(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['domain'] = \
            ['new domain for this domain profile', DEFAULT]
        param_map['dkim_hdrs_algorithm'] = \
            ['the identity of the user or agent', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DOMAIN')
        self._process_input(param_map)

    def rename(self, new_name=DEFAULT):
        self._query_response('RENAME')
        self._query_response(new_name)
        self._to_the_top(self.level)

    def bodylength(self,
                   body_length_opt=DEFAULT,
                   custom_body_length=REQUIRED):
        self._query_response('BODYLENGTH')
        _body_length_opt = self._query_select_list_item(body_length_opt)
        if _body_length_opt == 3:
            self._query_response(custom_body_length)
        self._to_the_top(self.level)

    def headerselect(self,
                     how_to_sign=DEFAULT,
                     change_headers=DEFAULT,
                     custom_headers=DEFAULT):
        self._query_response('HEADERSELECT')
        _how_to_sign = self._query_select_list_item(how_to_sign)
        if _how_to_sign == 3:
            self._query_response(change_headers)
            if is_yes(change_headers):
                self._query_response(custom_headers)
        self._to_the_top(self.level)

    def customheaders(self, custom_headers=DEFAULT):
        # this option will only display if profile was configured with
        # custom header previously.
        self._query_response('CUSTOMHEADERS')
        self._query_response(custom_headers)
        self._to_the_top(self.level)

    def expirationtime(self, time=DEFAULT):
        self._query_response('EXPIRATIONTIME')
        self._query_response(time)
        self._to_the_top(self.level)


class domainkeysconfigKeysEdit(clictorbase.IafCliConfiguratorBase):
    """domainkeysconfig -> Keys ->Edit"""

    class DomainProfileKeyNameError(IafCliError):
        pass

    class KeyGeneratingError(IafCliError):
        pass

    class InvalidDataKeyError(IafCliError):
        pass

    class KeyLengthError(IafCliError):
        pass

    level = 3

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('DomainKeys profile and key names must',
             EXACT): self.DomainProfileKeyNameError,
            ('Failed to generate public key', EXACT): self.KeyGeneratingError,
            ('Invalid key data', EXACT): self.InvalidDataKeyError,
            ('Keys must be 512, 768', EXACT): self.KeyLengthError,
        })

    def rename(self, new_name=DEFAULT):
        self._query_response('RENAME')
        self._query_response(new_name)
        self._to_the_top(self.level)

    def key(self,
            key_method=DEFAULT,
            size=DEFAULT,
            rsa_key=REQUIRED):
        self._query_response('KEY')
        idx = self._query_select_list_item(key_method)
        if idx:
            if idx == 1:
                self._query_response(size)
            if idx == 2:
                self._writeln(rsa_key + '\n' + ctrl('d'))
        else:
            self._query_response(size)
        self._to_the_top(self.level)
