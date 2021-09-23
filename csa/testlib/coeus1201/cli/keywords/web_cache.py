#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/web_cache.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class WebCache(CliKeywordBase):

    """Web Cache Configuration."""

    def get_keyword_names(self):
        return [
            'web_cache_evict',
            'web_cache_add',
            'web_cache_delete',
            'web_cache_list',
            'web_cache_describe',
        ]

    def web_cache_evict(self, entry=DEFAULT):
        """Remove URL from the cache.

        webcache > evict

        Parameters:
        - `entry`: the URL to be removed from the cache.

        Examples:
        | Web Cache Evict | entry=qa19.qa |
        """
        self._cli.webcache().evict(entry)

    def web_cache_describe(self, entry=None):
        """Describe URL cache status.

        webcache > describe

        Parameters:
        - `entry`: string with URL to display its cache status.

        Examples:
        | Web Cache Describe | entry=qa19.qa |
        | ${output}= | Web Cache Describe | entry=qa19.qa |
        """

        if entry is not None:
            output = self._cli.webcache().describe(entry)
            self._info(output)
            return output

        else:
            raise ValueError('Entry is mandatory.')

    def web_cache_add(self, entry=DEFAULT, type=None):
        """Add new entries.

        webcache > ignore > new

        Parameters:
        - `entry`: enter new url or domain values.
        - `type`: specify type. Either 'Domain' or 'URL'.

        Example:
        | Web Cache Add | entry=google.com | type=Domain |
        | Web Cache Add | entry=http://test.com/test.png | type=Url |
        """

        if type and type.strip().lower() == 'domain':
            input_dict={'domain':[entry, DEFAULT]}
            self._cli.webcache().ignore().domains().add(input_dict)

        elif type.strip().lower() == 'url':
            input_dict={'url':[entry, DEFAULT]}
            self._cli.webcache().ignore().urls().add(input_dict)

        else:
            raise ValueError('Type should be either domain or URL.')

    def web_cache_delete(self, entry=DEFAULT, type=None):
        """Delete existing entry.

        webcache > ignore > delete

        Parameters:
        - `entry`: enter url or domain values to be deleted.
        - `type`: specify type. Either 'Domain' or 'URL'.

        Examples:
        | Web Cache Delete | entry=test1.com | type=domain |
        | Web Cache Delete | entry=http://test2.com/test.png  | type=url |
        """

        if type and type.strip().lower() == 'domain':
            self._cli.webcache().ignore().domains().delete(entry.strip())
        elif type.strip().lower() == 'url':
            self._cli.webcache().ignore().urls().delete(entry.strip())
        else:
            raise ValueError('Type should be either domain or URL.')

    def web_cache_list(self, type=None):
        """List entries.

        Parameters:
        - `type`: specify type. Either 'Domain' or 'URL'.

        Examples:
        | Web Cache List | type=domain |
        | ${output}= | Web Cache List | type=domain |
        | ${output}= | Web Cache List | type=url |
        """

        if type and type.strip().lower() == 'domain':
            output = self._cli.webcache().ignore().domains().list()
        elif type.strip().lower() == 'url':
            output = self._cli.webcache().ignore().urls().list()
        else:
            raise ValueError('Type should be either domain or URL.')
        self._info(output)
        return output

