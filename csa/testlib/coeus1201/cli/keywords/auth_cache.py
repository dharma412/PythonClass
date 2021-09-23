#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/auth_cache.py#1 $
# $Author: uvelayut $
# $DateTime: 2019/08/14 09:58:47 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class AuthCache(CliKeywordBase):
    """authcache
        - This cli is used to manipulate authentication cache entries.
          It is ineffective under Forward mode NTLM with no surrogates
    """
    def get_keyword_names(self):
        return [
            'auth_cache_flushall',
            'auth_cache_flushuser',
            'auth_cache_list',
            'auth_cache_search',
        ]

    def auth_cache_flushall(self):
        """authcache->flushall

        Flush all entries in proxy authentication cache

        Examples:

        | Auth Cache Flushall  |

        """
        output = self._cli.authcache().flushall()
        self._info(output)
        return output

    def auth_cache_flushuser(self, realm=DEFAULT, user=DEFAULT):
        """authcache->flushuser

        Flush specific user entry from auth cache

        Examples:

        | Auth Cache Flushuser  |
        |...|  realm=ntlm1     |
        |...|  user=testuser    |

        """
        if not realm:
            raise ValueError('Parameter- realm has to be specified')
        if not user:
            raise ValueError('Parameter- user has to be specified')

        output = self._cli.authcache().flushuser(realm=realm, user=user)
        self._info(output)
        return output

    def auth_cache_list(self):
        """authcache->list

        Returns the List all entries in proxy authentication cache

        Examples:

        | Auth Cache List  |

        """
        output = self._cli.authcache().listcache()
        self._info(output)
        return output

    def auth_cache_search(self, searchstr=DEFAULT):
        """authcache->search

        Search all entries in proxy authentication cache
        and returns result string

        Examples:

        | Auth Cache Search           |
        |...|  searchstr='Logged in'  |

        """
        if not searchstr:
            raise ValueError('Parameter- searchstr has to be specified')

        output = self._cli.authcache().search(searchstr=searchstr)
        self._info(output)
        return output