#!/usr/bin/env python
""" clictorbase.py
This module contains classes and functions for interacting with and
extracting data from the Ironport MGA CLI. The easiest way to start
using this module is to write the following code:

    import clictorbase
    class MyConfigurator(clictorbase.IafCliConfiguratorBase):
        ... Define Functions to control a specific CLI command here ...

    if __name__=='__main__':
        sess = clictorbase.get_sess()
        mc = MyConfigurator(sess)
        # ... Call MyConfigurator functions here ... #

More examples are available in this directory: libipt/phoebe46/cli/ctor
"""

from sal.exceptions import ConfigError
from sal.exceptions import TimeoutError
import os
import re
import types
import time
from sal.containers import odict
from common.logging import Logger
import sal.net.sshlib
import sal.containers.yesnodefault as yesnodefault
import sal.multiprompt as multiprompt
from sal.deprecated import expect

__all__ = ['REQUIRED', 'NO_DEFAULT', 'DEFAULT', 'get_sess',
           'IafCliConfiguratorBase', 'IafCliParamMap',
           'IafCliCtorNotImplementedError', 'ctor_logfile']

default_timeout = 10
ctor_logfile = '%s/tmp/ctor.log' % os.environ['SARF_HOME']
debug = True

RegexObject = type(re.compile(''))
REQUIRED = None  # Must specify a value for this parameter
NO_DEFAULT = None  # Must specify value for this parm  if CLI question is asked.
DEFAULT = ''  # Default value to param provided. No need to specify a value


# General IronPort MGA CLI exceptions
class IafCliError(Exception): pass


class IafCliValueError(IafCliError): pass


class IafIpHostnameError(IafCliValueError): pass


class IafEmailAddrError(IafCliValueError): pass


class IafUrlError(IafCliValueError): pass


class IafPasswordError(IafCliValueError): pass


class IafUnknownOptionError(IafCliError): pass


class IafUnknownCommandError(IafCliError): pass


class IafCliTraceback(IafCliError): pass


class IafIncorrectAccessGroupError(IafCliError): pass


class IafCliCtorNotImplementedError(Exception): pass


class DuplicateEntry(IafCliError): pass


class UnknownOptionError(IafCliError): pass


def get_sess(host=None, dev_mode=False):
    """ Return: sal.net.sshlib.SSHExpect object
    - Login to the DUT specified in either .iaf2rc.
    - Set the tty mode to NOT paginate output
    - Log all CLI interaction to a hard coded location: "ctor_logfile" """
    if not host:
        from iafframework import iafcfg
        iafcfg.init_cfg()
        host = iafcfg.get_cfg().dut.hostname

    name = 'admin'
    password = 'ironport'
    log_file = open('%s/tmp/clictorbase.log' % os.environ['SARF_HOME'], 'w', 0)
    sess = sal.net.sshlib.get_ssh(host, name, password, logfile=log_file,
                                  devmode=dev_mode)

    sess.set_prompt(multiprompt.MultiPrompt(host))
    sess.wait_for_prompt(timeout=timeout)
    sess.writeln('setttymode 0 1')
    sess.wait_for_prompt(timeout=timeout)
    return sess


def set_ignore_unanswered_questions(ignore=True):
    IafCliConfiguratorBase.ignore_unanswered_questions = ignore


