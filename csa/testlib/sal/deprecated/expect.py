#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/sal/deprecated/expect.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
This module contains classes and functions that perform Expect-like operations
on file objects. It is a general and object oriented approach to interacting
with files and processes. Use this in concert with the proctools module for
interacting with processes.

Notes from the IAF refactoring project (05/26/09): this module will be replaced
 with pexpect eventually. Deprecated.
"""
from __future__ import absolute_import

#: Reference Symbols: expect

from sal.exceptions import TimeoutError, ExpectError
import sys, os
import re
from errno import EINTR

import time
from sal.containers import RingBuffer

import signal
import select

import sal.deprecated.thirdparty.termtools as termtools

# matching types
EXACT = 1  # string match (fastest)
GLOB = 2  # POSIX shell style match, but really uses regular expressions
REGEX = 3  # slow but powerful RE match
USER = 4  # any subclass of UserMatch

def_enable_ring_buffering = True
debug = False


# Expect convenience class to store info generated from a call to expect()
class ExpectInfo:
    def __init__(self, index, mo, text):
        self.index = index
        self.mo = mo
        self.matched_text = text

    def set_index(self, index):
        self.index = index

    def set_mo(self, mo):
        del self.mo
        self.mo = mo

    def set_text(self, text):
        self.matched_text = text

    def update(self, index, mo, text):
        self.set_index(index)
        self.set_mo(mo)
        self.set_text(text)


class UserMatch:
    def get_match_object(self, mtype=None, callback=None):
        raise NotImplementedError

    def search(self, text, pos=0, endpos=2147483647):
        raise NotImplementedError

    def get_pattern(self):
        raise NotImplementedError


class RegexUserMatch(UserMatch):
    """ This class allows us to the do equivalent of:
        >>> self._sess.set_prompt(re.compile(some_regex))
        >>> self._sess.wait_for_prompt()

    For expect.Expect.wait_for_prompt() to match on a regular expression
    (instead of a string) we must create a UserMatch derived class.
    """

    def __init__(self, patt):
        self.patt = patt
        self.mo = None  # re.MatchObject

    def search(self, text, pos=0, endpos=2147483647):
        self.mo = re.search(self.patt, text[pos:endpos])
        return self.mo

    def get_match_object(self, mtype=None, callback=None):
        """Stub.  UserMatch requires get_match_object() to be defined."""
        return (self, callback)

    def matchlen(self):
        if not self.mo:
            return 0
        return self.mo.end() - self.mo.start()

    def get_pattern(self):
        return self.patt


class StringMatchObject:
    """ String "MatchObject" objects implement a subset of re.MatchObject objects.
        This allows for a more consistent interface for the match types.  Since
        string.find is about 10 times faster than an RE search with a plain string,
        this should speed up expect matches in that case by about that much, while at
        the same time keeping a consistent interface.
    """

    def __init__(self, start, end, string, pos, endpos):
        self._start = start
        self._end = end
        self.string = string
        self.pos = pos
        self.endpos = endpos
        self.lastgroup = None
        self.lastindex = None

    def get_pattern(self):
        return self.string

    def expand(self, template):
        raise NotImplementedError

    def group(self, *args):
        raise NotImplementedError

    def groups(self, default=None):
        raise NotImplementedError

    def groupdict(self, default=None):
        raise NotImplementedError

    def start(self, group=None):
        return self._start

    def end(self, group=None):
        return self._end

    def span(self, group=None):
        return self._start, self._end

    def __nonzero__(self):
        return 1


class StringExpression:
    """ an object that looks like a compiled regular expression, but does exact
    string matching. should be much faster in that case.
    """

    def __init__(self, patt):
        self.pattern = patt
        # bogus attributes to simulate compiled REs from re module.
        self.flags = 0
        self.groupindex = {}

    def get_pattern(self):
        return self.pattern

    def search(self, text, pos=0, endpos=2147483647):
        n = text.find(self.pattern, pos, endpos)
        if n >= 0:
            return StringMatchObject(n, n + len(self.pattern), text, pos, endpos)
        else:
            return None

    match = search  # match is same as search for strings

    def split(self, text, maxsplit=0):
        return text.split(self.pattern, maxsplit)

    def findall(self, string):
        raise NotImplementedError

    def finditer(self, string):
        raise NotImplementedError

    def sub(self, repl, string, count=0):
        raise NotImplementedError

    def subn(self, repl, string, count=0):
        raise NotImplementedError


def compile_exact(string):
    """ factory function to "compile" EXACT patterns (which are strings) """
    return StringExpression(string)


# swiped from the fnmatch module for efficiency
def glob_translate(pat):
    """Translate a shell (glob style) pattern to a regular expression.
    There is no way to quote meta-characters.
    """
    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + "$"


class Expect:
    """Expect wraps a file-like object and provides enhanced read, write,
    readline, send, and expect methods. This is very useful when combined with
    proctool objects running interactive programs (A Process object is a
    file-like object as well).
    """

    def __init__(self, fo, prompt="$", timeout=90, logfile=None,
                 enable_ring_buffering=None):
        global def_enable_ring_buffering

        if hasattr(fo, "fileno"):
            self._fo = fo
            if hasattr(self._fo, "restart"):
                # for Process objects. This needs to catch EINTR for timeouts.
                self._fo.restart(0)
        else:
            raise ValueError, \
                "Expect: first parameter not a file descriptor or file object."

        self.default_timeout = timeout
        self._log = logfile
        self.cmd_interp = None
        self.prompt = prompt
        self._patt_cache = {}

        if enable_ring_buffering == None:
            self._enable_ring_buffering = def_enable_ring_buffering

        else:
            self._enable_ring_buffering = enable_ring_buffering

        if self._enable_ring_buffering:
            self._max_ring_buf_size = 10000  # size of list
            self._ring_buf = RingBuffer(self._max_ring_buf_size)

        self._extra = ''  # buffer for extra data to make read_until more efficient
        self.eof = 0
        self.expectindex = -1  # Maintain for backwards compatibility
        self._last_expect_info = ExpectInfo(self.expectindex, mo=None, text='')

        # functions that need decorations with file object validation
        self.read = self.__add_fo_validation(self.read)
        self.write = self.__add_fo_validation(self.write)
        self.fileno = self.__add_fo_validation(self.fileno)
        self.interrupt = self.__add_fo_validation(self.interrupt)
        self.interrupt_writeln = self.__add_fo_validation(self.interrupt_writeln)
        self.interact = self.__add_fo_validation(self.interact)
        self.isatty = self.__add_fo_validation(self.isatty)
        self.ttyname = self.__add_fo_validation(self.ttyname)
        self.tcgetpgrp = self.__add_fo_validation(self.tcgetpgrp)
        self.fstat = self.__add_fo_validation(self.fstat)
        self.seek = self.__add_fo_validation(self.seek)
        self.rewind = self.__add_fo_validation(self.rewind)
        self.sendfileobject = self.__add_fo_validation(self.sendfileobject)

    def __add_fo_validation(self, func):
        """Function decorator that adds file object presence validation.

        :Parameters:
            -`func`: function, that needs to be decorated

        :Exceptions:
            -`IOError`: is raised, when file object is NoneType

        :Return:
            Reference to a decorated function
        """

        def decorated(*args, **kwarg):
            if self._fo is None:
                raise IOError('File object _fo does not exist')

            return func(*args, **kwarg)

        return decorated

    def fileobject(self):
        return self._fo

    def fileno(self):
        return self._fo.fileno()

    def openlog(self, fname):
        try:
            self._log = open(fname, "w")
        except:
            self._log = None
            raise

    def close(self):
        """If self._fo is None can assume file object has been closed. """
        if self._fo != None:
            rv = self._fo.close()
            self._fo = None
            return rv

    def interrupt(self):
        """interrupt() sends the INTR character to the stream.

           DO NOT USE WITH MGA TESTS.  Use interrupt_writeln() instead.
        """
        global debug
        try:
            if debug:
                print '{sending interrupt}'
            self._fo.interrupt()
            self.writeln('')
        except AttributeError:
            pass

    def interrupt_writeln(self):
        """Sends the INTR character to the stream and adds a LF afterwards."""
        global debug
        try:
            if debug:
                print '{sending interrupt}'
            self._fo.interrupt()
            self.writeln('')
        except AttributeError:
            pass

    def closelog(self):
        if self._log:
            self._log.close()
            self._log = None

    def flushlog(self):
        if self._log:
            self._log.flush()

    def setlog(self, fo):
        if hasattr(fo, "write"):
            self._log = fo

    def getlog(self):
        return self._log

    def getbuf(self, clear_buf=False):
        """Returns contents of ring buffer as a string.  If clear_buf
        is True _ring_buf is emptied on each getbuf() call and a new
        empty _ring_buf is created.
        """
        if not self._enable_ring_buffering:
            return ''
        data = ''.join(self._ring_buf.get())
        if clear_buf:
            self._ring_buf = RingBuffer(self._max_ring_buf_size)
        return data

    def clearbuf(self):
        """Clears the contents of ring buffer.  """
        if not self._enable_ring_buffering:
            return ''
        del self._ring_buf
        self._ring_buf = RingBuffer(self._max_ring_buf_size)

    def delay(self, delay_len):
        time.sleep(delay_len)

    sleep = delay

    def wait_for_prompt_line(self, timeout=None, err_dict=None):
        """ wait_for_prompt_line(timeout, err_dict) --> (out) """

        out = ""
        patt = [('\n', EXACT), self.prompt]

        # preserve expect index
        old_index = self.expectindex

        while 1:
            mo = self.expect(patt=patt, timeout=timeout, err_dict=err_dict)
            out += self.get_last_matched_text()
            if self.expectindex == 1:
                break

        # reset expectindex to old value
        self.expectindex = old_index
        self._last_expect_info.set_index(self.expectindex)
        return out

    def wait_for_prompt(self, timeout=None, err_dict=None, read_by_line=False):
        """ Read from the connection until the next prompt is found, and return
            all text read upto that prompt. read_by_line enables a faster but
            more limited line processing algorithm to be used.
        """
        if read_by_line:
            return self.wait_for_prompt_line(timeout, err_dict)

        patt = self.prompt
        if not issubclass(patt.__class__, UserMatch):
            return self.read_until(patt, timeout=timeout, err_dict=err_dict)
        self.expect(patt=patt, timeout=timeout, err_dict=err_dict, \
                    preserve_index=True)
        return self.get_last_matched_text()

    # Prompt Functions
    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_prompt(self):
        return self.prompt

    # Attribute GET functions
    def get_last_matched_text(self):
        return self._last_expect_info.matched_text

    def get_last_mo(self):
        return self._last_expect_info.mo

    def _get_re(self, patt, mtype=EXACT, callback=None):
        try:
            return self._patt_cache[patt]
        except KeyError:
            if mtype == EXACT:
                self._patt_cache[patt] = p = (compile_exact(patt), callback)
                return p
            elif mtype == GLOB:
                self._patt_cache[patt] = p = (re.compile(glob_translate(patt)), \
                                              callback)
                return p
            elif mtype == REGEX:
                self._patt_cache[patt] = p = (re.compile(patt), callback)
                return p

    def _get_search_list_user(self, patt, solist=None):
        if solist is None:
            solist = []
        solist.append(patt.get_match_object(None, None))
        return solist

    def _get_search_list(self, patt, mtype, callback, solist=None):
        if solist is None:
            solist = []
        ptype = type(patt)
        if issubclass(patt.__class__, UserMatch):
            solist.append(patt.get_match_object(mtype, callback))
        elif ptype is str:
            solist.append(self._get_re(patt, mtype, callback))
        elif ptype is tuple:
            solist.append(apply(self._get_re, patt))
        elif ptype is list:
            map(lambda p: self._get_search_list(p, mtype, callback, solist), patt)
        elif patt is None:
            return self._patt_cache.values()
        return solist

    def expect(self, patt, mtype=EXACT, callback=None,
               timeout=None, err_dict=None, preserve_index=False):
        """ The expect method supports a very flexible calling signature. thus, the
        convoluted type checking, etc.  You may call with a string (defaults to
        exact string match), or you may supply the match type as a second
        parameter. Or supply the pattern as a tuple, with string and match type.
        Or, a list of tuples or strings as just described. An optional callback
        method and timeout value may also be supplied. The callback will be
        called when a match is found, with a match-object as a parameter.

        preserve_index is an extra parameter that controls whether self.expectindex and
        self._last_expect_info.index are set. Changes have been made to write other methods
        in this class using expect(). This has had the side effect of setting the variables
        mentioned in cases people did not plan on before. Thus, to keep backwards compatibility,
        those calls can now preserve the index and test writer's sanity.
        """
        if not timeout:
            timeout = 60
        solist = self._get_search_list(patt, mtype, callback)

        # If there is an error dict, add all of the patterns defined there into
        # the search object list.
        if err_dict:
            orig_patt_len = len(solist)
            err_range = range(orig_patt_len, orig_patt_len + len(err_dict))
            solist.extend(self._get_search_list(err_dict.keys(), mtype, callback))

        buf = ""
        st = time.time()
        while 1:
            # If an error occurs here, then set the expectindex back to -1
            # for backwards compatibility. I'm not sure if this is needed, but
            # it is what IAF 1.0 expect.py did.
            try:
                c = self.read(1, timeout)

            except TimeoutError:
                buf = buf or "None - buffer is empty"
                self.expectindex = -1
                raise TimeoutError, 'Timed out during read.\n' + \
                                    'Read buffer contents at timeout:\n"%s"' % buf

            except Exception:
                buf = buf or "None - buffer is empty"
                self.expectindex = -1
                print 'Error encountered during expect.'
                print 'Read buffer contents at error:\n"%s"' % buf
                raise

            if not c:
                self.expectindex = -1
                raise ExpectError, 'EOF during expect.'

            buf += c
            i = -1
            for so, cb in solist:
                mo = so.search(buf)
                if mo:
                    # If we matched an error, then find the (string, mtype) tuple to
                    # match the exception to raise.
                    if err_dict and (i + 1 in err_range):
                        matched_err = err_dict.keys()[(i - orig_patt_len) + 1]
                        raise err_dict[matched_err], buf

                    # save the list index of the match object
                    if not preserve_index:
                        self.expectindex = i + 1

                    self._last_expect_info.update(self.expectindex, mo, buf)
                    # If a callback is defined, call it
                    if cb:
                        cb(mo)
                    return mo
                i += 1

    def expect_exact(self, patt, callback=None, timeout=None):
        return self.expect(patt, EXACT, callback, timeout)

    def expect_glob(self, patt, callback=None, timeout=None):
        return self.expect(patt, GLOB, callback, timeout)

    def expect_regex(self, patt, callback=None, timeout=None):
        return self.expect(patt, REGEX, callback, timeout)

    def read(self, amt=2147483646, timeout=None):
        """ Just like any file-like object, read() will try to read as much
            as you tell it to, and will time out if it can't. The data that
            is read in is returned if no timeout occurs.
        """

        # enable alarm
        self._timed_out = 0
        if timeout == None:
            timeout = self.default_timeout

        signal.signal(signal.SIGALRM, self._timeout_cb)
        signal.alarm(int(round(timeout)))

        try:
            while 1:
                try:
                    data = self._fo.read(amt, timeout + 1)
                    break
                except EOFError:
                    return ""
                except OSError, val:
                    if val[0] == EINTR and self._timed_out == 1:
                        raise TimeoutError, "timed out during read."
                    elif val[0] == EINTR:
                        continue
                    else:
                        raise
                assert False, 'should never reach this line'
        finally:
            signal.alarm(0)  # disable alarm

        if self._log:
            self._log.write(data)
        if self._enable_ring_buffering:
            self._ring_buf.append(data)
        return data

    def _timeout_cb(self, signum, frame):
        signum = frame = None  # args not used
        self._timed_out = 1

    def read_until(self, patt=None, timeout=None, err_dict=None):
        """ Read until a given pattern is found in the stream. """
        if patt is None:
            patt = self.prompt
        self.expect(patt=patt, timeout=timeout, err_dict=err_dict, \
                    preserve_index=True)
        mo = self.get_last_mo()

        # Sometimes, users can define search objects that return strings
        # instead match objects.
        # if type(mo) == type(''):
        if isinstance(mo, (str, unicode)):
            matchlen = len(mo)
        else:
            matchlen = mo.end() - mo.start()
        return self.get_last_matched_text()[:-matchlen]

    def readline(self, timeout=None, err_dict=None):
        return self.read_until("\n", timeout=timeout, err_dict=err_dict)

    def readlines(self, N=2147483646, filt=None):
        """readlines([N], [filter])
