#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/radius_def/config_parsers_base/base_compiler.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from base_tokenizer import TokenNotFoundError


class CompilationError(Exception):
    pass


class BaseCompiler(object):
    def __init__(self, tokenizer_class):
        self._tokenizer_class = tokenizer_class

    def _raise_compilation_error(self, token, pos):
        raise CompilationError('Unexpected token "%s" is found at ' \
                               'position %s:\n%s' % (token.name, pos,
                                                     self._tokenizer.get_content_for_error_desciption(pos)))

    def _get_compiled_data(self, tokenizer):
        self._tokenizer = tokenizer
        self._compiled_data = []
        self._compile()
        return self._compiled_data

    def get_compiled_file(self, path):
        try:
            return self._get_compiled_data(self._tokenizer_class(path=path))
        except TokenNotFoundError as e:
            raise CompilationError(unicode(e))

    def get_compiled_content(self, content):
        try:
            return self._get_compiled_data(self._tokenizer_class(content=content))
        except TokenNotFoundError as e:
            raise CompilationError(unicode(e))

    def _compile(self):
        raise NotImplementedError('Should be implemented in subclasses')
