#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/requests.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from __future__ import with_statement

__docformat__ = "restructuredtext en"

import sys, os
import types

import common.Variables

# Use HTTPMessage to parse HTTP headers from a file
from httplib import HTTPMessage

# Use md5 to calculate md5 of actual HTTP response bodies
import md5

# We need the re module to parse output from curl
import re

# copy is used in the __add__ methods to create new objects
import copy

# urllib for utility functions splithost and splittype
# to extract host to connect to from a URL
import urllib

# We need to sleep!
import time

# Catch socket.error
import socket

from sal.exceptions import WGATestToolException, WGATestToolError
from sal.deprecated.runcmd import run_cmd
from common.util.utilcommon import UtilCommon

# Do we use Curl or Python to generate a given HTTP request?
CURL = 0
PYTHON = 1

# What type of Authentication are we using?
BASIC = 0
NTLM = 1

REGEX = 12
SUBSTR = 13
FILE = 14
ERROR = 15

import tempfile

tmpdir = tempfile.gettempdir()


####### Module convenience method(s) #######
class Requests(UtilCommon):
    """ Keywords for sending/verifying HTTP, HTTPS and FTP requests """

    def get_keyword_names(self):
        return [
            'send_request',
            'verify_response',
        ]

    def verify_response(self, response, *args):
        """
        Verify a response from HTTP, HTTPS and FTP requests

        Parameters:

            - `response` : required, returned value from execution of the
              keyword 'Send Request'

            - `error_message` : optional, default - independent message for each exception.
              Message that will be displayed in the time of an exception;

            - `message_numbers` : optional, default - the last message.
              numbers of HTTP messages that will be verified.

              *allowed values:*
              | All | all http messages |
              | -1 | last http message |
              | 0 | first http message |
              | 0,1,-1 | first, second and last http messages |

            - `attribute_name` : optional, default - nothing.

              *allowed attributes that can be verified:*
              | status | value of a status for HTTP message |
              | body_size | size of body of  HTTP message, in bytes |
              | body_md5 | md5 sum for body of  HTTP message |
              | version | version of HTTP message, it may be '1.1' or '1.0' |
              | uri | value of uniform resource identifier that was used |
              | protocol | value of rotocol that was used, it may be 'HTTP', 'HTTPS', 'FTP' |
              | headers.date | date from HTTP header |
              | headers.server | detailed information about server from HTTP header |
              | headers.vary | value of vary field from HTTP header |
              | headers.content-length | length of content from HTTP header |
              | headers.content-type | type of content from HTTP header |

        Return:
        None

        Exception:
        | `ValueError` | if response is empty |
        |  | if not allowed attribute is used |
        |  | if attribute is absent in response |
        |  | if mismatch occurs |

        Examples:
        | Verify Response |  ${response} | status=200 | version=1.1 |
        | Verify Response |  ${response} | status=200 | protocol=https | message_numbers=all |
        | Verify Response |  ${response} | version=1.1 | error_message=We have a trouble. Please call a boss. |
        | Verify Response |  ${response} | protocol=https | headers.content-type=text/html | message_numbers=0, -1 |
        | Verify Response |  ${response} | status=301 | message_numbers=0 | error_message=We have a trouble. Please call a boss. |
        """
        # attributes that can be verified
        attribute_set = ['status', 'body_size', 'body_md5',
                         'version', 'uri', 'protocol',
                         'headers.date', 'headers.server', 'headers.vary',
                         'headers.content-length', 'headers.content-type']

        # making a list of responses
        response_list = []
        if isinstance(response, list):
            response_list.extend(response)
        else:
            response_list.append(response)

        kwargs = self._parse_args(args)
        # selection of message numbers
        message_numbers = []
        if kwargs.has_key('message_numbers'):
            message_number = kwargs['message_numbers']
            if message_number.lower() == 'all':
                message_numbers = [ind for ind in \
                                   xrange(len(message_number) - 1)]
            else:
                message_numbers = re.findall(r'(-?\d)', message_number)
            del kwargs['message_numbers']
        else:
            message_numbers.append(-1)

        # selection of error message for displaying when an exception occurs
        if kwargs.has_key('error_message'):
            error_message_about_empty_response = \
                kwargs['error_message']
            error_message_about_not_existing_attribute = \
                kwargs['error_message']
            error_message_about_incorrect_attribute = lambda attr: \
                '%s%s' % (kwargs['error_message'], attr)
            error_message_about_mismatch = lambda attr, exist, expect: \
                '%s%s%s%s' % (kwargs['error_message'], attr, exist, expect)
            del kwargs['error_message']
        else:
            error_message_about_empty_response = 'Response is empty'
            error_message_about_not_existing_attribute = \
                'Expected attribute is absent'
            error_message_about_incorrect_attribute = lambda attr: \
                'Incorrect attribute was used(%s).' % (attr)
            error_message_about_mismatch = lambda attr, exist, expect: \
                'Expected(%s) and existing(%s) values are different for' \
                ' attribute(%s)' % (exist, expect, attr)

        # generating an exception when a list of  responses is empty
        if len(response_list) < 1:
            raise ValueError(error_message_about_empty_response)

        # running over each message number
        for message_number in message_numbers:
            message_number = int(message_number)

            # running over each given attribute
            for expected_attribute in kwargs:
                expected_attributes = (expected_attribute.lower()).split('.')

                # exception occurs when an attribute name is not handled
                if expected_attribute not in attribute_set:
                    raise ValueError(error_message_about_incorrect_attribute( \
                        expected_attribute))
                if hasattr(response_list[message_number],
                           expected_attributes[0]):

                    if len(expected_attributes) == 1:
                        # attribute name is consisted of one part
                        existing_value = str(getattr(
                            response_list[message_number],
                            expected_attributes[0]))

                        if existing_value.lower() != \
                                (str(kwargs[expected_attribute])).lower():
                            raise ValueError(error_message_about_mismatch(
                                expected_attribute,
                                existing_value,
                                kwargs[expected_attribute]))
                    else:
                        # attribute name is consisted of two parts
                        attribute = getattr(response_list[message_number],
                                            expected_attributes[0])
                        present_attribute = 0

                        # search of the second part of an attribute name
                        for (key, value) in attribute:
                            if (str(key)).lower() == expected_attributes[1]:
                                present_attribute = 1
                                if (str(value)).lower() == \
                                        (str(kwargs[expected_attribute])).lower():
                                    present_attribute = 2

                        if present_attribute == 0:
                            # exception occurs when the second part
                            # of an attribute name is not found
                            raise ValueError(
                                error_message_about_not_existing_attribute)
                        elif present_attribute == 1:
                            # exception occurs when expected value
                            # of an attribute is different from existing
                            raise ValueError(error_message_about_mismatch(
                                expected_attribute,
                                '',
                                kwargs[expected_attribute]))
                else:
                    # exception occurs when an attribute name is not existing
                    raise ValueError(error_message_about_not_existing_attribute)

    def send_request(self, *args):
        """
        Send HTTP, HTTPS and FTP requests using curl

        Parameters:

            - `retry_on_net_error`: retry sending requests if network error
              occurs. If True 4 attempts will be made before raising exception,
              by default False value is used and one attempt to send request is
              made. Possible values either True/False or Yes/No

            - `uri`: URI of the requested page.
            - `uri_file`: path to file of URIs. Multiple URI is specifies as
              separate line in the file.
            - `uri_list`: string of comma separated values of list of URIs.

              Note: Only one of above three parameters `uri`, `uri_file`, `url_list`
              can be used simultaneously. If any two of them are specified
              then respective exception is raised.

            - `cookies`: whether use cookies or not. Possible values: Yes/No,
              True/False. True is used by default. If True or Yes then following
              parameters will be added to curl command: '-l --location-trusted
              -c /dev/null'

            - `version`: version of HTTP to specify in request. For example: 1.0
              or 1.1. No need to be specified for FTP requests.

            - `method`: Specifies a custom request method to use when
              communicating with the HTTP server.  The specified request will be
              used instead of the method otherwise used (which defaults to GET).

            - `proxy`: <proxyhost[:port]>
              Use the specified HTTP proxy. If the port number is not specified,
              it is assumed at port 1080.

            - `http_connect`: When  an  HTTP proxy is used (`proxy` parameter
              specified), this option will cause non-HTTP protocols to attempt to tunnel
              through the proxy instead of merely using it to do HTTP-like
              operations. The tunnel approach is made with the HTTP proxy
              CONNECT request and requires that the proxy allows direct connect
              to the remote port number curl wants to tunnel through to.
              Possible values True/False or Yes/No.

            - `bind_ip`: IP Address to use when performing request.

            - `validate_certs`: validate server certificates. If True/Yes is
              passed then valid certificate is expected, when False/No - invalid
              certificate is expected. By default None is used and certificate
              is not verified.

            - `proxy_auth`: <authentication type:user:password> authentication
              type, the user name and password to use for proxy authentication.
              Authentication type is either 'basic' or 'NTLM'.
            - `http_auth`: <authentication type:user:password> authentication
              type, the user name and password to use for server authentication.
              Authentication type is either 'basic' or 'NTLM'.

            - `headers`: a string of comma separated pairs: header:value to be
              added to request

            - `form_data`: send POST data using the Content-Type
              multipart/form-data according to RFC1867.
              This  enables  uploading of binary files etc. To force the 'con-
              tent' part to be a file, prefix the file name with an @ sign. To
              just get the content part from a file, prefix the file name with
              the symbol <. The format of this parameter is
              <name:content>[;<name2:content2>]. The value will be passed to the
              `curl -F` parameter (before passing to the curl colons ':' will be
              replaced with equal signs '=')

              Note: if form_data is used for uploading files then either full
              path to the file or relative to the $SARF/tests/testdata
              directory.

            - `use_remote_name`: write output to a local file named like the
              remote file we get. (Only  the file part of the remote file is
              used, the path is cut off.) The remote file name to use for
              saving is  extracted  from  the given URL, nothing else.
              Either True (yes) or False (no). If True then curl option '-O' will be added.
              By default False.

            - `timeout`: set maximal time for request operation. Default value
              is 60 seconds. This value will be passed to 'curl -m' parameter.

        Examples:
        | Send Request | uri=https://www.google.com |
        | ... | proxy=${DUT}:80 |
        | Send Request | uri_list=http://www.google.com, https://www.yahoo.com |
        | Send Request | uri_file=%{SARF_HOME}/tests/testdata/uri_file.txt |
        | Send Request | uri=http://services.wga/test-data |
        | ... | headers=X-Server-Config: BYPASS-ACCESSFILE = 1 |
        | ... | proxy=${DUT}:80 |
        | ... | proxy_auth=basic:admin:ironport |
        | ... | http_auth=basic:admin:ironport |
        | ... | cookies=No |
        | ... | bind_ip=10.7.1.250 |
        | ... | version=1.1 |
        | ... | method=POST |
        | Send Request | uri=https://www.google.com |
        | ... | retry_on_net_error=Yes |
        | ... | validate_certs=Yes |
        | Send Request | uri=ftp://ftp.freebsd.org |
        | ... | proxy=${DUT}:80 |
        | ... | http_connect=Yes |
        | # upload file |
        | Send Request | uri=http://vm10bsd150.wga/upload |
        | ... | from_data=foo:@cert.crt |
        | # download file |
        | Send Request | uri=http://vm10bsd150.wga/uploads/cert.crt |
        | ... | use_remote_name=yes |
        | Send Request | uri=http://services.wga/test-data/cache/1GBfile |
        | ... | timeout=1200 |
        """

        # parse arguments from RobotFramework
        kwargs = self._parse_args(args)

        # parse list values
        list_values = ['headers', 'uri_list']
        for value in list_values:
            if kwargs.has_key(value):
                kwargs[value] = self._convert_to_list(kwargs[value])

        # parse boolean values
        boolean_values = ['validate_certs',
                          'cookies',
                          'retry_on_error',
                          'http_connect',
                          'use_remote_name', ]
        for value in boolean_values:
            if kwargs.has_key(value):
                bool = kwargs[value].lower()
                if bool == 'yes' or bool == 'true':
                    kwargs[value] = True
                elif bool == 'no' or bool == 'false':
                    kwargs[value] = False
                else:
                    raise ValueError("Incorrect value of '%s' parameter. " \
                                     "Expected either True/False or Yes/No" % value)
                # validate_certs expect string values 'True' or 'False'
                if value == 'validate_certs':
                    kwargs[value] = str(kwargs[value])

        # parse auth values
        auth_values = ['proxy_auth', 'http_auth']
        for value in auth_values:
            if kwargs.has_key(value):
                try:
                    auth_type, auth_user, auth_password = tuple([item.strip() \
                                                                 for item in kwargs[value].split(':')])
                    kwargs[value] = (auth_type.lower(), auth_user + ':' +
                                     auth_password)
                except:
                    raise ValueError("Incorrect value of '%s' parameter. " \
                                     "Expected string 'auth_type:user:password'" % value)

        # parse form_data values
        if kwargs.has_key('form_data'):
            form_fields = kwargs['form_data'].split(';')
            for i in range(len(form_fields)):
                key, value = form_fields[i].split(':')
                # handle file values
                if value[0] in ('<', '@'):
                    value = value[0] + self._get_absolute_path(value[1:])
                form_fields[i] = key + '=' + value
            kwargs['form_data'] = ';'.join(form_fields)

        # this parameter is not for request
        retry_on_net_error = kwargs.get('retry_on_net_error', False)
        if kwargs.has_key('retry_on_net_error'):
            del kwargs['retry_on_net_error']

        # This code has been inserted to create more
        # robust test cases with fewer calls to time.sleep()
        # due to config changes restarting the proxy.
        for attempt_num in range(4):
            try:
                return self._request(**kwargs)
            except socket.error:
                if not retry_on_net_error or attempt_num == 3:
                    raise
                self._info("Sleeping 5 seconds due to network error")
                time.sleep(5)

    def _request(self, **kwargs):
        responses = Request(**kwargs).run()
        if type(responses) == type([]):
            resp_list_list = [Response(resp).expand() for resp in responses]
        else:
            resp_list_list = [Response(responses).expand()]
        ret_list = []
        for resp_list in resp_list_list:
            for resp in resp_list:
                ret_list.append(resp)
        if len(ret_list) == 1:
            return ret_list[0]
        return ret_list