Return a list of lines of input. Read up to N lines, optionally filterered
through a filter function.  """
        if filt:
            assert callable(filt)
        lines = [];
        n = 0
        while n < N:
            line = self.readline()
            if filt:
                if filt(line):
                    lines.append(line)
                    n += 1
            else:
                lines.append(line)
                n += 1
        return lines

    def peek(self, amt=64, timeout=None):
        """Read from file descriptor, but do not consumer any data from
        the I/O stream. Future calls to read() can still read peeked-at data"""

        timeout = timeout or self.default_timeout

        # enable alarm
        self._timed_out = 0
        signal.signal(signal.SIGALRM, self._timeout_cb)
        signal.alarm(int(round(timeout)))

        assert '_read_fill' in dir(self._fo), '_read_fill() does not exist'
        try:
            data = self._fo._read_fill(amt)
        except EOFError:
            return ''
        except OSError, val:
            assert val[0] == EINTR, 'expecting EINTR, but got: %s' % (str(val))
            assert self._timed_out == 1, 'EINTR not generated due to timeout'
            raise TimeoutError, "timed out during read."

        # disable alarm (there's a small race condition here)
        signal.alarm(0)

        return data

    def peekline(self, timeout=5):
        """Read line from descriptor, but do not consume any data from the
        I/O stream. Wrapper for peek() function."""
        s = ''
        while True:
            c = self.peek(amt=1, timeout=timeout)
            s += c
            if c == '\n':
                return s

    def isatty(self):
        return os.isatty(self._fo.fileno())

    def ttyname(self):
        return os.ttyname(self._fo.fileno())

    def tcgetpgrp(self):
        return os.tcgetpgrp(self._fo.fileno())

    def fstat(self):
        return os.fstat(self._fo.fileno())

    def seek(self, pos, whence=0):
        return os.lseek(self._fo.fileno(), pos, whence)

    def rewind(self):
        return os.lseek(self._fo.fileno(), 0, 0)

    # Note: this interactive method is currently incompatible with the asyncio usage.
    # (it has an internal select)
    def interact(self, msg=None, escape=None, cmd_interp=None):
        """ interact directly with the connection. Not entirely useful, but
            it seems to work.
        """
        if escape is None:
            escape = chr(29)  # ^]
        assert escape < " ", "escape key must be control character"
        self.cmd_interp = cmd_interp
        if self.cmd_interp:
            self.cmd_interp.set_session(self)
        print msg or "\nEntering interactive mode."
        print "Type ^%s to stop interacting." % (chr(ord(escape) | 0x40))
        # save tty state and set to raw mode
        stdin_fd = sys.stdin.fileno()
        fo_fd = self.fileno()
        ttystate = termtools.tcgetattr(stdin_fd)
        termtools.setraw(stdin_fd)
        try:
            self._fo.restart(1)
        except AttributeError:
            pass
        while 1:
            try:
                rfd, wfd, xfd = select.select([fo_fd, stdin_fd], [], [])
            except select.error, errno:
                if errno[0] == EINTR:  # interrupted system call
                    continue
            if fo_fd in rfd:
                try:
                    text = self._fo.read(100)
                except (OSError, EOFError), err:
                    termtools.tcsetattr(stdin_fd, termtools.TCSAFLUSH, ttystate)
                    print '*** EOF ***'
                    print err
                    break
                if text:
                    sys.stdout.write(text)
                    sys.stdout.flush()
                    if self._enable_ring_buffering:
                        self._ring_buf.append(text)
                else:
                    break
            if stdin_fd in rfd:
                char = sys.stdin.read(1)
                if char == escape:
                    termtools.tcsetattr(stdin_fd, termtools.TCSAFLUSH, ttystate)
                    if self.cmd_interp:
                        try:
                            self.cmd_interp.cmdloop()
                            termtools.setraw(stdin_fd)
                        except InteractiveQuit:
                            break
                        except:
                            extype, exvalue, tb = sys.exc_info()
                            sys.stderr.write("%s: %s\n" % (extype, exvalue))
                            sys.stderr.flush()
                            termtools.setraw(stdin_fd)
                    else:
                        break
                else:
                    try:
                        self.write(char)
                    except:
                        termtools.tcsetattr(stdin_fd, termtools.TCSAFLUSH, ttystate)
                        extype, exvalue, tb = sys.exc_info()
                        sys.stderr.write("%s: %s\n" % (extype, exvalue))
                        sys.stderr.flush()
                        termtools.setraw(stdin_fd)
        try:
            self._fo.restart(0)
        except AttributeError:
            pass

    def clear_cache(self):
        """Clears the pattern cache."""
        self._patt_cache.clear()

    def add_pattern(self, patt, mtype=EXACT, callback=None):
        """add_pattern(pattern, matchtype=EXACT, callback=None)
        Add a new pattern to the pattern cache.
        """
        return self._get_search_list(patt, mtype, callback)

    def match(self, text, patt=None, mtype=EXACT, callback=None):
        """Match text against a pattern, or set of patterns, as the expect
        method does. Does not consume input.  If the pattern is None, use the set from
        the cache.  You can add to the pattern cache with the add_pattern() method.
        """
        solist = self._get_search_list(patt, mtype, callback)
        self.matchindex = i = -1
        for so, cb in solist:
            mo = so.match(text)
            if mo:
                self.matchindex = i + 1
                if cb:
                    cb(mo)
                return mo
            i += 1
        return None

    def run(self):
        """run() runs this Expect engine until EOF on file object. Useful if
        you have added patterns with callbacks.
        """
        line = self.readline()
        while line:
            self.match(line)
            line = self.readline()

    # write methods
    def write(self, data, timeout=None):
        """ Writes data to file descriptor."""

        timeout = timeout or self.default_timeout

        # enable alarm
        self._timed_out = 0
        signal.signal(signal.SIGALRM, self._timeout_cb)
        signal.alarm(int(round(timeout)))

        try:
            data = self._fo.write(data)
        except OSError, val:
            assert val[0] == EINTR, 'expecting EINTR, but got: %s' % (str(val))
            assert self._timed_out == 1, 'EINTR not generated due to timeout'
            raise TimeoutError, "timed out during write."
        finally:
            signal.alarm(0)

        return data

    send = write

    def writeln(self, text=''):
        return self.write(text + "\n")

    writeline = writeln  # alias
    sendline = writeln
    # CLI batch commands get an alias to writeln
    # so as to make them easier to find in a test script
    send_batch_cmd = writeln

    def sendfile(self, filename, wait_for_prompt=0):
        """ send an entire file (via filename) through the connection. """
        fp = open(filename, "r")
        try:
            self.sendfileobject(fp, wait_for_prompt)
        finally:
            fp.close()

    def sendfileobject(self, fp, wait_for_prompt=0):
        """ send an entire file (via object) through the connection. """
        while 1:
            line = fp.read(4096)
            if not line:
                break
            self._fo.write(line)
            if wait_for_prompt:
                self.wait_for_prompt()


# convenience functions
def interact(fo):
    """interact(fileobject)
Factory function that wraps the fileobject with Expect, and runs the interact()
method. Mostly useful with 'proctools.Process' objects."""
    ex = Expect(fo)
    ex.interact()
