#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/bvconfig.py#1 $


import clictorbase
from sal.containers.yesnodefault import YES, NO

DEBUG = True


class bvconfig(clictorbase.IafCliConfiguratorBase):
    """bvconfig
    """

    def __call__(self):
        self._writeln('bvconfig')
        return self

    def key(self, key=None):
        # This method will serve dual purpose. It will add a key and also
        # it will return a list of keys used in past. just like a print command.

        self._query_response('key')
        self._query_response(key)
        buf = self._read_until('incoming mail:')
        buf = self._read_until('Choose')
        self._restart()
        # buf contains the list of keys.
        return buf

    def clear(self, disable_bounce_verification=YES):
        # This method will clear the keys based upon the choice to disable
        # the feature.

        self._query_response('clear')
        self._query_response(disable_bounce_verification)
        buf = self._read_until('Choose')
        self._restart()
        # buf contains the list of keys or 'Not configured' message.
        return buf

    def setup(self, behaviour='reject', tag=None, value=None, \
              smart_exceptions=YES):
        self._query_response('setup')
        self._query_select_list_item(behaviour)
        if behaviour.lower() == 'add':
            self._query_response(tag)
            self._query_response(value)
        self._query_response(smart_exceptions)
        self._restart()

    def purge(self, duration='ALL'):
        self._query_response('purge')
        self._query_select_list_item(duration)
        self._restart()


if __name__ == "__main__":
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    bvc = bvconfig(cli_sess)
    bvc().key(key='testfoo')
    bvc().key(key='testfoo1')
    bvc().key(key='testfoo2')
    bvc().setup(behaviour='reject')
    bvc().setup(behaviour='add', tag='X-Ironport', value='test')
    bvc().purge()
    bvc().key(key='testfoo')
    bvc().key(key='testfoo1')
    bvc().key(key='testfoo2')
    bvc().purge(duration='month')
    buf = bvc().key(key='testfoo')
    print buf
    buf = bvc().key(key='testfoo1')
    print buf
    bvc().key(key='testfoo2')
    bvc().purge(duration='year')
    bvc().key(key='testfoo')
    bvc().key(key='testfoo1')
    buf = bvc().key(key='testfoo2')
    print buf
    bvc().purge(duration='ALL')
    bvc().key(key='testfoo')
    bvc().key(key='testfoo1')
    bvc().key(key='testfoo2')
    buf = bvc().clear(disable_bounce_verification=YES)
    print buf
    bvc().key(key='testfoo')
    buf = bvc().clear(disable_bounce_verification=NO)
    print buf
