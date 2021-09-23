#!/usr/bin/env python
""" Module to contain everything for client-side commandd operations, including
the HTTP client to get and set variables, a helper class to provide list and dictionary
operations, and a CLI interface to the helper class.
"""

__docformat__ = "restructuredtext en"

import httplib
import sys
import time
from sets import Set

# For CLI interface
import getopt
import sys
import socket


class VarstoreException(Exception):
    pass


class VarstoreHTTPClient:
    """ Client class to interact with the QA backdoor commandd HTTP server.

        As of right now the only exposed interface is the ability to get and set
        values of commandd variables in the current level."""

    def __init__(self, host, port=8123, debug=False):
        self.hc = httplib.HTTPConnection(host, port)
        if debug: self.hc.set_debuglevel(10)

    def _check_response(self, hr):
        """ If the HTTP response from varstore is not 200, raise an exception. """
        if hr.status != 200:
            raise VarstoreException, "HTTP Error: %s %s\nVarstore Error: %s" % (hr.status, hr.reason, hr.read())

    ### In the future, we may support changing variables at various levels
    def get_var(self, varname):
        """ Issue a HTTP GET to fetch the value of the commandd variable on the
        server.

        If the machine is in cluster mode this request will only fetch the
        value of the variable for the current level.

        Parameters:
            - `varname`: Name of the commandd (varstore) variable whose value
            will be fetched.

        Return:
            A python object created from the text of the HTTP response body.

        Exceptions:
            - `VarstoreException`: Will be raised if you request a non-existent
            variable or if anything but an HTTP 200 response is received.

        Examples:
        | @{groups}= | Commandd Get Var | prox.acl_rules.policy_groups |
        | ${sophos_enabled}= | Get From Dictionary | @{groups}[0] | sophos_enabled |
        | Log | ${sophos_enabled} |
        """
        self.hc.request('GET', '/varstore/%s' % varname, '', {})
        hr = self.hc.getresponse()
        self._check_response(hr)
        return eval(hr.read())

    def change_var(self, varname, newvalue):
        """ Issue a HTTP PUT to set the value of the commandd variable on the
        server.

        As with `Commandd Get Var`, if the server machine is in cluster mode,
        then this variable will be set for its current level. If verify is
        True, then fetch the varname again after setting it to verify that it
        was properly set.

        Parameters:
            - `varname`: Name of the commandd (varstore) variable whose value
            will be fetched.
            - `newvalue`: Value to set the specified varstore variable to

        Return:
            Body of the HTTP response.

        Exceptions:
            - `VarstoreException`: Will be raised if you try to change a
            non-existent variable, set a variable to the wrong type of object,
            if `newvalue` is not a valid representation of python object, or
            if anything but an HTTP 200 response is received.

        Examples:
        | ${output}= | Commandd Change Var | prox.config.https_optin | yes |
        | Log | ${output} |
        | @{groups}= | Commandd Get Var | prox.acl_rules.policy_groups |
        | ${key}= | Get From Dictionary | @{groups}[0] | sophos_enabled |
        | Set to Dictionary | @{groups}[0] | sophos_enabled | yes |
        | ${output}=  | Commandd Change Var | prox.acl_rules.policy_groups | ${groups} |
        | Log | ${output} |
        """
        encoded_value = repr(newvalue)

        # remove unicode strings get from RF test cases
        start_pos = 0
        while True:
            u_pos = encoded_value.find("u'", start_pos)
            if u_pos == -1:
                # exit when no more unicode string found
                break
            # check number of quotes to see whether u' is a part of value
            # if not then remove u
            if encoded_value[:u_pos].count("'") % 2 == 0:
                encoded_value = encoded_value[:u_pos] + encoded_value[u_pos + 1:]
            else:
                start_pos = u_pos + 2

        self.hc.request('PUT', '/varstore/%s' % varname,
                        encoded_value,
                        {'content-length': len(encoded_value)})
        hr = self.hc.getresponse()
        self._check_response(hr)
        return hr.read()

    def commit(self, commit_comment=None):
        """ Commit changes that have been made using commandd.

        Parameters:
            - `commit_comment`: comment for commit

        Examples:
        | Commandd Commit | my comment |
        """
        header_dict = {}
        if commit_comment:
            header_dict['content-length'] = len(commit_comment)
        self.hc.request('COMMIT', '/varstore', commit_comment, header_dict)
        hr = self.hc.getresponse()
        self._check_response(hr)
        return hr.read()


