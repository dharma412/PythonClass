#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/webcache.py#1 $

"""
IAF 2 CLI command: webcache
"""

import clictorbase
from clictorbase import IafCliError, REQUIRED, DEFAULT, \
                        IafCliParamMap, IafCliConfiguratorBase

class webcache(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        self._writeln('webcache')
        return self

    def evict(self, target_url=''):
        self._query_response('EVICT')
        self._query_response(target_url)
        self._to_the_top(self.newlines)

    def describe(self, target_url=''):
        self._query_response('DESCRIBE')
        self._query_response(target_url)
        self._expect('\n')
        out = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        return out

    def ignore(self):
        self._query_response('IGNORE')
        return webcacheIgnore(self._get_sess())

class webcacheIgnore(clictorbase.IafCliConfiguratorBase):
    """webcache -> ignore"""
    def __call__(self):
        self._writeln('IGNORE')
        return self

    def domains(self):
        self._query_response('DOMAINS')
        return webcacheIgnoreDomains(self._get_sess())

    def urls(self):
        self._query_response('URLS')
        return webcacheIgnoreUrls(self._get_sess())

class webcacheIgnoreDomains(clictorbase.IafCliConfiguratorBase):
    """webcache -> ignore -> domains"""
    newlines = 3

    def delete(self, entry=None):
        self._query_response('DELETE')
        if entry != None:
            self._query_select_list_item(entry)
        self._writeln()
        self._to_the_top(self.newlines)

    def add(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['domain']    = ['new domain values', [DEFAULT, DEFAULT]]
        param_map.update(input_dict or kwargs)

        self._query_response('ADD')
        return self._process_input(param_map)

    def list(self):
        self._query_response('LIST')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        return raw

class webcacheIgnoreUrls(clictorbase.IafCliConfiguratorBase):
    """webcache -> ignore -> urls"""
    newlines = 3

    def delete(self, entry=None):
        self._query_response('DELETE')
        if entry != None:
            self._query_select_list_item(entry)
        self._writeln()
        self._to_the_top(self.newlines)

    def add(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['url']    = ['new url values', [DEFAULT, DEFAULT]]
        param_map.update(input_dict or kwargs)

        self._query_response('ADD')
        return self._process_input(param_map)

    def list(self):
        self._query_response('LIST')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        return raw

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    wc = webcache(cli_sess)

    #webcache -> evict
    wc().evict(target_url='google.com')

    #webcache -> ignore -> domains
    wc().ignore().domains().add(input_dict={'domain':['whatever.qa', DEFAULT]})
    wc().ignore().domains().add(input_dict={'domain':['foo.qa', DEFAULT]})
    list = wc().ignore().domains().list()
    print("Current ignored domain list: %s\n" % list)
    wc().ignore().domains().delete(entry='whatever.qa')
    wc().ignore().domains().delete(entry='foo.qa')

    #webcache -> ignore -> urls
    wc().ignore().urls().add(input_dict={'url':['www.foo.com', DEFAULT]})
    wc().ignore().urls().add(input_dict={'url':['www.bar.com', DEFAULT]})
    list = wc().ignore().urls().list()
    print("Current ignored url list: %s\n" % list)
    wc().ignore().urls().delete(entry='www.foo.com')
    wc().ignore().urls().delete(entry='www.bar.com')

