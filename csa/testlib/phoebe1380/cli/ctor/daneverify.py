#!/usr/bin/env python
"""
    SARF CLI ctor - daneverify
"""

import clictorbase as ccb


class daneverify(ccb.IafCliConfiguratorBase):

    def __call__(self, domain):
        self.clearbuf()
        self._writeln('daneverify')
        self._query_response(domain)
        self._query_response('N')
        self._to_the_top(1)
        return self.getbuf()