def _or(x, y):
    """ This _or function differs from the or builtin function in that a Non-None
    object will always be returned when or-ed with a None object.
    """
    if y == None and not x:
        return x
    if x == None and not y:
        return y
    return x or y


###### End Module convenience methods ######

class WGAClientSideError(Exception):
    pass


class Request(UtilCommon):
    """ wga_test_client.Request is a class that holds the parameters for one HTTP request.

Request knows how to execute the request, and will use CurlController to do so.
to use. More HTTP Connection classes can be supported as long as they implement set_params(request_obj)
and run() methods. Another requirement is that the run() method return an HTTPResponse one-tuple or a
two-tuple that points to a response header file and a response body file.
"""

    def __init__(self, **kwargs):
        """ Create Request object by loading values passed in via **kwargs.
"""
        # initialize all attributes to None, False, or []
        self.uri, self.body, self.version, self.method, self.proxy = (None,) * 5
        self.uri_file = self.use_http_connect = self.uri_list = self.bind_ip = None

        # I'm trying something new. Instead of using a class to tie 3 pieces of information together,
        # I'm using a dictionary. The keys in these dicts will be "user", "password", and "type"
        self.proxy_auth = {}
        self.http_auth = {}

        # By default have no delay
        self.delay = 0.0

        # self.host will be set to this request's Host header if there is one.
        self.host = None
        self.headers = []

        # Unless we find a different protocol, assume HTTP
        self.protocol = 'HTTP'

        # Unless specified, no verification of Server SSL Certificates
        self.validate_certificates = None

        # Satisfy cookielib
        self.unverifiable = False

        self.use_cookies = True

        # form data variable
        self.form_data = None

        # download file with the remote name
        self.use_remote_name = False

        # max timeout for operation
        self.timeout = '60'

        for arg in kwargs.keys():
            if hasattr(self, 'set_%s' % arg):
                # Get the set_* method
                exec ('set_func = self.set_%s' % arg)

                # Does it have multiple args? Make sure the user passes
                # the right types of sequences.
                if set_func.func_code.co_argcount > 2:
                    if type(kwargs[arg]) not in (type([]), type(())):
                        raise WGATestToolException, "Function %s takes multiple " \
                                                    "arguments, which need to be " \
                                                    "passed to Request as a list " \
                                                    "or tuple"
                    set_func(*kwargs[arg])
                else:
                    set_func(kwargs[arg])
            else:
                raise WGATestToolException, "kwargs in Request.__init__ should always point to a set function"

    #### SET/ADD METHODS ####
    ## Most of these are very boring, but needed :) ##
    def set_uri(self, uri):
        if self.uri_file:
            raise WGATestToolException, "No uri can be set if uri_file is already set"
        self.uri = uri
        self._set_protocol()

    def set_uri_file(self, uri_file):
        if self.uri:
            raise WGATestToolException, "No uri_file can be set if uri is already set"
        self.uri_file = uri_file

    # This is a Python only attribute setting.
    def set_uri_list(self, uri_list):
        self.uri_list = []
        for uri in uri_list:
            self.uri_list.append(uri)

    def set_cookies(self, use_cookies):
        self.use_cookies = use_cookies

    def set_http_connect(self, use_http_connect):
        self.use_http_connect = use_http_connect

    def set_validate_certs(self, validate_certs):
        self.validate_certificates = validate_certs

    def set_body(self, body):
        self.body = body

    def set_version(self, version):
        self.version = version

    def set_method(self, method):
        self.method = method

    def set_proxy(self, proxy):
        self.proxy = proxy

    # Leave here so that things don't break
    def set_force_curl(self, force_curl):
        pass

    def set_bind_ip(self, bind_ip):
        self.bind_ip = bind_ip

    def set_proxy_auth(self, auth_type, auth_str):
        self._set_auth(self.proxy_auth, auth_type, auth_str)

    def set_http_auth(self, auth_type, auth_str):
        self._set_auth(self.http_auth, auth_type, auth_str)

    def _set_auth(self, auth_dict, auth_type, auth_str):
        """ Set parameters of this request relating to authentication. """
        auth_dict['type'] = {'basic': BASIC, 'ntlm': NTLM}.get(auth_type)
        if auth_dict['type'] == None:
            raise WGATestToolException, "Only authentication types are 'basic' and 'ntlm'"
        user_passwd_list = auth_str.split(':')
        if len(user_passwd_list) != 2:
            raise WGATestToolException, "<proxy_auth> and <http_auth> tags must specify a user and password separated by a ':'"
        auth_dict['user'], auth_dict['passwd'] = user_passwd_list

    def set_headers(self, headers):
        """ set_headers --> None

        Process the headers into (header, value) 2-tuples. At the same time, replace all
        XML config variables with actual values.
        """
        if headers is not None:
            for header in headers:
                header_value_pair = [s.strip() for s in str(header).split(':', 1)]
                if header_value_pair and len(header_value_pair) == 2:
                    self.headers.append(header_value_pair)

                    # If there is Host header defined, then we want to keep track of it
                    if header_value_pair[0] == 'Host':
                        self.host = header_value_pair[1]
                elif header_value_pair and len(header_value_pair) == 1:
                    raise WGATestToolException, "Headers must all be 2 tokens (even empty) separated by a ':'"

    def set_delay(self, delay):
        if not delay: return
        try:
            # Do the whole float(str(x)) thing to be compatible xmltramp objects.
            self.delay = float(str(delay))
        except ValueError:
            raise WGATestToolException, "delay must be an integer or floating point number."

    def _set_protocol(self):
        """ Use the uri attribute to set the protocol for this request. Otherwise use HTTP. """
        if not self.uri:
            self.protocol = 'HTTP'
        else:
            self.protocol = urllib.splittype(self.uri)[0] or 'HTTP'
        self.protocol = self.protocol.upper()

    def set_form_data(self, form_data):
        self.form_data = form_data

    def set_use_remote_name(self, use_remote_name):
        self.use_remote_name = use_remote_name

    def set_timeout(self, timeout):
        self.timeout = timeout

    #### QUERY METHODS ####
    def _uses_auth(self):
        if self.proxy_auth or self.http_auth:
            return True
        return False

    def _has_abs_url(self):
        """ Does this request have an absolute URI defined?  """
        return self.uri.find('http://') == 0 or \
               self.uri.find('https://') == 0 or \
               self.uri.find('ftp://') == 0

    def _has_empty_header(self):
        """ Does this request have any headers defined that have empty values? """
        for header, value in self.headers:
            if value == '':
                return True
        return False

    def _header(self, name):
        """ Does this request have any headers of 'name'? If so, return the value """
        for header, value in self.headers:
            if header.lower() == name.lower(): return value
        return None

    def _get_header_str(self):
        """ Return a string representation of this request's HTTP headers """
        ret_val = ''
        for header, value in self.headers:
            ret_val += '\t%s: %s\n' % (header, value)
        return ret_val

    def get_connect_host(self):
        """ Get the host for this request to connect to.

        So while curl will connect to either the real host or the given proxy, CustomHTTPConnection needs
        to be told where to connect. If there is a proxy defined, then we do want to connect there, but
        if not, we want to connect to the "Host" or the host defined in the uri. (If any) If neither of those
        are defined, then we must fail.
        """
        if self.proxy:
            return self.proxy
        if self.host:
            return self.host
        uri_host = urllib.splithost(urllib.splittype(self.uri)[1])[0]
        if uri_host:
            return uri_host
        raise WGATestToolException, "A request must have at least a proxy address, a Host header, or an absolute URI to make a connection"

    def _curl_okay(self):
        """ Curl needs a few conditions to be true to process a WGA Test Tool request. """
        return not self.body and \
               self._has_abs_url()

    def __str__(self):
        """ Return a string representation of this request. Only include non-default settings. """
        http_connect_str = ''
        validate_cert_str = {None: 'Off', 'True': 'Must Validate', 'False': 'Must NOT Validate'}[
            self.validate_certificates]
        retval = ''
        if self.uri: retval += 'URI: %s\n' % self.uri
        if self.protocol == 'HTTPS':
            retval += 'VALIDATE_CERTIFICATES: %s\n' % validate_cert_str
        if self.uri_file: retval += 'URI_FILE: %s\n' % self.uri_file
        if self.body: retval += 'BODY: %s\n' % self.body
        if self.version: retval += 'VERSION: %s\n' % self.version
        if self.method: retval += 'METHOD: %s\n' % self.method
        if self.use_http_connect: http_connect_str = 'USING HTTP CONNECT'
        if self.proxy: retval += 'PROXY: %s %s\n' % (self.proxy, http_connect_str)
        if self.proxy_auth:
            retval += 'PROXY_USER: %s\n' % self.proxy_auth['user']
            retval += 'PROXY_PASSWD: %s\n' % self.proxy_auth['passwd']
            retval += 'PROXY_AUTH_TYPE: %s\n' % {BASIC: 'basic', NTLM: 'ntlm'}[self.proxy_auth['type']]
        if self.http_auth:
            retval += 'HTTP_USER: %s\n' % self.http_auth['user']
            retval += 'HTTP_PASSWD: %s\n' % self.http_auth['passwd']
            retval += 'HTTP_AUTH_TYPE: %s\n' % {BASIC: 'basic', NTLM: 'ntlm'}[self.http_auth['type']]
        if self.host: retval += 'HOST HEADER: %s\n' % self.host
        if self.headers:
            retval += 'ADDED HTTP HEADERS: \n%s\n' % self._get_header_str()

        return retval

    __repr__ = __str__

    ### Methods to get along with cookielib (mimicing urllib2.Request) ###
    get_header = _header

    def add_unredirected_header(self, key, value):
        """ Mimic urllib2.Request.add_unredirected_header """
        self.headers.append((key, value))

    add_header = add_unredirected_header

    def has_header(self, name):
        """ Mimic urllib2.Request.has_header """
        if self._header(name) != None:
            return True
        else:
            return False

    def get_type(self):
        """ Mimic urllib2.Request.get_type """
        return self.protocol.lower()

    def header_items(self):
        """ Mimic urllib2.Request.header_items """
        return self.headers

    def get_full_url(self):
        """ Mimic urllib2.Request.get_full_url """
        if self._has_abs_url():
            return self.uri
        else:
            return 'http://%s' % self.uri

    def get_host(self):
        """ Mimic urllib2.Request.get_host """
        return self.get_connect_host()

    def is_unverifiable(self):
        """ Mimic urllib2.Request.is_unverifiable """
        return self.unverifiable

    def get_origin_req_host(self):
        """ Mimic urllib2.Request.get_origin_req_host """
        return urllib.splitport(self.get_connect_host())[0]

    ### End cookielib compatibility section ###

    def validate_request(self):
        """ Self validation method.
        """

        # Need to have a uri or a uri_file or a uri_list
        if not (self.uri or self.uri_list or self.uri_file):
            raise WGATestToolException, "A request must have a uri, uri_list, or uri_file"

        # Cannot have a single uri and a file/list to specify multiple uris
        if self.uri and (self.uri_file or self.uri_list):
            raise WGATestToolException, "A request cannot contain both a uri and a uri_file or uri_list"

        # Cannot have a uri_file and a uri_list
        if self.uri_file and self.uri_list:
            raise WGATestToolException, "A request cannot contain both a uri_file and a uri_list"

        # If we're using uri_file, the file must exist before running
        if self.uri_file and not os.path.exists(self.uri_file):
            raise WGATestToolException, "The uri_file specified does not exist: %s" % self.uri_file

        # Cannot do HTTP Tunneling without a forward proxy
        if self.use_http_connect and not self.proxy:
            raise WGATestToolException, "A request cannot use HTTP CONNECT (tunneling) without specifying a proxy"

        # HTTPS and FTP only for tunneling
        if self.use_http_connect and self.protocol not in ('HTTPS', 'FTP'):
            raise WGATestToolException, "HTTP CONNECT (tunneling) is only supported for HTTPS and FTP"

        if self.validate_certificates not in (None, 'True', 'False'):
            raise WGATestToolException, "validate_certificates tag is limited to values of 'True' and 'False'"

        if self.protocol == 'FTP' and (self.use_http_connect or not self.proxy) and \
                (self.method or self.body or self.uri_file or self.version or self.headers or \
                 self.http_auth):
            raise WGATestToolException, "Native FTP requests must not use any HTTP specific request tags."

        # No transparent proxy auth *with* http auth
        if not self.proxy and (self.http_auth and self.proxy_auth):
            raise WGATestToolException, "Curl currently does not support " \
                                        "http_auth with transparent proxy " \
                                        "auth."

    def expand(self):
        """ expand (self) --> List of Request Objects

        This function takes a Request that contains a uri_file or uri_list, and returns a list
        of Requests: one per URI in that file. ALL other attributes stay the same.
        """
        if not (self.uri_list or self.uri_file):
            raise WGATestToolException, "expand method must be called with a uri_list or uri_file"

        req_list = []

        if not self.uri_list:
            f = open(self.uri_file)
            # Allow comments in the uri_file that start with #
            uris = [u.strip() for u in f.readlines() if not u.strip().startswith('#')]
            f.close()
        else:
            uris = self.uri_list

        # We do not want new requests to have the uri_file or uri_list attribute
        self.uri_file = None
        self.uri_list = None

        for uri in uris:
            new_req = copy.deepcopy(self)
            new_req.uri = uri
            new_req._set_protocol()
            req_list.append(new_req)

        return req_list

    def __add__(self, other):
        """ __add__ (other) --> New Request Object

        self + other = New Object

        This overloaded __add__ function combines two requests such that the
        RHS's attributes override the LHS's (or global) attributes.
        """

        new_req = copy.copy(self)
        new_req.uri = _or(other.uri, self.uri)
        new_req._set_protocol()
        new_req.validate_certificates = _or(other.validate_certificates, self.validate_certificates)
        new_req.uri_file = _or(other.uri_file, self.uri_file)
        new_req.body = _or(other.body, self.body)
        new_req.version = _or(other.version, self.version)
        new_req.method = _or(other.method, self.method)
        new_req.proxy = _or(other.proxy, self.proxy)
        new_req.use_http_connect = _or(other.use_http_connect, self.use_http_connect)
        new_req.proxy_auth = _or(other.proxy_auth, self.proxy_auth)
        new_req.http_auth = _or(other.http_auth, self.http_auth)
        new_req.host = _or(other.host, self.host)

        new_headers = []
        for header, value in self.headers:
            if other._header(header) == None:
                new_headers.append((header, value))
        new_headers.extend(other.headers)
        new_req.headers = new_headers
        return new_req

    def run(self, bind_ip=None):
        """ Execute the request via curl or CustomHTTP*Connection.

        We ALWAYS prefer to use CustomHTTPConnection. So if our request
        does not use HTTP or Proxy authentication, we use the pure python method.
        Otherwise, we try to use curl, which will work only for compliant HTTP where
        the URI is absolute. If we cannot use either, we bail.
        authentication is used, then we cannot go on.

        :Parameters:
            - `bind_ip`: Outbound IP to bind to if Non-None.

        :Return:
            A HTTPResponse or CurlResponse object depending on what underlying engine ran the request.

        :Exceptions:
            - `WGATestToolException`: Will be raised if a curl request is attempted with non-compliant HTTP,
              an HTTP request body, empty HTTP headers, or a relative URL.
        """
        self.validate_request()

        if self.uri_list or self.uri_file:
            return self._expand_and_run(bind_ip)

        http_obj = None

        bind_ip_str = ''
        # self.bind_ip attribute takes precedence
        if self.bind_ip:
            bind_ip = self.bind_ip
        if bind_ip:
            bind_ip_str = "-- BIND IP: %s " % bind_ip

        if not self._curl_okay():
            raise WGATestToolException, "Cannot create a request with FTP or authentication and non-compliant HTTP or a relative URL"
        self.request_type = CURL
        http_obj = CurlController(bind_ip)

        http_obj.set_params(self)
        self._debug('\n======= Request: %s =======' % (bind_ip_str,))
        response_obj = http_obj.run(self.body, bind_ip)

        # Load the response object with specific request attributes
        # to keep from passing the request object around.
        response_obj.request_header_str = http_obj.request_header_str
        response_obj.protocol = self.protocol
        response_obj.method = self.method
        response_obj.uri = self.uri

        # Sleep for self.delay milliseconds
        time.sleep(self.delay)

        return response_obj

    def _expand_and_run(self, bind_ip):
        response_list = []
        request_list = self.expand()
        for req in request_list:
            response_list.append(
                req.run(bind_ip)
            )
        return response_list


