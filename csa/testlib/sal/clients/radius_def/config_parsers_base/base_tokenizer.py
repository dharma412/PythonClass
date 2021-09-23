#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/config_parsers_base/base_tokenizer.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os
import re


class TokenNotFoundError(Exception):
    pass


class Token(object):
    def __init__(self):
        self._value = ''

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def value(self):
        return self._value

    @classmethod
    def get_signature(cls):
        raise NotImplementedError('Should return regexp pattern of the token signature')

    def get_value(self):
        return self._value

    def _extract_from_content(self, content, current_pos):
        raise NotImplementedError('Should be implemented in subclasses')


class Indent(Token):
    @classmethod
    def get_signature(cls):
        return r'[^\S\n]'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos
        while end_pos < len(content) and re.search(self.get_signature(),
                                                   content[end_pos]):
            end_pos += 1
        self._value = content[current_pos:end_pos]
        return end_pos


class Comment(Token):
    @classmethod
    def get_signature(cls):
        return r'#'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos + content[current_pos + 1:].find('\n') + 1
        if end_pos < 0:
            end_pos = content[current_pos + 1:].find('\r') + 1
        if end_pos < 0:
            end_pos = len(content)
        self._value = content[current_pos + 1:end_pos]
        return end_pos


class LineBreak(Token):
    @classmethod
    def get_signature(cls):
        return r'[\r\n]'

    def _extract_from_content(self,
                              content,
                              current_pos):
        end_pos = current_pos
        while end_pos < len(content) and re.search(self.get_signature(),
                                                   content[end_pos]):
            end_pos += 1
        self._value = content[current_pos:end_pos]
        return end_pos


class BaseTokenizer(object):
    def __init__(self, path=None, content=None):
        assert ((path is not None) or (content is not None))
        if (path is not None) and os.path.exist(path):
            self._content = self._get_strings_content(path)
        elif content is not None:
            self._content = content
        else:
            raise ValueError('You should pass correct path ' \
                             'to existing file or its content')
        self._splitted_content = self._content.splitlines()
        self._tokenized_view = []
        self._init_helper_vars()
        self._tokenize_content()

    def _init_helper_vars(self):
        pass

    def _get_strings_content(self, path):
        with open(path, 'rU') as f:
            content = f.read()
        return content

    def _get_next_token(self, current_pos):
        raise NotImplementedError('Should be implemented in subclasses')

    def _pos_to_line_col(self, pos):
        current_char_num = 0
        for line_num in xrange(len(self._splitted_content)):
            # plus LF symbol
            line_length = len(self._splitted_content[line_num]) + 1
            if current_char_num <= pos <= current_char_num + line_length:
                return (line_num + 1, pos - current_char_num + 1)
            else:
                current_char_num += line_length
        return (1, 1)

    def _tokenize_content(self):
        current_pos = 0
        while current_pos < len(self._content):
            try:
                tok, next_pos = self._get_next_token(current_pos)
                self._tokenized_view.append((tok,
                                             self._pos_to_line_col(next_pos)))
                current_pos = next_pos
            except TokenNotFoundError:
                row_col = self._pos_to_line_col(current_pos)
                raise TokenNotFoundError('Unexpected symbol is found at ' \
                                         u'line %s column %s:\n%s  \u21D0' % \
                                         (row_col[0], row_col[1], self.get_content_for_error_desciption(row_col)))

    def get_content_for_error_desciption(self, error_pos):
        dest_line, dest_col = error_pos
        return self._splitted_content[dest_line - 1][:dest_col]

    def get_tokenized_view(self):
        return self._tokenized_view


def create_token(token_context, content, current_pos):
    pos = current_pos
    buffer = ''
    while pos < len(content):
        buffer += content[pos]
        for token_cls in token_context:
            if re.match(token_cls.get_signature(), buffer):
                tok = token_cls()
                next_pos = tok._extract_from_content(content, current_pos)
                return (tok, next_pos)
        pos += 1
    raise TokenNotFoundError()


def transform_token(src_token, target_token_class):
    result = target_token_class()
    if re.match(target_token_class.get_signature(), src_token.value[0]):
        result._value = src_token.value
    else:
        raise TokenNotFoundError()
    return result
