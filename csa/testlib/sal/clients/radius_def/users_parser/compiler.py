#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/users_parser/compiler.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re

from common.util.ordered_dict import OrderedDict

from sal.clients.radius_def.config_parsers_base.base_compiler import BaseCompiler, \
    CompilationError
from sal.clients.radius_def.config_parsers_base.base_tokenizer import Comment, LineBreak, \
    Indent
from tokenizer import UsersTokenizer, Comma, Attribute, \
    Operator, UserRecordID


class CompiledUser(object):
    def __init__(self, name, verification_attributes={}, response_attributes={}):
        self.name = name
        self.verification_attributes = verification_attributes
        self.response_attributes = response_attributes

    def as_string(self):
        verification_attributes_str = ''
        response_attributes_str = ''

        for key, value in self.verification_attributes.iteritems():
            verification_attributes_str += '%s %s "%s", ' % (key, value[0], value[1])
        if verification_attributes_str:
            verification_attributes_str = verification_attributes_str[:-2]
        else:
            raise ValueError('User "%s" should contain at least one verification ' \
                             'attribute' % (self.name,))

        for key, value in self.response_attributes.iteritems():
            response_attributes_str += '    %s %s "%s",\n' % (key, value[0], value[1])
        if response_attributes_str:
            response_attributes_str = response_attributes_str[:-2]
            return '"%s"   %s\n%s\n' % (self.name, verification_attributes_str,
                                        response_attributes_str)
        else:
            return '"%s"   %s\n' % (self.name, verification_attributes_str)


class UsersCompiler(BaseCompiler):
    def _verify_username(self, value, pos):
        """value can be unix user name
        """
        validation_regex = r'^[a-zA-Z][a-zA-Z0-9\-_\s]*'
        if re.match(value, validation_regex):
            raise CompilationError('Invalid user name %s is found at '
                                   'position %s:\n%s' % (value, pos,
                                                         self._tokenizer.get_content_for_error_desciption(pos)))

    def _verify_attrname(self, value, pos):
        attrname_regex = r'^[a-zA-Z][0-9a-zA-Z\-_]*'
        if not re.match(attrname_regex, value):
            raise CompilationError('Invalid attribute name %s is found at position ' \
                                   '%s:\n%s' % (value, pos,
                                                self._tokenizer.get_content_for_error_desciption(pos)))

    def _verify_attrvalue(self, value, pos):
        attrvalue_regex = r'[^\s]+'
        if not re.match(attrvalue_regex, value):
            raise CompilationError('Invalid attribute value %s is found at position ' \
                                   '%s:\n%s' % (value, pos,
                                                self._tokenizer.get_content_for_error_desciption(pos)))

    def _complie_tokenized_user_record(self, user_id_token, user_id_pos, tokenized_content):
        self._verify_username(user_id_token.value, user_id_pos)
        user_name = user_id_token.value
        verification_attributes = OrderedDict()
        response_attributes = OrderedDict()
        is_inside_verification_attrs_section = True
        is_inside_response_attrs_section = False
        attr_name = None
        last_operator = None

        previous_token = user_id_token
        while tokenized_content:
            token, pos = tokenized_content.pop()
            IGNORED_TOKENS = (Indent, Comment)
            if any(map(lambda x: isinstance(token, x), IGNORED_TOKENS)):
                continue
            elif isinstance(token, UserRecordID) and is_inside_response_attrs_section:
                # response attributes section is empty
                tokenized_content.append((token, pos))
                break
            elif isinstance(token, LineBreak) and not isinstance(previous_token, Comma):
                if is_inside_verification_attrs_section:
                    is_inside_verification_attrs_section = False
                    is_inside_response_attrs_section = True
                elif is_inside_response_attrs_section:
                    break
            elif isinstance(token, LineBreak):
                pass
            elif isinstance(token, Attribute):
                if attr_name is None:
                    self._verify_attrname(token.value, pos)
                    attr_name = token.value
                elif last_operator is not None:
                    self._verify_attrvalue(token.value, pos)
                    if is_inside_verification_attrs_section:
                        verification_attributes[attr_name] = (last_operator.value,
                                                              token.value)
                    else:
                        response_attributes[attr_name] = (last_operator.value,
                                                          token.value)
                    attr_name = None
                    last_operator = None
                else:
                    self._raise_compilation_error(token, pos)
            elif isinstance(token, Operator):
                if attr_name is not None:
                    last_operator = token
                else:
                    self._raise_compilation_error(token, pos)
            elif isinstance(token, Comma):
                if attr_name is not None:
                    self._raise_compilation_error(token, pos)
            else:
                self._raise_compilation_error(token, pos)
            previous_token = token
        if not len(verification_attributes):
            raise CompilationError('User %s should contain at least one verification attribute' % \
                                   (user_name,))
        return CompiledUser(user_name, verification_attributes, response_attributes)

    def _compile(self):
        tokenized_content = self._tokenizer.get_tokenized_view()
        tokenized_content.reverse()
        while tokenized_content:
            token, pos = tokenized_content.pop()
            IGNORED_TOKENS = (Indent, LineBreak, Comment)
            if any(map(lambda x: isinstance(token, x), IGNORED_TOKENS)):
                continue
            elif isinstance(token, UserRecordID):
                user = self._complie_tokenized_user_record(token, pos, tokenized_content)
                self._compiled_data.append(user)
            else:
                raise CompilationError('Unexpected token "%s" is found at ' \
                                       'position %s:\n%s' % \
                                       (token.name, pos,
                                        self._tokenizer.get_content_for_error_desciption(pos)))


if __name__ == '__main__':
    uc = UsersCompiler(UsersTokenizer)
    entries_list = uc.get_compiled_file('testdata/users')
    for entry in entries_list:
        print entry.as_string()
