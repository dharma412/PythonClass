#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/arguments.py#1 $

import re
import sys
import os


class ArgumentParser:
    """
    Common class for parsing arguments
    from Robot Framework's test cases
    """

    # Parsing dictionary of named argument passed as *args
    def _parse_args(self, args):
        kwargs = {}
        for arg in args:
            # convert from unicode to str
            if type(arg) == unicode:
                arg  = arg.encode('utf-8')
            else:
                arg = str(arg)
            pos = arg.find('=')
            key = arg[:pos]
            value = arg[pos + 1:].strip()
            # check for special cases: ${True}, ${False}, ${None}, ${Null}
            if value.upper() in ('TRUE', 'FALSE'):
                value = (value.upper() == 'TRUE')
            elif value.upper() in ('NONE', 'NULL'):
                value = None
            kwargs[key] = value
        return kwargs

    # Convert string of comma separated values into list
    def _convert_to_list(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = [item.strip() for item in user_input.split(',')]
        return user_input

    # Convert string of comma separated values or list into tuple
    def _convert_to_tuple(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple(filter(None,
                                      (item.strip() for item in user_input.split(','))))
        if isinstance(user_input, list):
            user_input = tuple(user_input)
        return user_input

    # Converts a string of comma-separated pairs to a dictionary
    def _convert_to_dictionary(self, user_input):
        """
        Converts a string of comma-separated pairs to a dictionary
        Items in a pair are separated by a colon and are construed as key:value
        Both key and value are trimmed from heading and tailing spaces
        Missing keys and values are interpreted as empty strings
        Example:
        string "Adult:block, aghk:23d,  2 : w6546, a aaa: b  "
        is converted to:
        {'Adult':'block', 'aghk':'23d', '2':'w6546', 'a aaa':'b'}
        """
        _result = {}
        _array = user_input.split(',')
        for _pair in _array:
            _pos = _pair.find(':')
            if _pos < 0:
                _result[_pair.strip()] = ''
            else:
                _result[_pair[0:_pos].strip()] = _pair[_pos + 1:].strip()

        return _result

    def _convert_to_tuple_from_colon_separated_string(self, user_input):
        """Converts a string of comma-separated values to tuple.
        """
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError('Argument \'%s\' should be string type.' % \
                             (user_input,))
        return user_input

    # Get testdata location
    def _get_testdata_dir(self):
        testlib = ''
        for path in sys.path:
            if path.endswith('testlib'):
                testlib = path
                break
        sarf_home = os.path.dirname(os.path.abspath(testlib))
        testdata = os.path.join(sarf_home, 'tests/testdata')
        return testdata

    # get absolute path to the file
    def _get_absolute_path(self, filepath):
        if filepath.startswith('/'):
            # return absolute path as is
            return filepath
        else:
            # assume that relative path relies on tests/testdata/ directory
            return os.path.join(self._get_testdata_dir(), filepath)

    def _normalize(self, s, use_normalize=True):
        """
        Normalize strings that should be used as key
        of dictionary(attribute of CfgHolder class).
        """
        if not use_normalize:
            return s
        tmp = re.sub('[\\W\\d]', '_', s)
        return tmp.lower()
