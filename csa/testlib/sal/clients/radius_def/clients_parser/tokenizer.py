#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/clients_parser/tokenizer.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from datetime import datetime
import re

from sal.clients.radius_def.config_parsers_base.base_tokenizer import BaseTokenizer, \
    Token, Indent, Comment, LineBreak, create_token


class RecordBegin(Token):
    @classmethod
    def get_signature(cls):
        return r'{'

    def _extract_from_content(self,
                              content,
                              current_pos):
        self._value = content[current_pos]
        return current_pos + 1


class RecordFinish(Token):
    @classmethod
    def get_signature(cls):
        return r'}'

    def _extract_from_content(self,
                              content,
                              current_pos):
        self._value = content[current_pos]
        return current_pos + 1


class EqualSign(Token):
    @classmethod
    def get_signature(cls):
        return r'='

    def _extract_from_content(self,
                              content,
                              current_pos):
        self._value = content[current_pos]
        return current_pos + 1


class Attribute(Token):
    @classmethod
    def get_signature(cls):
        return r'[^={}\s#]'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos
        while end_pos < len(content) and re.search(self.get_signature(),
                                                   content[end_pos]):
            end_pos += 1
        self._value = content[current_pos:end_pos]
        return end_pos


class ClientRecordID(Token):
    @classmethod
    def get_signature(cls):
        return r'client'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos + len(self.get_signature())
        self._value = content[current_pos:end_pos]
        return end_pos


GLOBAL_TOKENS = (Comment, LineBreak, Indent, ClientRecordID)
CLIENT_RECORD_TOKENS = (Comment, LineBreak, Indent, RecordBegin,
                        RecordFinish, EqualSign, Attribute)


class ClientsConfTokenizer(BaseTokenizer):
    def _init_helper_vars(self):
        self._is_inside_client_record = False

    def _get_next_token(self, current_pos):
        if self._is_inside_client_record:
            token_context = CLIENT_RECORD_TOKENS
        else:
            token_context = GLOBAL_TOKENS
        current_token, next_pos = create_token(token_context, self._content, current_pos)
        if isinstance(current_token, RecordFinish):
            self._is_inside_client_record = False
        if isinstance(current_token, ClientRecordID):
            self._is_inside_client_record = True
        return (current_token, next_pos)


if __name__ == '__main__':
    print datetime.now()
    st = ClientsConfTokenizer('testdata/clients.conf')
    for token, pos in st.get_tokenized_view():
        print token.name, '::', token.value
    print datetime.now()
