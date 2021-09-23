#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/bvconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class bvconfig(CliKeywordBase):
    """
    cli -> bvconfig

    Provides keywords for bounce message verification setup
    """

    def get_keyword_names(self):
        return ['bvconfig_key',
                'bvconfig_clear',
                'bvconfig_setup',
                'bvconfig_purge'
                ]

    def bvconfig_key(self, key=None):
        """
        Creates a key to be used for tagging outgoing mails when tagging is
        enabled in the Good Neighbor Table

        bvconfig -> key

        *Parameters*:
        - `key`: key to tag outgoing mails with

        *Returns*:
          Keys used in past along with currently used one

        *Examples*:
        | ${output}= | Bvconfig Key | key=testfoo2 |
        """
        try:
            return self._cli.bvconfig().key(key=key)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def bvconfig_clear(self, disable_bv='yes'):
        """
        Clear all keys including current key.

        bvconfig -> clear

        *Parameters*:
        - `disable_bv`: confirm to disable bounce verification on
          clearing all keys

        *Returns*:
          Output of the clear command

        *Examples*:
        | ${output}= | Bvconfig Clear | disable_bv=yes |
        """
        try:
            return self._cli.bvconfig(). \
                clear(disable_bounce_verification=self._process_yes_no(disable_bv))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def bvconfig_setup(self, behaviour='reject', tag=None, value=None, \
                       smart_exceptions='yes'):
        """
        Configure bounce verification options

        bvconfig -> setup

        *Parameters*:
        - `behaviour`: behavior for bounce messages which are not addressed
          to a valid tagged recipient. Either 'reject' or 'add'
        - `tag`: Specify the header name
        - `value`: Specify the header content
        - `smart_exceptions`: Enable smart exceptions to tagging.
          Either 'yes' or 'no'

        *Examples*:
        | Bvconfig Setup | behaviour=reject | smart_exceptions=yes |
        | Bvconfig Setup | behaviour=add | tag=X-Ironport | value=test |
        | ... | smart_exceptions=yes |
        """
        try:
            self._cli.bvconfig().setup(behaviour=behaviour, tag=tag, value=value,
                                       smart_exceptions=self._process_yes_no(smart_exceptions))
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def bvconfig_purge(self, duration='all'):
        """
        Purge keys no longer needed for verifying incoming mail.

        bvconfig -> purge

        *Parameters*:
        - `duration`: Specify the range of previously-used keys to be purged.
          Either 'all' or 'year' or 'month'

        *Examples*:
        | Bvconfig Purge | duration=month |
        """
        try:
            self._cli.bvconfig().purge(duration=duration)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