class IafCliConfiguratorBase(object, Logger):
    # Class variable is needed here because we do not
    # pass state down from one configurator class to another.
    ignore_unanswered_questions = False

    def __init__(self, sess):
        self._sess = sess
        self._hostname = None
        self._model = None  # model name must be lowercase!

        self._sub_prompt = re.compile('\[(.*)]> ')
        self._sub_prompt_user_match = expect.RegexUserMatch('\[(.*)]> ')
        self._input_list_obj = IafCliInputListObject(self._sess)

        self._last_default = ''
        self._local_err_dict = None
        self._global_err_dict = {
            ('You must enter a', expect.EXACT): IafCliValueError,
            ('The value cannot', expect.EXACT): IafCliValueError,
            ('The value should', expect.EXACT): IafCliValueError,
            ('The value must', expect.EXACT): IafCliValueError,
            ('The value may', expect.EXACT): IafCliValueError,
            ('That value must', expect.EXACT): IafCliValueError,
            ('That value is not valid', expect.EXACT): IafCliValueError,
            ('Not a valid ', expect.EXACT): IafCliValueError,
            ('Value must be ', expect.EXACT): IafCliValueError,
            ('Must be a ', expect.EXACT): IafCliValueError,
            ('Must be at ', expect.EXACT): IafCliValueError,
            ('Must be an ', expect.EXACT): IafCliValueError,
            ('Please answer ', expect.EXACT): IafCliValueError,
            ('Valid characters are', expect.EXACT): IafCliValueError,
            ('The IP address ".+" is already configured', expect.REGEX)
            : IafIpHostnameError,
            ('The IP address must be 4 numbers ', expect.EXACT)
            : IafIpHostnameError,
            ('The IP cannot start with 127 or 0', expect.EXACT)
            : IafIpHostnameError,
            ('Invalid IP or IP range', expect.EXACT): IafIpHostnameError,
            ('A CIDR address is an IP', expect.EXACT): IafIpHostnameError,
            ('A hostname is ', expect.EXACT): IafIpHostnameError,
            ('A hostname must ', expect.EXACT): IafIpHostnameError,
            ('Invalid hostname format ', expect.EXACT): IafIpHostnameError,
            ('Unknown option', expect.EXACT): IafUnknownOptionError,
            ('An email address is a localname', expect.EXACT)
            : IafEmailAddrError,
            ('The email domain must be', expect.EXACT): IafEmailAddrError,
            ('The address must be an email', expect.EXACT): IafEmailAddrError,
            ('An http/https URL must consist', expect.EXACT): IafUrlError,
            ('The password must be', expect.EXACT): IafPasswordError,
            ('Traceback', expect.EXACT): IafCliTraceback,
            # ('Error:', expect.EXACT) : IafCliError,
            ('Unknown command:', expect.EXACT): IafUnknownCommandError,
            ('Invalid arguments when processing:', expect.EXACT): IafCliError,
            ('You are not in the correct access group to use', expect.EXACT)
            : IafIncorrectAccessGroupError,
        }

    def _set_local_err_dict(self, err_dict):
        self._local_err_dict = self._global_err_dict.copy()
        self._local_err_dict.update(err_dict)

    def _get_expectindex(self):
        """Return the index into the last list that was passed to
        self._sess.expect(). The index corresponds to the actual
        pattern in the list that was matched.  """
        return self._sess._last_expect_info.index

    _expectindex = property(_get_expectindex)

    ############################################################
    # Expose some expect methods.
    def getbuf(self):
        return self._sess.getbuf()

    def clearbuf(self):
        return self._sess.clearbuf()

    def interrupt(self):
        return self._sess.interrupt()

    def close(self):
        return self._sess.close()

    def _writeln(self, line=''):
        # if line is already a string, don't re-convert it
        # avoids UnicodeEncodeError when dealing with unicode strings
        if isinstance(line, basestring):
            self._debug('***********************Admin Entered => %s************\
                                                               \n' % line)
            return self._sess.writeln(line)
        else:
            self._debug('***********************Admin Entered => %s************\
                                                          \n' % str(line))
            return self._sess.writeln(str(line))

    def _read_until(self, patt=None, timeout=None):
        curr_err_dict = self._local_err_dict or self._global_err_dict
        return self._sess.read_until(patt=patt, timeout=timeout,
                                     err_dict=curr_err_dict)

    def _wait_for_prompt(self, timeout=60):
        curr_err_dict = self._local_err_dict or self._global_err_dict
        return self._sess.wait_for_prompt(timeout=timeout,
                                          err_dict=curr_err_dict)

    def _wait_for_prompt_line(self, timeout=30):
        curr_err_dict = self._local_err_dict or self._global_err_dict
        return self._sess.wait_for_prompt_line(timeout=timeout,
                                               err_dict=curr_err_dict)

    def _expect(self, patt, mtype=expect.EXACT, timeout=None):
        curr_err_dict = self._local_err_dict or self._global_err_dict
        return self._sess.expect(patt=patt, mtype=mtype, timeout=timeout,
                                 err_dict=curr_err_dict)

    def _peek(self, amt=1, timeout=None):
        return self._sess.peek(amt, timeout=timeout)

    def _peekline(self, timeout=None):
        return self._sess.peekline(timeout=timeout)

    def _get_sess(self):
        return self._sess

    def _get_prompt(self):
        return self._sess.prompt

    def _get_last_matched_text(self):
        return self._sess.get_last_matched_text()

    def _get_last_mo(self):
        return self._sess.get_last_mo()

    ############################################################
    # Methods to query, answer CLI questions
    def _query(self, *args, **kwargs):
        """_query is a convenience method to wrap expect.Expect.expect().
        If no patterns are passed to _query, then the CLI subprompt
        is searched for. Each CLI subprompt can contain a default
        value that is selected when just '\\n' is entered.  This value
        is fetched and can be viewed with _get_last_default().

        If patterns are passed to _query, they are processed into
        tuples for expect() and then searched for. The index of
        the pattern that matched is then returned.  """
        global default_timeout

        # set timeout
        if kwargs.has_key('timeout'):
            timeout = kwargs['timeout']
        else:
            timeout = default_timeout

        # query _sub_prompt
        if len(args) == 0:
            try:
                m = self._expect((self._sub_prompt, expect.REGEX),
                                 timeout=timeout)
                self._set_last_default(self._sub_prompt,
                                       self._get_expectindex(), m)
                return 0
            except (ConfigError, IafCliValueError, DuplicateEntry,
                    UnknownOptionError):
                self._restart_nosave()
                raise

        # build patt_list
        # XXX: The logic to create regular expressions from strings exists
        #      in the expect module. I see the convenience of not passing in
        #             tuples, but I think removing this code could be good.
        # XXX: Added an elif statement to *not* add a tuple when patt
        #      is a expect.UserMatch. This special case adds to my dislike of
        #      this masking of expect functionality.
        # XXX TODO: clean this up. mikew
        patt_list = []
        for patt in args:
            if isinstance(patt, basestring):
                patt_list.append((patt, expect.EXACT))
            elif hasattr(patt, '__class__') \
                    and issubclass(patt.__class__, expect.UserMatch):
                patt_list.append(patt)
            elif type(patt) == types.TupleType:
                patt_list.append(patt)
            elif type(patt) == type(re.compile('')):
                patt_list.append((patt, expect.REGEX))
            else:  # unknown
                patt_list.append(patt)

        # expect string/regex match  in patt_list
        try:
            m = self._expect(patt_list, timeout=timeout)
        except (ConfigError, IafCliValueError, DuplicateEntry,
                UnknownOptionError):
            self._restart_nosave()
            raise

        # XXX cleanup: confusing. because we don't always set last default
        self._set_last_default(patt_list, self._get_expectindex(), m)

        return self._get_expectindex()

    def _query_response(self, resp='', timeout=default_timeout):
        """_query_response searches for the next subprompt and sets the
        last default (see _query, above).  If the subprompt was found,
        then we write the response to the CLI.  """

        if resp == None: resp = ''
        ei = self._query(timeout=timeout)
        self._debug('************************Matched Text => %s****************\
                    *********************************************\n' % \
                    self._get_last_matched_text())
        self._writeln(str(resp))
        return ei

    ############################################################
    # START: Input List Handling
    """ selector: Is a string, integer, or regular expression.
                1a.If selector is a string, the first input list option
                   that contains selector will be chosen.
                   regardless of what the menu is.
                1b.If selector is the empty string a newline is sent
                   and -1 is returned.
                2. If selector is a regular expression, then the first input
                   list option that matches selector will be chosen.
                3. If selector is a digit, then that selection is entered,
        text_block: string containing a CLI input list.
    """

    def _query_select_list_item(self, selector, exact_match=False,
                                timeout=default_timeout):
        # Return the selected item number (an IntegerType).
        self._query(timeout=timeout)
        input_list_text_block = self._get_last_matched_text()
        self._input_list_obj.parse_text(input_list_text_block)
        idx = self._input_list_obj.select_item(selector, exact_match)
        return idx

    def _select_list_item(self, selector, text_block=None, exact_match=False):
        # Return the selected item number (an IntegerType).
        if text_block:
            self._input_list_obj.parse_text(text_block)
        idx = self._input_list_obj.select_item(selector, exact_match)
        return idx

    def _query_parse_input_list(self):
        # Method indefinitely stores Input Lists in the self._input_list_obj
        self._query()
        input_list_text_block = self._get_last_matched_text()
        self._input_list_obj.parse_text(input_list_text_block)
        return self._input_list_obj  # return input list obj for convenience

    def _parse_input_list(self, text_block):
        self._input_list_obj.parse_text(text_block)
        return self._input_list_obj  # return input list obj for convenience

    # Input List Helper Methods
    def _get_input_list_length(self):
        """Return number of rows in input list"""
        return self._input_list_obj.get_length()

    def _get_input_list_selector(self):
        """Returns unmodified selector used to select item in input list."""
        return self._input_list_obj.get_selector()

    def _get_input_list_idx(self):
        """Return item number written to CLI session when input list item
        was selected.  If Default(empty string) was selected, return -1."""
        return self._input_list_obj.get_idx()

    def _get_input_list_dict(self):
        """Return dictionary where keys is the item number and
        value is the line item string."""
        return self._input_list_obj.get_input_list_dict()

    # END: Input List Handling
    ############################################################

    def _process_input(self, param_map, do_restart=True, timeout=default_timeout):
        """_process_input takes an IafCliParamMap instance to navigate its
        way through a CLI command.  The map (see docs below) defines
        what questions to expect, what answers to give, if a question
        must be answered, and if a question has already been answered.
        Also defined is an ending_phrase to know when the command has finished.

        If there ends up being a missing question or an unexpected
        question, an error will be raised. Otherwise the command
        will be navigated and the MGA CLI session object will be put
        back to the main prompt.

        param_map: is an IafCliParamMap object
        do_restart: set to False if you want to call _process_input()
                    more than once in a single ctor call.
        """

        answer_map = param_map
        while 1:
            # Read the question (that's asked by the MGA's CLI).
            # Or match on the terminating string.
            try:
                idx = self._query(answer_map.ending_string,
                                  self._sub_prompt,
                                  timeout=timeout)
                block = self._get_last_matched_text()

            except TimeoutError:
                # need to escase timeout errors in case no
                # prompt appears(eg. multiline input prompted)
                idx = None
                block = self._sess.getbuf()

                # press any key several times to read EULA completely
                if block.endswith('-Press Any Key For More-'):
                    self._writeln()
                    continue

            question_text = re.sub('[\r\n]+', ' ', block, re.MULTILINE)

            # found terminating string
            if idx == 0:
                unanswered = answer_map.get_missing_questions()
                if unanswered and \
                        not IafCliConfiguratorBase.ignore_unanswered_questions:
                    self._restart_nosave()
                    raise ConfigError, 'Unanswered questions:%s' % unanswered

                if do_restart:
                    self._restart()
                return

            # select the answer object to use to answer the question
            key = self._find_answer_key(question_text, answer_map)
            answer_obj = answer_map[key]

            answer_str = answer_map._get_answer_str(key)
            if debug:
                self._print_debug(question_text, key, answer_str)

            # answer the question
            if answer_obj['is_input_list']:
                try:
                    self._select_list_item(answer_str, block)
                except (ConfigError, IafCliValueError, DuplicateEntry,
                        UnknownOptionError):
                    self._restart_nosave()
                    raise
            else:
                self._writeln(answer_str)

            # markup answer_map to indicate this answer obj has been used up
            answer_obj['answer_qty'] += 1

    def _find_answer_key(self, question_text, answer_map):
        """Select the answer object from the list of potential
        answer objects stored in the answer_map. This answer
        object will be used to answer the question specified
        in question_text."""
        for answer_key in answer_map.keys():
            # find text_string in 'question_text'
            text_string = answer_map[answer_key]['text_string']
            found = (isinstance(text_string, RegexObject) and \
                     text_string.search(question_text)) \
                    or \
                    (isinstance(text_string, basestring) and \
                     question_text.find(text_string) >= 0)

            if found and not answer_map.has_been_answered(answer_key):
                return answer_key
        else:
            raise ConfigError, "Unrecognized question: %r" % (question_text,)

    def _print_debug(self, question_text, answer_key, answer_text):
        val1 = str(question_text)[:20]
        val2 = str(answer_key)[:20]
        val3 = str(answer_text)[:20]
        if len(str(question_text)) > 20: val1 += '..'
        if len(str(answer_key)) > 20: val2 += '..'
        if len(str(answer_text)) > 20: val3 += '..'
        print '  <<<<%-22s|%-22s|%-22s>>>>' % (val1, val2, val3)

    ############################################################
    # Methods to access default prompt values
    def _get_last_default(self):
        return self._last_default

    def _set_last_default(self, patt_list, expect_index, expect_match):
        """ If the last pattern to be matched was the _sub_prompt,
        then set the last default.  Otherwise, do nothing.  """
        assert expect_match
        if patt_list is [] or patt_list is ():
            patt = patt_list[expect_index]
        else:
            patt = patt_list
        if patt == self._sub_prompt:
            self._last_default = expect_match.group(1)

    def _is_last_default_yes(self):
        if self._last_default.lower().find('y') == 0:
            return True
        else:
            return False

    ############################################################
    # Methods to exit a CLI command
    # XXX this needs some clean-up
    def _restart(self, waittime=2):
        """restart(): Return to top-level prompt while attempting to
        save any data that has been changed in the current command.
        Also be attentive to the number of ^Cs that are printed to the
        screen to not clog log files. """
        cr_tries = 0
        timeout_waittime = 2
        max_tries = 24
        try:
            self._query(self._get_prompt(), timeout=waittime)
        except TimeoutError:
            while 1:
                if cr_tries == max_tries:
                    raise ConfigError, "Entering Many CRLFs " \
                                       "and interrupts (^C) have failed to " \
                                       "get the CLI session back to the main prompt."
                self._sess.send("\r")
                try:
                    mo = self._expect(["-- Changes not", self._sess.prompt],
                                      timeout=timeout_waittime)
                    if mo:
                        if self._get_expectindex() == 0:
                            try:
                                # eat remainder of line
                                self._wait_for_prompt(2)
                            except TimeoutError:
                                pass  # will raise exception anyway...
                            raise ConfigError, "Something wedged, " \
                                               "changes not recorded. check the logfile."
                        else:  # got prompt
                            break
                except TimeoutError:
                    cr_tries += 1
                    if cr_tries >= 10:
                        # if we can't get a prompt after lots of enters,
                        # try interrupt and Enter again.
                        self.interrupt()

                    # Increase delay as the amount of attempts to exit increase
                    if cr_tries == 10:
                        timeout_waittime = 5
                    if cr_tries == 18:
                        timeout_waittime = 10

    def _restart_nosave(self, waittime=2):
        """_restart(): Return to the top-level prompt without caring
        if there are any:
            "-- Changes not recorded" or other errors
        from the CLI."""
        dummy = 0
        for dummy in range(10):
            try:
                # Call the session's wait_for_prompt directly to ignore
                # any err_dicts. This also avoids changing the
                # _wait_for_prompt function signature.
                self._sess.wait_for_prompt(timeout=waittime,
                                           err_dict={})
                return
            except TimeoutError:
                self.interrupt()
        else:
            raise ConfigError, 'restart failed'

    def _to_the_top(self, newlines, timeout=default_timeout):
        global debug
        text = ''
        if debug:
            print 'self._to_the_top(%d)' % newlines

        if newlines == 0:
            text = self._wait_for_prompt(timeout)
            return text

        for i in range(newlines - 1):
            self._writeln()
            self._query(timeout=timeout)
            text += self._get_last_matched_text()
        else:
            self._writeln()
            text += self._wait_for_prompt(timeout)

        return text

    ############################################################
    # Miscellaneous methods
    def set_model(self, model):
        self._model = str(model).lower()

    def get_model(self):
        return self._model.lower()

    def get_hostname(self):
        return self._hostname

    def set_hostname(self, hostname):
        self._hostname = hostname

    def _check_feature(self, feature_name):
        return _check_feature(self, feature_name)


