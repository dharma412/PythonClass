#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/users_parser/tokenizer.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from datetime import datetime
import re

from sal.clients.radius_def.config_parsers_base.base_tokenizer import BaseTokenizer, \
    Token, Indent, Comment, LineBreak, create_token, transform_token


class Operator(Token):
    # http://freeradius.org/radiusd/man/users.html
    AVAILABLE_OPERATORS = (r':=', r'==', r'\+=',
                           r'!=', r'>=', r'<=',
                           r'=~', r'!~', r'=\*',
                           r'!\*', r'=', r'<',
                           r'>')
    MAX_OPERATOR_LEN = 2

    @classmethod
    def get_signature(cls):
        return '|'.join(cls.AVAILABLE_OPERATORS)

    def _extract_from_content(self,
                              content,
                              current_pos):
        endpos = current_pos + 1
        str_operators = map(lambda x: x.replace('\\', ''), self.AVAILABLE_OPERATORS)
        while endpos < len(content) and \
                filter(lambda x: x.find(content[current_pos:endpos]) == 0, str_operators) and \
                len(content[current_pos:endpos]) <= self.MAX_OPERATOR_LEN:
            endpos += 1
        endpos -= 1
        self._value = content[current_pos:endpos]
        return endpos


class Comma(Token):
    @classmethod
    def get_signature(cls):
        return r','

    def _extract_from_content(self,
                              content,
                              current_pos):
        self._value = content[current_pos]
        return current_pos + 1


class Attribute(Token):
    @classmethod
    def get_signature(cls):
        return r'[^\s#,:=\+!><]'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos + 1
        if content[current_pos] == '"':
            while end_pos < len(content) and (content[end_pos] != '"' and \
                                              content[end_pos - 1] != '\\'):
                end_pos += 1
            if end_pos < len(content):
                end_pos += 1
        else:
            while end_pos < len(content) and re.search(self.get_signature(),
                                                       content[end_pos]):
                end_pos += 1
        self._value = content[current_pos:end_pos]
        if len(self._value) >= 2 and self._value[0] == '"':
            # strip quotes
            self._value = self._value[1:-1]
        return end_pos


class UserRecordID(Token):
    @classmethod
    def get_signature(cls):
        return r'[a-zA-Z0-9"]'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos
        while end_pos < len(content) and re.search(self.get_signature(),
                                                   content[end_pos]):
            end_pos += 1
        self._value = content[current_pos:end_pos]
        return end_pos


GLOBAL_TOKENS = (Comment, LineBreak, Indent, Operator, Comma, Attribute)


class UsersTokenizer(BaseTokenizer):
    def _get_next_token(self, current_pos):
        if self._tokenized_view:
            previous_token = self._tokenized_view[-1][0]
        else:
            previous_token = None
        current_token, next_pos = create_token(GLOBAL_TOKENS, self._content, current_pos)
        if isinstance(current_token, Attribute) and \
                (isinstance(previous_token, LineBreak) or (previous_token is None)):
            current_token = transform_token(current_token, UserRecordID)
        return (current_token, next_pos)


if __name__ == '__main__':
    print datetime.now()
    st = UsersTokenizer('testdata/users')
    tv = st.get_tokenized_view()
    # print tv
    for token, pos in tv:
        print token, ' :: ', pos
    print datetime.now()