class VarstoreHelper:
    """ Provide convenience methods for a Varstore Client

    Note that VarstoreHelper operates on python objects as strings, and calls
    eval() where necessary to hand real python objects to the
    VarstoreHTTPClient.
"""

    def __init__(self, vs_client, commit_each=False):
        self.vs_client = vs_client
        self.commit_each = commit_each

    def get_set(self, varname, value=None):
        """ Simple Wrapper around VarstoreHTTPClient.change_var/set_var.

        If value is None perform a 'GET' else perform a 'PUT'

        :Parameters:
            - `varname`: Name of the commandd (varstore) variable whose value will be fetched or set.
            - `value`: If set, this value will be set to the specified varstore variable.

        :Return:
            If we perform a 'GET', then return a python object fetched from the variable store, otherwise
            return a description of the action triggered by VarstoreHTTPClient.change_var

        :Exceptions:
            - `VarstoreException`: See VarstoreHTTPClient.get_var and VarstoreHTTPClient.change_var"""
        if value != None:
            try:
                pyobj = eval(value)
            except:
                pyobj = value
            retval = self.vs_client.change_var(varname, pyobj)
            if self.commit_each:
                self.vs_client.commit()
            return retval
        return self.vs_client.get_var(varname)

    def append(self, list_varname, value):
        """ Append a value to the specified varstore variable. """
        l = self.get_set(list_varname)
        l.append(eval(value))
        return self.get_set(list_varname, l)

    def prepend(self, list_varname, value):
        """ Prepend a value to the specified varstore variable. """
        l = self.get_set(list_varname)
        l.insert(0, eval(value))
        return self.get_set(list_varname, l)

    def remove(self, list_varname, value):
        """ Remove a value from the specified varstore variable. """
        l = self.get_set(list_varname)
        l.remove(eval(value))
        return self.get_set(list_varname, l)

    def lookup(self, dict_varname, key):
        """ Return dict_varname[key] """
        d = self.get_set(dict_varname)
        return d.__getitem__(key)

    def delete(self, dict_varname, key):
        """ Delete dict_varname[key] """
        d = self.get_set(dict_varname)
        d.__delitem__(key)
        # The call to repr(d) is necessary because all functions
        # of VarstoreHelper work on string representations of objects.
        return self.get_set(dict_varname, repr(d))

    def set(self, dict_varname, key, value):
        """ dict_varname[key] = value """
        d = self.get_set(dict_varname)
        d.__setitem__(key, value)
        # The call to repr(d) is necessary because all functions
        # of VarstoreHelper work on string representations of objects.
        return self.get_set(dict_varname, repr(d))


### CLI Interface to commandd/varstore
def usage_and_quit():
    print "Usage: commandd.py <host> <varname>"
    print "       commandd.py <host> <varname> <setval>"
    print "       commandd.py -arp <host> <list_varname> <arg>"
    print "       commandd.py -ld <host> <dict_varname> <key>"
    print "       commandd.py -s <host> <dict_varname> <key> <setval>"
    print '=== General Operations ==='
    print 'Get: commandd.py <host> hermes.omh.good_table'
    print 'Set: commandd.py <host> hermes.omh.good_table "{\'foo.com\':[100,0,0]}"'
    print '=== List Operations ==='
    print 'Append: commandd.py -a <host> prox.etc.profiles "acl admin_bl_src_ip SRC 1.2.6.5"'
    print 'Prepend: commandd.py -p <host> prox.etc.profiles "acl all src all"'
    print 'Remove: commandd.py -r <host> prox.etc.profiles "acl all src all"'
    print '=== Dictionary Operations ==='
    print 'Dictionary Lookup: commandd.py -l <host> hermes.omh.goodtable webtv.net'
    print 'Dictionary Set: commandd.py -s <host> hermes.omh.goodtable foo.com "[100,0,0]"'
    print 'Dictionary Delete: commandd.py -d <host> hermes.omh.goodtable webtv.net'
    sys.exit(1)


def f_wrap(func, *args):
    """ Wrap VarstoreHelper functions to catch errors gracefully """
    try:
        return func(*args)
    except AttributeError:
        print "List/Dictionary operations must be used with a commandd list/dictionary variable"
        usage_and_quit()
    except KeyError, ke:
        print "Dictionary variable does not have key: %s" % args[0]
        sys.exit(1)
    except ValueError, ve:
        print "List variable does not contain item: %s" % args[0]
        sys.exit()


def main(argv):
    import pprint
    # process command line args
    try:
        opts, args = getopt.getopt(argv, 'arplsd')
        if not opts:
            opts.append(('', ''))
    except getopt.GetoptError:
        usage_and_quit()

    # Can only have one option and must have at least 2 args
    if len(opts) != 1 or len(args) < 2:
        usage_and_quit()

    # This is the lone option (or '' if no options)
    opt = opts[0][0]

    # Verify that the option corresponds to number of args
    len_dict = {2: ('',),
                3: ('', '-a', '-r', '-p', '-l', '-d'),
                4: ('-s',)}
    if opt not in len_dict.get(len(args), []):
        usage_and_quit()

    vs_client = VarstoreHTTPClient(args.pop(0))
    vsc_helper = VarstoreHelper(vs_client, commit_each=True)

    # Since we have checked the number of args, we can blindly
    # pass the VarstoreHTTPClient object and the list of args
    # to the function that corresponds to the supplied option.
    func_dict = {'': vsc_helper.get_set,
                 '-a': vsc_helper.append,
                 '-r': vsc_helper.remove,
                 '-p': vsc_helper.prepend,
                 '-l': vsc_helper.lookup,
                 '-s': vsc_helper.set,
                 '-d': vsc_helper.delete}

    try:
        pprint.pprint(f_wrap(func_dict[opt], *args))
    except VarstoreException, ve:
        # XXX: If we get HTML, then we've hit a QA Backdoor without the varstore changes.
        if str(ve).find('<title>Error response</title>') != -1:
            print "Varstore Error: Host %s does not serve varstore HTTP requests" % vs_client.hc.host
        else:
            print ve
    except socket.error, se:
        # XXX: Handle network errors gracefully
        print "Network Error: %s" % str(se)


if __name__ == '__main__':
    main(sys.argv[1:])