class IafCliParamMap:
    """ IafCliParamMap keeps track of Expected questions and the answers
    to be entered to those questions for a particular CLI command.
    For each question, there are 5 attributes:

    - A substring of the expected question that is unique (enough)
    - The answer that should be entered when the question is encountered
    - A boolean stating whether or not the question is an input list
    - A boolean stating whether the question must be answered
    - A counter stating the number of times the question has been answered """

    def __init__(self, end_of_command=None):
        self._map = odict.odict()
        self.ending_string = end_of_command

    def __setitem__(self, param_name, value_list):
        value_dict = dict()
        value_dict['text_string'] = value_list[0]
        value_dict['answer'] = value_list[1]
        value_dict['is_input_list'] = 0
        if len(value_list) == 3:
            value_dict['is_input_list'] = value_list[2]
        value_dict['must_answer'] = 0
        value_dict['answer_qty'] = 0

        # convert integers, longs, and floats to string
        ans_type = type(value_dict['answer'])
        assert ans_type in (types.ListType,
                            types.IntType, types.LongType, types.FloatType,
                            type(yesnodefault.YesNoDefault()),
                            types.NoneType, types.StringType, types.UnicodeType), \
            'unexpected data type'
        if ans_type == types.ListType:
            value_dict['answer'] = map(lambda v: str(v), value_dict['answer'])
        elif ans_type in (types.IntType, types.LongType, types.FloatType,
                          type(yesnodefault.YesNoDefault())):
            value_dict['answer'] = str(value_dict['answer'])
        else:  # is NoneType or basestring type
            value_dict['answer'] = value_dict['answer']

        self._map[param_name] = value_dict

    def __getitem__(self, param_name):
        return self._map[param_name]

    def keys(self):
        return self._map.keys()

    def set_ending_string(self, end_of_command):
        self.ending_string = end_of_command

    def _get_answer_str(self, param_name):
        """self._map[paramname]['answer'] can be string or list or strings.
        If list, then return 0th element otherwise return string.
        """
        assert self._map[param_name]['answer'] != None

        answer = self._map[param_name]['answer']
        if isinstance(answer, types.ListType):
            if self._map[param_name]['answer_qty'] >= len(answer):
                # error: seen this question more times than expected
                raise ConfigError, 'Cannot answer question. No answers left.'
            return answer[self._map[param_name]['answer_qty']]
        elif isinstance(answer, basestring):
            return answer
        # should never reach this line
        assert False, "No 'answer' in parameter map. Has type:%s" % type(answer)

    def set_must_answer(self, param_name):
        self._map[param_name]['must_answer'] = 1

    def get_missing_questions(self):
        q_list = []
        for key in self._map.keys():
            if self._map[key]['must_answer'] \
                    and not self.has_been_answered(key):
                q_list.append(key)
        return q_list

    def update(self, input_dict):
        for key in input_dict.keys():
            # convert integers, longs, and floats to string
            ans_type = type(input_dict[key])
            assert ans_type in (types.ListType,
                                types.IntType, types.LongType, types.FloatType,
                                type(yesnodefault.YesNoDefault()),
                                types.NoneType, types.StringType, types.UnicodeType), \
                'unexpected data type'
            if ans_type == types.ListType:
                self._map[key]['answer'] = map(lambda v: str(v), input_dict[key])
            elif ans_type in (types.IntType, types.LongType, types.FloatType,
                              type(yesnodefault.YesNoDefault())):
                self._map[key]['answer'] = str(input_dict[key])
            else:  # is NoneType or basestring type
                self._map[key]['answer'] = input_dict[key]

            self.set_must_answer(key)

    def has_been_answered(self, param_name):
        answer = self._map[param_name]['answer']
        if isinstance(answer, types.ListType):
            return bool(len(answer) == self._map[param_name]['answer_qty'])
        else:
            return bool(self._map[param_name]['answer_qty'])


