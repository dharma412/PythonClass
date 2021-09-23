#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/show_recipients.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class ShowRecipients(CliKeywordBase):

    """Keywords for showrecipients CLI command."""

    def get_keyword_names(self):
        return ['showrecipients',
                ]

    def showrecipients(self, how=DEFAULT, recipient_host=DEFAULT,
            envelop_from=DEFAULT, issensitive=DEFAULT, raw_output=True):
        """ Get netstat information.

        *Parameters*\n
        Selector: Is a string or regular expression.
                  1. If selector is a string, the first input list option
                  that contains selector will be chosen.
                  2. If selector is a regular expression, then the first input
                  list option that matches selector will be chosen.\n
        - `how`:  how you would like to show messages. Selector.
        - `recipient_host`: show only messages sent to this hostname.
        - `envelop_from`: show only messages sent from this address.
        - `issensitive`: If you filter messages by `envelop_from`, should this
          search be case sensitive? YES or NO string.
        - `raw_output`: if this parameter is ${False} then  result will
          be returned as list of string. If ${True}, result will be non-formated
          output of this command. Default is ${True}.

        Return:
            List of string or unformated output of command 'showrecipients'. See
            `raw_output` parameter.

        Exception:
            None.

        *Examples*

        | Showrecipients | all |
        | Showrecipients | how=host | recipient_host=evilhost.com |
        | ... | issensitive=YES |
        | Showrecipients | how=Envelop | envelop_from=iafhost@auto06.auto |
        | ... | raw_output=${False} |
        | Showrecipients | how=All | raw_output=${False} |
        """
        return self._cli.showrecipients(how=how, recipient_host=recipient_host,
                envelop_from=envelop_from, issensitive=issensitive,
                raw_output=raw_output)

