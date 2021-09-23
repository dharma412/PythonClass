#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/clients_parser/compiler.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.ordered_dict import OrderedDict

import re

from sal.clients.radius_def.config_parsers_base.base_compiler import BaseCompiler, \
    CompilationError
from sal.clients.radius_def.config_parsers_base.base_tokenizer import Comment, LineBreak, \
    Indent
from tokenizer import ClientsConfTokenizer, \
    RecordBegin, RecordFinish, EqualSign, \
    Attribute, ClientRecordID


class CompiledClient(object):
    def __init__(self, name, attributes={}):
        self.name = name
        self.attributes = attributes

    def as_string(self):
        attributes_str = ''
        for key, value in self.attributes.iteritems():
            attributes_str += '\t\t%s = %s\n' % (key, value)
        return 'client %s {\n%s}\n' % (self.name, attributes_str)


class ClientsConfCompiler(BaseCompiler):
    def _verify_hostname(self, value, pos):
        """value can be DNS or ipv4 or ipv6
        or subnet address
        """
        slash_pos = value.find('/')
        if slash_pos > 0:
            value_to_check = value[:slash_pos]
        else:
            value_to_check = value
        ipv4_regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)' \
                     r'{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
        ipv6_regexp = r'^(((?=.*(::))(?!.*\3.+\3))\3?|[\dA-F]{1,4}:)' \
                      r'([\dA-F]{1,4}(\3|:\b)|\2){5}(([\dA-F]{1,4}(\3|:\b|$)|\2){2}|' \
                      r'(((2[0-4]|1\d|[1-9])?\d|25[0-5])\.?\b){4})\Z'
        hostname_regex = r'^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*' \
                         r'([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$'
        if not any(map(lambda x: re.match(x, value_to_check, re.I or re.S),
                       [ipv4_regex, ipv6_regexp, hostname_regex])):
            raise CompilationError('Invalid client hostname %s is found at '
                                   'position %s:\n%s' % (value, pos,
                                                         self._tokenizer.get_content_for_error_desciption(pos)))

    def _verify_attrname(self, value, pos):
        attrname_regex = r'^[a-zA-Z][0-9a-zA-Z]*'
        if not re.match(attrname_regex, value):
            raise CompilationError('Invalid attribute name %s is found at position ' \
                                   '%s:\n%s' % (value, pos,
                                                self._tokenizer.get_content_for_error_desciption(pos)))

    def _verify_attrvalue(self, value, pos):
        attrvalue_regex = r'[^\s#{}=]+'
        if not re.match(attrvalue_regex, value):
            raise CompilationError('Invalid attribute value %s is found at position ' \
                                   '%s:\n%s' % (value, pos,
                                                self._tokenizer.get_content_for_error_desciption(pos)))

    def _complie_tokenized_client_record(self, tokenized_content):
        client_name = ''
        client_attributes = OrderedDict()
        is_record_begin_found = False
        attr_name = None
        is_equal_sign_found = False
        while tokenized_content:
            token, pos = tokenized_content.pop()
            IGNORED_TOKENS = (Indent, LineBreak, Comment)
            if any(map(lambda x: isinstance(token, x), IGNORED_TOKENS)):
                continue
            elif isinstance(token, Attribute):
                if not client_name:
                    self._verify_hostname(token.value, pos)
                    client_name = token.value
                    continue
                if client_name and is_record_begin_found:
                    if attr_name is None:
                        self._verify_attrname(token.value, pos)
                        attr_name = token.value
                    elif is_equal_sign_found:
                        self._verify_attrvalue(token.value, pos)
                        client_attributes[attr_name] = token.value
                        attr_name = None
                        is_equal_sign_found = False
                else:
                    self._raise_compilation_error(token, pos)
            elif isinstance(token, EqualSign):
                if client_name and is_record_begin_found and (attr_name is not None):
                    is_equal_sign_found = True
                else:
                    self._raise_compilation_error(token, pos)
            elif isinstance(token, RecordBegin):
                if not client_name or is_record_begin_found:
                    self._raise_compilation_error(token, pos)
                else:
                    is_record_begin_found = True
            elif isinstance(token, RecordFinish):
                if not is_record_begin_found:
                    self._raise_compilation_error(token, pos)
                else:
                    break
            else:
                self._raise_compilation_error(token, pos)
        if not client_name:
            raise CompilationError('Failed to parse client entry')
        if not client_attributes:
            raise CompilationError('Client %s should contain at least one attribute' % \
                                   (client_name,))
        return CompiledClient(client_name, client_attributes)

    def _compile(self):
        tokenized_content = self._tokenizer.get_tokenized_view()
        tokenized_content.reverse()
        while tokenized_content:
            token, pos = tokenized_content.pop()
            IGNORED_TOKENS = (Indent, LineBreak, Comment)
            if any(map(lambda x: isinstance(token, x), IGNORED_TOKENS)):
                continue
            elif isinstance(token, ClientRecordID):
                client = self._complie_tokenized_client_record(tokenized_content)
                self._compiled_data.append(client)
            else:
                raise CompilationError('Unexpected token "%s" is found at ' \
                                       'position %s:\n%s' % \
                                       (token.name, pos,
                                        self._tokenizer.get_content_for_error_desciption(pos)))


if __name__ == '__main__':
    sc = ClientsConfCompiler(ClientsConfTokenizer)
    entries_list = sc.get_compiled_file('testdata/clients.conf')
    for entry in entries_list:
        print entry.as_string()
