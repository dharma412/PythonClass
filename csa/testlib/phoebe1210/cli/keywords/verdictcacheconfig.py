#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/verdictcacheconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $
from common.cli.clicommon import CliKeywordBase, DEFAULT


class verdictcacheconfig(CliKeywordBase):
    """Keywords for Verdictcacheconfig CLi Command.This is a hidden command."""

    def get_keyword_names(self):
        return ['verdictcacheconfig_cloudmark_setup',
                'verdictcacheconfig_cloudmark_status',
                'verdictcacheconfig_case_setup',
                'verdictcacheconfig_case_status',
                'verdictcacheconfig_imageanalysis_setup',
                'verdictcacheconfig_imageanalysis_status',
                ]

    def verdictcacheconfig_cloudmark_setup(self,
                                           use_cache=DEFAULT):
        """
        This command is used to edit Cloudmark SP verdict cache settings

        *Parameters*
        - `use_cache` : This option is used to specify if we like to use
           Cloudmark SP verdict caching

        *Examples*
        | Verdictcacheconfig Cloudmark Setup | use_cache=yes |

        """
        kwargs = {
            'operation': 'setup',
            'use_cache': self._process_yes_no(use_cache),
        }
        self._cli.verdictcacheconfig().cloudmark(**kwargs)

    def verdictcacheconfig_cloudmark_status(self):
        """
        This command is used to Show status of Cloudmark SP verdict cache.

        *Return*
        - Entry lifetime: The number of seconds the entry has been made.
        - number of entries: Number of cache entries.
        - limit: The maximum limit.
        - hit rate: the hit rate for the entries.
        - time saved: The time saved in seconds.
        - total time: The total time in seconds.

        *Examples*
        | ${log}=  |  Verdictcacheconfig Cloudmark Status |
        | Log   |     ${log} |

        """
        kwargs = {
            'operation': 'status'
        }
        return str(self._cli.verdictcacheconfig().cloudmark(**kwargs))

    def verdictcacheconfig_case_setup(self,
                                      use_cache=DEFAULT):
        """

        This command is used to edit CASE  SP verdict cache settings

        *Parameters*
        - `use_cache` : This option is used to specify if we like to use
           CASE SP verdict caching

        *Examples*
        | Verdictcacheconfig Case Setup | use_cache=yes |

        """
        kwargs = {
            'operation': 'setup',
            'use_cache': self._process_yes_no(use_cache),
        }
        self._cli.verdictcacheconfig().case(**kwargs)

    def verdictcacheconfig_case_status(self):
        """
        This command is used to Show status of CASE verdict cache.
        *Return*
        - Entry lifetime: The number of seconds the entry has been made.
        - number of entries: Number of cache entries.
        - limit: The maximum limit.
        - hit rate: the hit rate for the entries.
        - time saved: The time saved in seconds.
        - total time: The total time in seconds.

        *Examples*
        | ${log}=  |  Verdictcacheconfig Case Status |
        | Log   |     ${log} |

        """
        kwargs = {
            'operation': 'status'
        }
        return str(self._cli.verdictcacheconfig().case(**kwargs))

    def verdictcacheconfig_imageanalysis_setup(self,
                                               use_cache=DEFAULT):
        """
        This command is used to edit imageanalysis SP verdict cache settings

        *Parameters*
        - `use_cache` : This option is used to specify if we like to use
           imageanalysis SP verdict caching

        *Example*
        | Verdictcacheconfig Imageanalysis Setup | use_cache=yes |
        """
        kwargs = {
            'operation': 'setup',
            'use_cache': self._process_yes_no(use_cache),
        }
        self._cli.verdictcacheconfig().imageanalysis(**kwargs)

    def verdictcacheconfig_imageanalysis_status(self):
        """
        This command is used to Show status of imageanalysis verdict cache.

        *Return*
        - Entry lifetime: The number of seconds the entry has been made.
        - number of entries: Number of cache entries.
        - limit: The maximum limit.
        - hit rate: the hit rate for the entries.
        - time saved: The time saved in seconds.
        - total time: The total time in seconds.

        *Examples*
        | ${log}=  |  Verdictcacheconfig imageanalysis status |

        """
        kwargs = {
            'operation': 'status'
        }
        return str(self._cli.verdictcacheconfig().imageanalysis(**kwargs))
