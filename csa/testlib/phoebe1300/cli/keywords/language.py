#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/language.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $


from common.cli.clicommon import CliKeywordBase


class language(CliKeywordBase):
    """Specify the language for the CLI."""

    def get_keyword_names(self):
        return ['language_get',
                'language_set']

    def language_set(self, lang):
        """Specify the language for the CLI.

        *Parameters:*
        - `lang`: the new language value for CLI. One of returned
        by Language Get command

        *Return:*
        Raw output

        *Examples:*
        | Language Set | some language |
        """
        return self._cli.language(lang)

    def language_get(self):
        """Print all available languages.

        *Return:*
        List of available CLI languages

        *Examples:*
        | ${lang_list} | Language |
        | Log | ${lang_list} |
        """
        return self._cli.language()