class CurlResponse:
    """ Struct-like class to hold information from a run of curl.
    (headers, output, return value, exception if any) """

    def __init__(self, headers, output, return_code, curl_exception=None):
        self.header_file = headers
        self.output_file = output
        self.curl_ret_val = return_code
        self.curl_exception = curl_exception


class CurlController(UtilCommon):
    """ This is a simple class to set curl command line options, and to run the full
    command once the options are set.
    """

    def __init__(self, bind_ip=None):
        """ Set the output files and bind_ip if necessary for this curl request """
        self.cmd_line = []
        # create temp dir in user's home directory and use it for keeping body
        # and header files
        # /tmp is very limited in space (1 Gb) on vm10bsd*.wga clients
        tempdir = os.path.join(os.environ['HOME'], 'temp')
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        tempfile.tempdir = tempdir
        # Store the headers and body in temp files
        self.header_file = tempfile.mktemp(prefix='headers.')
        self.output_file = tempfile.mktemp(prefix='body.')
        self.bind_ip = bind_ip
        # Store the request headers string from the Curl output
        self.request_header_str = ''

    def run(self, *not_used):
        """ run() --> response_header_filename, body_filename

        Compose the command line options (created by CurlController.set_params) for curl to
        execute the request. Return a CurlResponse object.
        """
        self._debug('curl CMD LINE: curl %s\n' % ' '.join(self.cmd_line))
        out, err, ret_val = run_cmd('curl %s' % ' '.join(self.cmd_line), timeout=15)
        self.request_header_str, response_header_str = self.process_curl_output(err)
        self._debug(response_header_str)

        return self.curl_error_check(ret_val)

    def process_curl_output(self, output):
        """ Process raw curl output into more readable output that is hopefully more relevant to
        a QA tester/HTTP Engineer.

        :Parameters:
            - `output`: Raw output from curl

        :Return:
            A string that is formatted to be as readable as possible.
        """
        head_re = re.compile('^[A-Za-z-_]+:')
        inlines = output.split('\n')
        outlines = []
        sent_lines = []
        SENT = 0
        RECV = 1
        OTHER = 2
        state = OTHER

        for l in inlines:
            if l.startswith('> '):
                if state == RECV:
                    outlines.append('')
                state = SENT
                outlines.append(l[2:])
                sent_lines.append(l[2:])
            elif l.startswith('< '):
                state = RECV
                outlines.append(l[2:])
            elif l.startswith('error:') or l.startswith('curl:'):
                pass
            elif head_re.search(l):
                outlines.append(l)
                sent_lines.append(l)
            elif not l.strip() and state == SENT:
                outlines.append(l)
                sent_lines.append(l)
                state = OTHER

        return '\n'.join(sent_lines), '\n'.join(outlines)

    def curl_error_check(self, ret_val):
        """ Okay, sometimes curl can fail even though it is not a WGA Test Tool failure case. curl has
        60 or so error codes it can return. Currently, only 19 and 60 affect the WGA Test Tool.

        If there is no error, then all is good. If there is an unrecognized error, raise a WGATestToolException.
        If there is a recognized error that represents a WGA Test Tool Error, then pass that to the response
        checker function via the CurlResponse object that we create here.
        """
        curl_exception = None
        okay_error_codes = [19,  # This means that the FTP file was not fetched correctly, equivalent to HTTP 404
                            60,  # SSL Certificate is Invalid
                            7,  # Connection refused
                            52]  # Empty reply from server
        okay_error = False
        for code in okay_error_codes:
            if ret_val == code or ret_val >> 8 == code:
                okay_error = True
                ret_val = code
                break

        if ret_val and not okay_error:
            raise WGATestToolException, "Call to 'curl' failed! Here is the curl error number: %d" % (ret_val >> 8)
        elif ret_val == 7:
            raise socket.error, "Connection refused"
        elif ret_val == 52:
            # Raise socket error here to auto-retry if the option is set
            raise socket.error, "No reply from server"
        elif ret_val == 60 and self.validate == 'True':
            curl_exception = WGAClientSideError(
                "SSL Server Certificate is not valid. wga_test_client expected a valid Certificate.")
        elif ret_val == 0 and self.validate == 'False':
            curl_exception = WGAClientSideError(
                "SSL Server Certificate is valid when wga_test_client expected an invalid Certificate.")
        elif ret_val == 60 and self.validate == 'False':
            self.cmd_line.insert(0, '-k')
            self.validate = None
            return self.run()

        return CurlResponse(self.header_file, self.output_file, ret_val, curl_exception)

    def set_params(self, request_obj):
        """ Use a Request object to create curl command line options to execute the request. """
        variables = common.Variables.get_variables()
        if variables.has_key("${IPV_PARAM}"):
            self.cmd_line.append(variables["${IPV_PARAM}"])
        else:
            self.cmd_line.append('-4')
        self.protocol = request_obj.protocol
        self.validate = request_obj.validate_certificates

        if request_obj.version == '1.0':
            self.cmd_line.append('-0')
        if request_obj.method:
            self.cmd_line.append('-X %s' % request_obj.method)
        if self.bind_ip:
            self.cmd_line.append('--interface %s' % self.bind_ip)

        # If no proxy is specified but there is proxy_auth, then
        # assume transparent authentication through a proxy.
        if request_obj.proxy_auth and request_obj.proxy:
            self.cmd_line.append('-U %s:%s' % (request_obj.proxy_auth['user'],
                                               request_obj.proxy_auth['passwd']))
            self.cmd_line.append('--proxy-%s' % {BASIC: 'basic', NTLM: 'ntlm'}[request_obj.proxy_auth['type']])
        elif request_obj.proxy_auth and not request_obj.proxy:
            self.cmd_line.append('-u %s:%s' % (request_obj.proxy_auth['user'],
                                               request_obj.proxy_auth['passwd']))
            self.cmd_line.append('--%s' % {BASIC: 'basic', NTLM: 'ntlm'}[request_obj.proxy_auth['type']])

        if request_obj.http_auth:
            self.cmd_line.append('-u %s:%s' % (request_obj.http_auth['user'],
                                               request_obj.http_auth['passwd']))
            self.cmd_line.append('--%s' % {BASIC: 'basic', NTLM: 'ntlm'}[request_obj.http_auth['type']])
        if request_obj.proxy:
            self.cmd_line.append('--proxy %s' % request_obj.proxy)
            if request_obj.use_http_connect:
                self.cmd_line.append('-p')
        for header, value in request_obj.headers:
            self.cmd_line.append("-H '%s: %s'" % (header, value))

        if self.validate == None:
            self.cmd_line.append('-k')
        if self.protocol == 'FTP':
            self.cmd_line.append('--disable-epsv')

        self.cmd_line.append('-D %s' % self.header_file)
        # set name of the output file
        if request_obj.use_remote_name:
            self.cmd_line.append('-O')
        else:
            self.cmd_line.append('-o %s' % self.output_file)
        self.cmd_line.append('-v')

        if request_obj.use_cookies:
            self.cmd_line.append('-l')
            self.cmd_line.append('--location-trusted')
            self.cmd_line.append('-c /dev/null')

        # add form data
        if request_obj.form_data:
            self.cmd_line.append('-F')
            self.cmd_line.append(request_obj.form_data)

        # add timeout
        if request_obj.timeout:
            self.cmd_line.append('-m')
            self.cmd_line.append(request_obj.timeout)

        # This must go last in the curl cmd line
        self.cmd_line.append(request_obj.uri)