############################################################
# START: Input List Handling
class IafCliInputListObject:
    def __init__(self, sess):
        self._sess = sess
        # Ordered dictionary containing items in a CLI Input-List
        self._input_list_dict = None

        # set _selector and _idx at the time input list item is selected
        self._selector = ''
        self._idx = None
        self._text_block = ''

    ## Getters
    def get_length(self):
        """Return number of rows in input list"""
        return len(self._input_list_dict)

    def get_selector(self):
        """Returns unmodified selector used to select item in input list."""
        return self._selector

    def get_idx(self):
        """Return item number written to CLI session when input list item
        was selected.  If Default(empty string) was selected, return -1."""
        return self._idx

    def get_input_list_dict(self):
        return self._input_list_dict

    ## Sess (encapsulate/wrap sess calls)
    def _writeln(self, line=''):
        return self._sess.writeln(line)

    ## Parse
    def parse_text(self, text_block):
        """Take String representing an Ironport MGA CLI input list like this:
            Currently configured listeners:
            1. allqa (on data1, 172.21.41.1) SMTP TCP Port 25 Private
            2. private_qmqp (on data1, 172.21.41.1) QMQP TCP Port 628 Private
            3. public_smtp (on data2, 172.22.41.1) SMTP TCP Port 25 Public
        and return an ordered dictionary that looks like:
        {'1':'allqa (on data1, 172.21.41.1) SMTP TCP Port 25 Private',
         '2':'private_qmqp (on data1, 172.21.41.1) QMQP TCP Port 628 Private',
         '3':'public_smtp (on data2, 172.22.41.1) SMTP TCP Port 25 Public'}

        Also can parse "input lists" that aren't really input lists, like
        those used for aliasconfig and quarantineconfig.
        """
        self._text_block = text_block  # store text_block for debugging

        input_list_dict = odict.odict()
        for line in text_block.split('\n'):
            line = line.strip()
            # first look for a standard input list
            m = re.search('^(\d+)\. (.*)', line)
            if m == None:
                # aliasconfig-style "input list"
                m = re.search('^(\d+)\) (.*)', line)
                if m == None:
                    # quarantineconfig-style "input list"
                    m = re.search('^\s?(\d+)  (.*)', line)
                    if m == None:
                        continue
            idx, desc = m.group(1), m.group(2)
            input_list_dict[idx] = desc

        self._input_list_dict = input_list_dict
        return self._input_list_dict

    ## Select
    def select_item(self, selector, exact_match=False):
        """Use 'selector' to determine which item in the
        _input_list_dict to select.
        selector: Can be a string, a digit, or a regular expression.
                1. If selector is a string, the first input list option
                   that contains selector will be chosen.
                   regardless of what the menu is.
                2. If selector is a regular expression, then the first input
                   list option that matches selector will be chosen.
                3. If selector is a digit, then that selection is entered,
                4. If selector is the empty string a newline is sent.
        """

        self._selector = selector  # save selector in this object's attribute

        # search input_list_dict for selector
        for idx, desc in self._input_list_dict.items():
            if type(selector) == types.IntType or selector.isdigit():
                self._idx = int(selector)
                self._writeln(str(selector))
                return self._idx
            elif selector == '' or selector == None:  # select default
                self._idx = -1  # SPECIAL CASE!
                self._writeln()
                return self._idx  # Note: returns -1!!
            elif isinstance(selector, basestring):
                if not exact_match:  # ignore case
                    desc = desc.lower()
                    selector = selector.lower()
                if desc.find(selector) >= 0:
                    self._idx = int(idx)
                    self._writeln(str(idx))
                    return self._idx
            else:  # assume regex
                regex_flag = None
                if not exact_match:  # ignore case
                    regex_flag = re.IGNORECASE
                if re.search(selector, desc, regex_flag):
                    self._idx = int(idx)
                    self._writeln(str(idx))
                    return self._idx
        else:
            err = self._get_input_list_error_string(selector)
            raise ConfigError, err

    ## Error
    def _get_input_list_error_string(self, selector):
        """This is a helper function to print out an input list along
        with the selector that did not match any of the selections to
        choose from.  """
        s = []
        s.append('')
        s.append('+-------------')
        s.append('|INPUT LIST')
        s.append('+-------------')
        for k, v in self._input_list_dict.items():
            s.append('|%2s. %s' % (k, v))
        s.append('+-------------')
        s.append('| Not found: ' + str(selector))
        s.append('+-------------')
        return '\n'.join(s)


# END: Input List Handling
############################################################

def check_feature(self, feature_name):
    return True
