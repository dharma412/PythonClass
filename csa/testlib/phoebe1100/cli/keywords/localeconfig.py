#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/localeconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class localeconfig(CliKeywordBase):
    """
    cli -> localeconfig

    Configure global locale options for mail content scanning.
    """

    def get_keyword_names(self):
        return ['locale_config']

    def locale_config(self, *args):
        """Configure locale options for mail content scanning.

        cli -> localeconfig

        *Parameters:*
        - `force_headers_to_body_charset`: controls whether headers that have
        been modified should be forced to
        the encoding of the main message body. Some MUAs do not honor the RFC
        2047 encoding of a header if the charset is different from the charset
        of the main message body. A risk here is that the body charset might
        not be able to encode all of the characters in the header and thus some
        of them might need to be replaced with placeholders instead of being
        properly encoded in some charset that can contain all of the characters,
        such as UTF-8. Defaults to 1 (true) to maintain maximal compatibility
        with MUAs at the risk of losing data in headers. Either yes or no
        - `use_body_charset_for_untagged_header`: controls whether headers
        that have no encoding but contain 8-bit
        characters and are being modified should be assumed to be in the
        charset of most of the message body. It is not uncommon for MUAs in
        some countries to be non-compliant when encoding message headers and
        not properly encode them in RFC 2047 coding.  Defaults to 1 (true)
        to maintain maximal compatibility with MUAs at the risk of losing
        data in headers. Either yes or no
        - `use_footer_encoding_for_ascii_message_body`: controls whether the
        system will try to use the encoding of the
        footer/header as the encoding of the message body when they do not match,
        and the body is encoded US-ASCII. Defaults to 0 (false) to instead
        include the footer/header as an attachment when its encoding does not
        match the body. Either yes or no

        *Examples:*
        | Locale Config | force_headers_to_body_charset=No |
        | ... | use_body_charset_for_untagged_header=Yes |
        | ... | use_footer_encoding_for_ascii_message_body=Yes |
        | ... | ignore_message_body_decoding_error=No |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.localeconfig().setup(**kwargs)