class Response:
    """ This class contains logic to compare expected HTTP/HTTPS/FTP response attributes loaded via XML
    with actual response data from httplib.HTTPResponse and request.CurlResponse objects."""

    def __init__(self, resp_obj):
        """ Load response data for future processing/checking

        :Parameters:
            - `resp_obj`: httplib.HTTPResponse or request.CurlResponse or xmlparse XML response tag object.

        :Exceptions:
            - `WGATestToolError`: Internal error checking
        """
        self.status = self.body_size = self.body_md5 = self.version = None
        self.body_match = None
        self.complete = True
        self.headers = []
        self.required_headers = set([])
        self.forbidden_headers = set([])

        # Was this created from real traffic, or is it created test data?
        self.actual_data = True

        # We want to save the HTTP Message object to feed to cookielib
        self.info_hm = None

        # Sometimes Curl makes a series of HTTP requests due to redirection. We want to capture all HTTPMessage
        # objects.
        self.hm_list = []

        if not resp_obj:
            raise WGATestToolError, "Response class no longer initializes without resp_obj"
        else:
            self.populate(resp_obj)

    def info(self):
        """ Compatibility function for use with cookielib """
        if self.info_hm:
            return self.info_hm
        elif self.hm_list:
            return self.hm_list[-1]
        raise WGATestToolException, "Internal error in Response.info()"

    def process_curl_ret_val(self, ret_val):
        """ Did the FTP fetch fail? If so we equate that to a HTTP 404 """
        if ret_val == 19:
            self.status = 404

    def populate(self, resp_obj):
        # Set values direct from the response object here, then
        # call the transport layer specific code.
        self.uri = resp_obj.uri
        self.method = resp_obj.method
        self.protocol = resp_obj.protocol
        self.request_str = resp_obj.request_header_str
        self.populate_with_curl(resp_obj)

    def populate_with_curl(self, resp_obj):
        self.process_curl_ret_val(resp_obj.curl_ret_val)
        self.curl_exception = resp_obj.curl_exception
        self.populate_body_info(resp_obj.output_file)
        self.parse_headers(resp_obj.header_file)

    def parse_headers(self, header_file):
        """ Parse the headers.N output file from curl.

        Sometimes there are more than one HTTP Messages (one set of headers + CRLFCRLF + Body
        == One HTTP Message) due to redirection. We want to keep track of all responses,
        especially for cookie processing.

        :Parameters:
            - `header_file`: The pathname of the file to parse. If it does not exist, an empty one
              will be created.

        :Exceptions:
            - `WGATestToolError`: If curl outputs a malformed headers file (unlikely), raise this error)
        """
        # If no file exists, then make an empty one like it did exist.
        if not os.path.exists(header_file):
            os.system('touch %s' % header_file)

        reason = ''
        headers = []

        status_re = re.compile('HTTP/([0-9.]+) ([0-9][0-9][0-9]) ([a-zA-Z0-9_ \t]+)')
        headers_obj = open(header_file)

        while 1:
            status_list = status_re.findall(headers_obj.readline())
            if status_list:
                self.version, self.status, reason = status_list[0]
                self.status = int(self.status)
            else:
                if not (self.version or self.status) and \
                        self.protocol != "FTP" and \
                        not self.curl_exception:
                    raise WGATestToolError, "Header file output by curl is malformed"
                break

            # If we find a 200 Connection established message, process it and start again...
            if reason.find('Connection established') != -1:
                # TODO: Expose connect_status to be a response check. See bug 22721.
                self.connect_status = self.status
                headers_obj.readline()
                if self.protocol == 'FTP': break
                continue

            if self.protocol in ('HTTP', 'HTTPS'):
                # If we've been through once before, delete the headers already accumulated
                if headers: del headers[:]

                hm = HTTPMessage(headers_obj)
                hm.status = self.status
                for header in hm.headers:
                    # Extract header:value into (header, value)
                    header, value = tuple([s.strip() for s in header.split(':', 1)])
                    # XXX: Note the header.lower()
                    headers.append((header.lower(), value))
                self.hm_list.append(hm)

        self.headers = headers
        headers_obj.close()
        # Remove curl's header file after parsing it in
        os.unlink(header_file)

    def populate_body_info(self, body_file):
        """ Parse the body.N files created by curl into the relevant Response attributes. (body text, body size, body MD5)

        :Parameters:
            - `body_file`: The pathname of the file to be parsed.
        """
        # If no file exists, then make an empty one like it did exist.
        if not os.path.exists(body_file):
            os.system('touch %s' % body_file)

        with open(body_file) as body_file_obj:
            self.body = body_file_obj.read()
        self.body_size = len(self.body)
        self.body_md5 = md5.new(self.body).hexdigest()
        # Remove curl's body file after reading it in.
        os.unlink(body_file)

    def expand(self):
        if len(self.hm_list) == 1:
            return [self]
        else:
            resp_list = []
            for hm in self.hm_list:
                if self.headers: del self.headers[:]
                for header in hm.headers:
                    # Extract header:value into (header, value)
                    header, value = tuple([s.strip() for s in header.split(':', 1)])
                    # XXX: Note the header.lower()
                    self.headers.append((header.lower(), value))
                new_resp = copy.deepcopy(self)
                new_resp.status = hm.status
                resp_list.append(new_resp)
            return resp_list

    def __str__(self):
        ret_val = ''
        if self.status != None: ret_val += 'STATUS: %s\n' % self.status
        if self.body_size != None: ret_val += 'BODY SIZE: %s\n' % self.body_size
        if self.body_md5: ret_val += 'BODY MD5: %s\n' % self.body_md5
        if self.body_match: ret_val += 'BODY MATCH TYPE: %s,\nBODY MATCH: %s\n' % (
        self.body_match.get_check_type(), self.body_match)
        if self.version: ret_val += 'HTTP VERSION: %s\n' % self.version
        if self.headers: ret_val += 'HTTP HEADERS:\n%s' % self._get_header_str()
        if self.required_headers: ret_val += 'REQUIRED HTTP HEADERS:\n\t%s\n' % ',\n\t'.join(self.required_headers)
        if self.forbidden_headers: ret_val += 'FORBIDDEN HTTP HEADERS:\n\t%s\n' % ',\n\t'.join(self.forbidden_headers)
        return ret_val

    __repr__ = __str__

    def _get_header_str(self):
        ret_val = ''
        for header, value in self.headers:
            ret_val += '\t%s: %s\n' % (header, value)
        return ret_val

    def _has_header(self, name):
        for header, value in self.headers:
            if header == name: return True
        return False

    def __mul__(self, int_num):
        assert type(int_num) == type(123)

        resp_list = [self]
        for i in range(int_num - 1):
            resp_list.append(copy.deepcopy(self))
        return resp_list

    def __add__(self, other):
        """ When two responses are combined, but the RHS's attributes override
        the LHS (or global) attributes."""
        if self.actual_data or other.actual_data:
            raise WGATestToolException, "Internal WGA Test Tool Error in Response.__add__. If you see this please log a bug via bugzilla."
        new_res = copy.deepcopy(self)
        new_res.status = _or(other.status, self.status)
        new_res.version = _or(other.version, self.version)
        new_res.body_size = _or(other.body_size, self.body_size)
        new_res.body_md5 = _or(other.body_md5, self.body_md5)
        new_res.body_match = _or(other.body_match, self.body_match)
        new_headers = []
        for header, value in self.headers:
            if not other._has_header(header):
                new_headers.append((header, value))
        new_headers.extend(other.headers)
        new_res.headers = new_headers

        new_res.required_headers = self.required_headers.difference(other.forbidden_headers).union(
            other.required_headers)
        new_res.forbidden_headers = self.forbidden_headers.difference(other.required_headers).union(
            other.forbidden_headers)

        return new_res
