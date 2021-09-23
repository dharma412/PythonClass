#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/sal/deprecated/proctools.py#1 $
""" Classes and functions for controlling, reading, and writing to co-processes.  """

#: Reference Symbols: proctools

from __future__ import nested_scopes, absolute_import

import sys, os
from signal import SIGTERM, SIGSTOP, SIGCONT, SIGHUP, SIGINT
from errno import EINTR, ECHILD, EIO
import select
import fcntl

import time
import sal.deprecated.thirdparty.shparser as shparser
import sal.deprecated.thirdparty.termtools as termtools

SYSNAME = os.uname()[0]
if SYSNAME == 'Darwin':  # hack to get this to work with Mac OS-X's Darwin
    SYSNAME = 'FreeBSD'

import string

_CMDTRANS = string.maketrans("\0\n", "  ")
del string

# Global process manager
procmanager = None


class Process(object):
    """Abstract base class for Processes. Handles all process handling, and
    some common functionality. I/O is handled in subclasses."""

    def __init__(self, cmdline, logfile=None, env=None, callback=None):
        """ Constructor:

            cmdline: command to run
            logfile: write output to a log?
            env: Seems to do nothing
            callback: function to call at the death of process
        """
        self.cmdline = cmdline
        self.name = cmdline.split()[0]
        self.deadchild = 0
        self.childpid = 0
        self.callback = callback  # called at death of process
        self._log = logfile  # should be file-like object
        self._restart = 1  # restart interrupted system calls
        self._rawq = ''
        # pointer indicating which bytes have been consumed
        self._rawq_idx = 0
        self._buf = ''
        self._errbuf = ''
        self._writebuf = ''
        self.exitstatus = None

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.cmdline, self._log)

    def __str__(self):
        if self.deadchild:
            return str(self.exitstatus)
        else:
            st = self.stat()
            try:
                tty = os.ttyname(self.fileno())
            except:
                tty = "?"
            return "%6d %-7s (%s) %s" % (st.pid, tty, st.statestr(), self.cmdline)

    def __int__(self):
        return self.childpid

    def __hash__(self):
        return id(self)

    def fileno(self):
        raise NotImplementedError

    def restart(self, flag=1):
        self._restart = bool(flag)

    def newlog(self, newlog):
        self._log = newlog

    setlog = newlog

    def flushlog(self):
        if self._log:
            self._log.flush()

    def clone(self, env=None):
        """clone([newenv])
Spawns a copy of this process. Note that the log file is not inherited."""
        return self.__class__(self.cmdline, env=env, callback=self.callback)

    def basename(self):
        return os.path.basename(self.cmdline.split()[0])

    def kill(self, sig=SIGTERM):
        """ Kill the child process. """
        if not self.deadchild:
            os.kill(self.childpid, sig)

    def killwait(self, sig=SIGTERM):
        """ Kill the child process and wait. """
        if not self.deadchild:
            os.kill(self.childpid, sig)
        return self.wait()

    def stop(self):
        os.kill(self.childpid, SIGSTOP)

    def cont(self):
        os.kill(self.childpid, SIGCONT)
        self.deadchild = 0

    def hangup(self):
        os.kill(self.childpid, SIGHUP)

    def wait(self, option=0):
        """wait() retrieves process exit status. Note that this may block if
the process is still running."""
        procmanager.waitproc(self, option)
        return self.exitstatus

    def setpgid(self, pgid):
        os.setpgid(self.childpid, pgid)

    def set_exitstatus(self, exitstatus):
        self.exitstatus = exitstatus

    def set_callback(self, cb=None):
        """set_callback(cb) Sets the callback function that will be
called when child dies. """
        self.callback = cb

    def dead(self):
        """dead() Called when the child dies. Usually only the
ProcManager uses this."""
        self.deadchild = 1
        if self.callback:
            self.callback(self.exitstatus)  # should be set by now

    def stat(self):
        """ return the status of the child process. """
        if not self.deadchild:
            return ProcStat(self.childpid)
        else:
            return self.exitstatus

    def isdead(self):
        return self.deadchild

    # process object considered true if child alive, false if child dead
    def __nonzero__(self):
        return not self.deadchild

    def _read(self, amt):
        raise NotImplementedError

    def read(self, amt=2147483646, timeout=None):
        """ read from the process' stdout. """
        bs = len(self._buf)
        try:
            while bs < amt:
                if self._rawq:
                    # pop up to 4096 bytes off rawq
                    c = self._rawq[:4096]
                    # next read() starts from updated _rawq_idx  pointer
                    self._rawq_idx = max(0, self._rawq_idx - len(c))
                    self._rawq = self._rawq[len(c):]
                else:
                    c = self._read(4096, timeout)
                if not c:
                    break
                self._buf += c
                bs = len(self._buf)
        except EOFError:  # XXX log an error
            pass  # let it return rest of buffer
        data = self._buf[:amt]
        self._buf = self._buf[amt:]
        return data

    def _readerr(self, amt):
        raise NotImplementedError

    def readerr(self, amt=2147483646):
        """ read from the process' stderr. """
        rs = 1024
        try:
            while len(self._errbuf) < amt:
                c = self._readerr(rs)
                if not c:
                    break
                self._errbuf += c
        except EOFError:
            pass
        amt = min(amt, len(self._errbuf))
        data = self._errbuf[:amt]
        self._errbuf = self._errbuf[amt:]
        return data

    # extra fileobject methods.
    def readline(self, amt=2147483646):
        bufs = []
        rs = min(100, amt)
        while 1:
            c = self.read(rs)
            i = c.find("\n")

            if i < 0 and len(c) > amt:
                i = amt - 1
            elif amt <= i:
                i = amt - 1
            if i >= 0 or c == '':
                bufs.append(c[:i + 1])
                self._unread(c[i + 1:])
                break

            bufs.append(c)
            amt -= len(c)
            rs = min(amt, rs * 2)

        return "".join(bufs)

    def readlines(self, sizehint=2147483646):
        rv = []
        while sizehint > 0:
            line = self.readline()
            if not line:
                break
            rv.append(line)
            sizehint -= len(line)
        return rv

    def _write_buf(self):
        writ = self._write(self._writebuf)
        self._writebuf = self._writebuf[writ:]
        return writ

    def _write(self, data):
        raise NotImplementedError

    def write(self, data):
        while self._writebuf:
            writ = self._write(self._writebuf)
            self._writebuf = data[writ:]
        writ = self._write(data)
        self._writebuf = data[writ:]
        return writ

    send = write

    def tell(self):
        raise IOError, "Process object not seekable"

    def seek(self, pos, whence=0):
        raise IOError, "Process object not seekable"

    def rewind(self):
        raise IOError, "Process object not seekable"

    def flush(self):
        return None

    def _unread(self, data):
        self._buf = data + self._buf

    def _read_fill(self, amt=1024):
        eof = False
        buf_sz = len(self._rawq[self._rawq_idx:])

        # read at least 'amt' bytes of new data;append to rawq
        try:
            while buf_sz < amt:
                data = self._read(4096)
                if not data:
                    break
                self._rawq += data
                buf_sz += len(data)
        except EOFError:
            eof = True  # return rest of buffer

        data = self._rawq[self._rawq_idx:self._rawq_idx + amt]
        if not eof:
            assert len(data) == amt, 'length of data(%d) != amt' % len(data)
        self._rawq_idx += len(data)

        # use <=  instead of < to handle empty rawq case
        assert self._rawq_idx <= len(self._rawq), \
            'rawq_idx(%d) > len(rawq)' % self._rawq_idx
        return data

    def _readerr_fill(self):
        try:
            c = self._readerr(8192)
            if not c:
                return
            self._errbuf += c
        except (IOError, EOFError):
            ex, val, tb = sys.exc_info()
            print >> sys.stderr, "*** Error:", ex, val


class ProcessPipe(Process):
    """ProcessPipe(<commandline>, [<logfile>], [environ])
    Forks and execs a process as given by the command line argument. The
    process's stdio is connected to this instance via pipes, and can be read
    and written to by the instances read() and write() methods.

    """

    def __init__(self, cmdline, logfile=None, env=None, callback=None, merge=1):
        """ Constructor has the same args as Process() except:

            merge: If true, merge stderr into stdout from child process
        """
        Process.__init__(self, cmdline, logfile, env, callback)

        cmd = split_command_line(self.cmdline)
        # now, fork the child connected by pipes
        p2cread, self._p_stdin = os.pipe()
        self._p_stdout, c2pwrite = os.pipe()
        if merge:
            self._stderr, c2perr = None, None
        else:
            self._stderr, c2perr = os.pipe()
        self.childpid = os.fork()
        if self.childpid == 0:
            # Child
            os.close(0)
            os.close(1)
            os.close(2)
            if os.dup(p2cread) <> 0:
                os._exit(1)
            if os.dup(c2pwrite) <> 1:
                os._exit(1)
            if merge:
                if os.dup(c2pwrite) <> 2:  # merge stderr into stdout from child process
                    os._exit(1)
            else:
                if os.dup(c2perr) <> 2:
                    os._exit(1)
            # close all other file descriptors for child.
            for i in xrange(3, 256):
                try:
                    os.close(i)
                except:
                    pass
            try:
                if env:
                    os.execvpe(cmd[0], cmd, env)
                else:
                    os.execvp(cmd[0], cmd)
            finally:
                os._exit(1)
            # Shouldn't come here
            os._exit(1)
        os.close(p2cread)
        os.close(c2pwrite)
        if c2perr:
            os.close(c2perr)

    def isatty(self):
        return os.isatty(self._p_stdin)

    def fileno(self):
        if self._p_stdout is None:
            raise ValueError, "I/O operation on closed process"
        return self._p_stdout

    def filenos(self):
        """filenos() Returns tuple of all file descriptors used in this object."""
        if self._p_stdout is None:
            raise ValueError, "I/O operation on closed process"
        return self._p_stdout, self._p_stdin, self._stderr

    def nonblocking(self, flag=1):
        for fd in self._p_stdout, self._p_stdin, self._stderr:
            set_nonblocking(fd, flag)

    def interrupt(self):
        self.kill(SIGINT)

    def close(self):
        try:
            os.close(self._p_stdin)
        except (TypeError, OSError):
            pass
        try:
            os.close(self._p_stdout)
        except (TypeError, OSError):
            pass
        if self._stderr:
            try:
                os.close(self._stderr)
            except (TypeError, OSError):
                pass
            self._stderr = None
        self._p_stdin = None
        self._p_stdout = None
        self.callback = None  # break a possible reference loop

    def _write(self, data):
        while 1:
            try:
                writ = os.write(self._p_stdin, data)
            except OSError, why:
                if self._restart and why[0] == EINTR:
                    continue
                else:
                    raise

            return writ

    def _read_fd(self, fd, length):
        while 1:
            try:
                next = os.read(fd, length)
            except OSError, why:
                if self._restart and why[0] == EINTR:
                    continue
                else:
                    raise
            else:
                break
        if self._log:
            self._log.write(next)
        return next

    def _read(self, amt=4096):
        if self._p_stdout is None:
            return ""
        return self._read_fd(self._p_stdout, amt)

    def _readerr(self, amt):
        if self._stderr is None:
            return ""
        return self._read_fd(self._stderr, amt)


class ProcessPty(Process):
    """ProcessPty(<commandline>, [<logfilename>], [environ])
    Forks and execs a process as given by the command line argument. The
    process's stdio is connected to this instance via a pty, and can be read
    and written to by the instances read() and write() methods. That pty
    becomes the processes controlling terminal.

    """

    def __init__(self, cmdline, logfile=None, env=None, callback=None, merge=1):
        """ Constructor has the same args as Process() except:

            merge: If true, merge stderr into stdout from child process
        """
        Process.__init__(self, cmdline, logfile, env, callback)
        cmd = split_command_line(self.cmdline)
        try:
            pid, self._fd = os.forkpty()
        except OSError, err:
            print >> sys.stderr, "ProcessPty: Cannot forkpty."
            print >> sys.stderr, str(err)
            raise

        else:
            if pid == 0:  # child
                for i in xrange(3, 64):
                    try:
                        os.close(i)
                    except:
                        pass
                try:
                    if env:
                        os.execvpe(cmd[0], cmd, env)
                    else:
                        os.execvp(cmd[0], cmd)
                finally:
                    os._exit(1)  # should not be reached

            else:  # parent
                self.childpid = pid
                self._intr = None

    def isatty(self):
        return os.isatty(self._fd)

    def fileno(self):
        if self._fd is None:
            raise ValueError, "I/O operation on closed process"
        return self._fd

    def filenos(self):
        """filenos() Returns tuple of all file descriptors used in this object."""
        if self._fd is None:
            raise ValueError, "I/O operation on closed process"
        return (self._fd,)

    def nonblocking(self, flag=1):
        set_nonblocking(self._fd, flag)

    def interrupt(self):
        if self._intr is None:
            self._intr = termtools.get_intr_char(self._fd)
        self._write(self._intr)

    def close(self):
        try:
            os.close(self._fd)
        except (TypeError, OSError):
            pass
        self._fd = None
        self.callback = None  # break a possible reference loop

        # wait ~10s for child process's pid to be removed from /proc
        for i in range(100):
            if not os.access('/proc/' + str(self.childpid), os.R_OK):
                break  # childpid file has been successfully removed
            time.sleep(0.1)
        else:
            print 'ProcessPty.close():child pty process not cleaned up!'

    def _write(self, data):
        while 1:
            try:
                writ = os.write(self._fd, data)
            except OSError, why:
                if self._restart and why[0] == EINTR:
                    continue
                else:
                    raise

            return writ

    def _read(self, length=100, timeout=None):
        while 1:
            try:
                if not is_nonblocking(self._fd):
                    # Use select.select() to work around bug18939
                    # (Python mishandle sigalrms on blocking reads())
                    if timeout is not None:
                        r_ready, _, _ = select.select([self._fd], [], [], timeout)
                    else:
                        select.select([self._fd], [], [])
                        r_ready = [self._fd]
                # else if FD is non-blocking:
                #   1. we should -not- do a select() (which will hang)
                #   2. os.read() bug will not appear since read()
                #      will not block and therefore not hang.
                if self._fd in r_ready:
                    next = os.read(self._fd, length)
                else:
                    raise OSError(EINTR)
            except (OSError, select.error), why:
                if why[0] == EINTR:
                    if self._restart:
                        continue
                    else:
                        raise OSError(*why)
                elif why[0] == EIO:
                    raise EOFError, "pty is closed"
                else:
                    raise
            else:
                break
        if self._log:
            self._log.write(next)

        return next


class CoProcessPty(ProcessPty):
    def __init__(self, savefiles=None, logfile=None, env=None, callback=None):
        """ savefiles is a list of file-like objects or integer file descriptors
            that we would like to preserve in the subprocess. If not listed here,
            they will be closed.
        """
        Process.__init__(self, " ".join(sys.argv), logfile, env, callback)
        pid, self._fd = os.forkpty()
        if pid == 0:  # child
            savefiles = savefiles or []
            if logfile:
                savefiles.append(logfile)
            sf_ints = filter(lambda o: o is int, savefiles)
            sf_obj = filter(lambda o: hasattr(o, "fileno"), savefiles)
            sf = sf_ints + map(lambda o: o.fileno(), sf_obj)
            for i in xrange(3, 64):
                if i not in sf:
                    try:
                        os.close(i)
                    except:
                        pass
        self.childpid = pid


class SubProcess(Process):
    """ simply forks this python process. """

    def __init__(self):
        Process.__init__(self, sys.argv[0])
        pid = os.fork()
        self.childpid = pid


class ProcStat:
    """Status information about a process. """
    # Linux 2.4 /proc/PID/stat format
    _STATINDEXLinux = {
        "pid": 0,
        "command": 1,
        "state": 2,
        "ppid": 3,
        "pgrp": 4,
        "session": 5,
        "tty_nr": 6,
        "tty_pgrp": 7,
        "flags": 8,
        "min_flt": 9,
        "cmin_flt": 10,
        "maj_flt": 11,
        "cmaj_flt": 12,
        "tms_utime": 13,
        "tms_stime": 14,
        "tms_cutime": 15,
        "tms_cstime": 16,
        "priority": 17,
        "nice": 18,
        # "_removed": 19,
        "it_real_value": 20,
        "start_time": 21,
        "vsize": 22,
        "rss": 23,  # you might want to shift this left 3
        "rlim_cur": 24,
        "mm_start_code": 25,
        "mm_end_code": 26,
        "mm_start_stack": 27,
        "esp": 28,
        "eip": 29,
        "sig_pending": 30,  # these are depricated, don't use
        "sig_blocked": 31,
        "sig_ignore": 32,
        "sig_catch": 33,
        "wchan": 34,
        "nswap": 35,
        "cnswap": 36,
        "exit_signal": 37,
        "processor": 38,
    }
    # FreeBSD /proc/PID/status format
    _STATINDEXFreeBSD = {
        "command": 0,
        "pid": 1,
        "ppid": 2,
        "pgid": 3,
        "sid": 4,
        "ctty": 5,
        "flags": 6,
        "start": 7,
        "ut": 8,
        "st": 9,
        "wchan": 10,
        "euid": 11,
        "ruid": 12,
        "groups": 13,
    }
    #   "RSDZTW"
    _STATSTR = {
        "R": "running",
        "S": "sleeping",
        "D": "uninterruptible disk sleep",
        "Z": "zombie/defunct",
        "T": "traced/stopped",
        "W": "paging"
    }
    _FF = {"Linux": "/proc/%d/stat", "FreeBSD": "/proc/%d/status"}[SYSNAME]
    _STATINDEX = {"Linux": _STATINDEXLinux, "FreeBSD": _STATINDEXFreeBSD}[SYSNAME]

    def __init__(self, pid=None):
        self.pid = None
        self.read(pid)

    # so sorting works
    def __lt__(self, other):
        return self.pid < other.pid

    def __gt__(self, other):
        return self.pid > other.pid

    def __eq__(self, other):
        return self.pid == other.pid

    def _toint(self, it):
        try:
            return int(it)
        except ValueError:
            return it

    def reread(self):
        self.read(self.pid)
        return self

    def read(self, pid=None):
        if pid is not None:
            self.pid = int(pid)
        if self.pid is not None:
            try:
                self.stats = tuple(map(self._toint, open(self._FF % (self.pid)).read().split()))
            except IOError:  # no such process
                self.pid = None
                self.stats = None
        else:
            self.stats = None
        return self

    def statestr(self):
        try:
            return self._STATSTR[self.stats[self._STATINDEX["state"]]]
        except:
            return "?"

    def RSS(self):
        try:
            return self.stats[self._STATINDEX["rss"]] << 3
        except:
            return 0

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.pid)

    def __str__(self):
        if self.stats is None:
            return "no stats - invalid pid?"
        else:
            s = ["%15s: %s" % ("cmdline", self.get_cmdline())]
            names = self._STATINDEX.keys()
            names.sort()
            # for name, i in self._STATINDEX.items():
            for name in names:
                i = self._STATINDEX[name]
                s.append("%15s: %s" % (name, self.stats[i]))
            return "\n".join(s)

    def get_attributes(self):
        return self._STATINDEX.keys()

    def get_cmdline(self):
        try:
            cmd = file("/proc/%d/cmdline" % (self.pid,)).read()
        except IOError:
            self.pid = None
            return "<exited>"
        cmd = cmd.translate(_CMDTRANS).strip()
        if not cmd:
            return self.cmdline
        else:
            return cmd

    cmdline = property(get_cmdline, None, None, "Command line")

    def _get_ttyname_linux(self):
        tty_nr = self["tty_nr"]
        if tty_nr:
            minor = tty_nr & 0xff
            major = (tty_nr >> 8) & 0xff  # XXX
            try:
                name = os.readlink("/proc/%d/fd/2" % (self.pid))
            except OSError:
                return "%d,%d" % (major, minor)  # XXX
            else:
                try:
                    os.stat(name)
                except OSError:
                    if major == 136:
                        name = "/dev/pts/%d" % (minor,)
                        try:
                            os.stat(name)
                        except OSError:
                            name = "%d,%d" % (major, minor)  # XXX
                    else:
                        name = "%d,%d" % (major, minor)  # XXX
                return name
        else:
            return "?"

    def _get_ttyname_bsd(self):
        #        import FreeBSD.devdb
        #        [major, minor] = map(int, self.ctty.split(","))
        #        if major < 0:
        #            return "?"
        #        db = FreeBSD.devdb.open()
        #        try:
        #            name = db.get_char(major, minor)
        #        except:
        #            name = "?"
        #        db.close()
        #        return name
        return

    ttyname = {"Linux": property(_get_ttyname_linux, None, None, None),
               "FreeBSD": property(_get_ttyname_bsd, None, None, None)}[SYSNAME]

    def get_stat(self, name):
        if not self.stats:
            raise ValueError, "no stats - run read(pid)"
        try:
            val = self.stats[self._STATINDEX[name]]
        except KeyError:
            raise ValueError, "no attribute %s" % name
        # ugly hack to work around Linux having "(,)" around command name
        if name == "command" and SYSNAME == "Linux":
            return val[1:-1]
        else:
            return val

    def __getattr__(self, name):
        try:
            return self.get_stat(name)
        except ValueError, err:
            raise AttributeError, err

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError, err:
            raise KeyError, err


class ProcStatTable:
    """ProcStatTable()
A collection of all processes running, like the standard 'ps' command. """

    def __init__(self, fmt="%(pid)6s %(ppid)6s %(ttyname)6.6s %(cmdline).55s"):
        self.fmt = fmt
        self._ptable = None

    def read(self):
        rv = self._ptable = {}
        for pfile in os.listdir("/proc"):
            try:
                pid = int(pfile)  # filter out non-numeric entries in /proc
            except ValueError:
                continue
            rv[pid] = ProcStat(pid)

    def __len__(self):
        return len(self._ptable)

    def __getitem__(self, pid):
        return self._ptable[pid]

    def __iter__(self):
        return self._ptable.itervalues()

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.fmt)

    def __str__(self):
        self.read()
        s = []
        k = self._ptable.keys()
        k.sort()
        for pid in k:
            s.append(self.fmt % self._ptable[pid])
        return "\n".join(s)

    # this is here because $#%@# FreeBSD ps can't print a tree of procs (a
    # helpful debugging aid)
    def tree(self):
        class _pholder:
            pass

        self.read()
        if not self._ptable.has_key(0):
            p0 = self._ptable[0] = _pholder()
            p0.pid = p0.ppid = 0
            p0.cmdline = "<kernel>"
        for p in self._ptable.values():
            try:
                self._ptable[p.ppid]._children.append(p.pid)
            except AttributeError:  # no child list yet
                self._ptable[p.ppid]._children = sortedlist([p.pid])

        pslist = self._tree_helper(self._ptable[0], 0, [])
        return "\n".join(pslist)

    # recursive helper to indent according to child depth
    def _tree_helper(self, obj, level, rv):
        rv.append("%s%6d %.60s" % ("  " * level, obj.pid, obj.cmdline))
        if not hasattr(obj, "_children"):
            return rv
        for cpid in obj._children:
            if cpid != obj.pid:
                self._tree_helper(self._ptable[cpid], level + 1, rv)
        return rv


class sortedlist(list):
    """ a list that self-maintains a sorted order. Insert items with
        insort(x). """

    def insort(self, x):
        hi = len(self)
        lo = 0
        while lo < hi:
            mid = (lo + hi) // 2
            if x < self[mid]:
                hi = mid
            else:
                lo = mid + 1
        self.insert(lo, x)

    append = insort


class ExitStatus:
    """ Encapsulate the ExitStatus information into a class. """
    EXITED = 1
    STOPPED = 2
    SIGNALED = 3

    def __init__(self, name, sts):
        self.name = name
        if os.WIFEXITED(sts):
            self.state = 1
            self._status = self.exitstatus = os.WEXITSTATUS(sts)

        elif os.WIFSTOPPED(sts):
            self.state = 2
            self._status = self.stopsig = os.WSTOPSIG(sts)

        elif os.WIFSIGNALED(sts):
            self.state = 3
            self._status = self.termsig = os.WTERMSIG(sts)

    def status(self):
        return self.state, self._status

    def exited(self):
        return self.state == 1

    def stopped(self):
        return self.state == 2

    def signalled(self):
        return self.state == 3

    def __int__(self):
        if self.state == 1:
            return self._status
        else:
            raise ValueError, "ExitStatus: did not exit normally"

    # exit status truth value is true if normal exit, and false otherwise.
    def __nonzero__(self):
        return (self.state == 1) and not self._status

    def __str__(self):
        if self.state == 1:
            if self.exitstatus == 0:
                return "%s: Exited normally." % (self.name)
            else:
                return "%s: Exited abnormally with status %d." \
                       % (self.name, self.exitstatus)
        elif self.state == 2:
            return "%s is stopped." % (self.name)
        elif self.state == 3:
            return "%s exited by signal %d. " % (self.name, self.termsig)
        else:
            return "FIXME! unknown state"


class ProcManager:
    """An instance of ProcManager manages a collection of child processes. It
is a singleton, and you should use the get_procmanager() factory function
to get the instance.  """

    def __init__(self):
        self._procs = {}
        self._graveyard = {}

    def __len__(self):
        return len(self._procs)

    def __str__(self):
        s = []
        for p in self.getprocs():
            s.append(str(p))
        return "\n".join(s)

    def spawnprocess(self, pklass, cmd, logfile=None, env=None, callback=None,
                     persistent=0, merge=1):
        """spawnclass(classobj, cmd, logfile=None, env=None, callback=None, persistent=0)
Start a child process using a user supplied subclass of ProcessPty or
ProcessPipe.  """

        if persistent and (callback is None):
            callback = self._persistent_callback
        proc = pklass(cmd, logfile=logfile, env=env, callback=callback, merge=merge)
        self._procs[proc.childpid] = proc
        return proc

    def add_process(self, proc):
        """add_process(ProcessObject)
Adds an already instantiated Process object to the manager."""
        self._procs[proc.childpid] = proc

    def spawnpipe(self, cmd, logfile=None, env=None, callback=None,
                  persistent=0, merge=1):
        """spawn(cmd, logfile=None, env=None, callback=None, persisten=None)
Start a child process, connected by pipes."""
        return self.spawnprocess(ProcessPipe, cmd, logfile, env, callback,
                                 persistent, merge)

    # default spawn method
    spawn = spawnpipe

    def spawnpty(self, cmd, logfile=None, env=None, callback=None,
                 persistent=0, merge=1):
        """spawnpty(cmd, logfile=None, env=None, callback=None, persisten=None)
Start a child process using a pty. The <persistent> variable is the number of
times the process will be respawned if the previous invocation dies.  """
        return self.spawnprocess(ProcessPty, cmd, logfile, env, callback,
                                 persistent, merge)

    def coprocess(self, method, args=(), savefiles=None, logfile=None, env=None, callback=None):
        """ Spawn a coprocess. """
        proc = CoProcessPty(savefiles=None, logfile=None, env=None, callback=None)
        if proc.childpid == 0:
            sys.excepthook = sys.__excepthook__
            # child is not managing any of these
            self._procs.clear()
            self._graveyard.clear()
            try:
                rv = apply(method, args)
            except:
                rv = 99
            if rv is None:
                rv = 0
            try:
                rv = int(rv)
            except:
                rv = 0
            os._exit(rv)
        self._procs[proc.childpid] = proc
        return proc

    def subprocess(self, method, *args, **kwargs):
        """ Spawn a subprocess. """
        proc = SubProcess()
        if proc.childpid == 0:  # in child
            sys.excepthook = sys.__excepthook__
            self._procs.clear()
            self._graveyard.clear()
            try:
                rv = apply(method, args, kwargs)
            except:
                rv = 99
            if rv is None:
                rv = 0
            try:
                rv = int(rv)
            except:
                rv = 0
            os._exit(rv)
        else:
            self._procs[proc.childpid] = proc
            return proc

    # introspection and query methods
    def getpids(self):
        """getpids() Returns a list of managed PIDs (which are integers)."""
        return self._procs.keys()

    def getprocs(self):
        """getprocs() Returns a list of managed process objects."""
        return self._procs.values()

    def getbyname(self, name):
        """getbyname(procname) Returns a list of process objects that match the given name."""
        name = os.path.basename(name)
        return filter(lambda p: p.basename() == name, self._procs.values())

    def getbypid(self, pid):
        """getbypid(pid) Returns the process object that matches the given PID."""
        try:
            return self._procs[pid]
        except KeyError:
            return None

    def getstats(self):
        """getstats() Returns a list of process status objects (ProcStat) for each managed process."""
        return map(ProcStat, self._procs.keys())

    def killall(self, name=None, sig=SIGTERM):
        """killall([name, [SIG]]) Kills all managed processes with the name
'name'. If 'name' not given kill ALL processes. Default signal is SIGTERM."""
        if name is None:
            procs = self._procs.values()
        else:
            procs = self.getbyname(name)
        for p in procs:
            print 'proctools.ProcManager(): killing process', p
            self.kill(p, sig)

    def kill(self, proc, sig=SIGTERM):
        proc.set_callback(None)  # explicit kill means no restart
        proc.kill(sig)

    def stopall(self, exceptions=None):
        """stopall() sends STOP to all managed processes. To restart get the
process objects and invoke the cont() method."""
        if exceptions is None:
            exceptions = []
        for p in self._procs.values():
            if not p in exceptions:
                print 'proctools.ProcManager(): stopping process', p
                p.stop()

    def closeall(self, exceptions=None):
        """closeall() sends close to all managed file descriptors. """
        if exceptions is None:
            exceptions = []
        for p in self._procs.values():
            if not p in exceptions:
                try:
                    print 'proctools.ProcManager(): closing process', p
                except TypeError:
                    pass
                p.close()

    def waitproc(self, proc, option=0):  # waits for a Process object.
        """waitproc(process, [option])
Waits for a process object to finish. Works like os.waitpid, but takes a
process object instead of a process ID.  """
        pid = int(proc)
        while 1:
            if pid in self._graveyard:
                es = self._graveyard[pid]
                del self._graveyard[pid]
                return es
            elif pid in self._procs:
                if (option & os.WNOHANG):
                    return 0
                self.waitpid(pid, 0)
            else:
                raise ValueError, "pid or proc is unmanaged."

    def clone(self, proc=None):
        """clone([proc]) clones the supplied process object and manages it as
well. If no process object is supplied then clone the first managed
process found in this ProcManager."""
        if proc is None:  # default to cloning first process found.
            procs = self._procs.values()
            if procs:
                proc = procs[0]
                del procs
            else:
                return
        newproc = proc.clone()
        self._procs[newproc.childpid] = newproc
        return newproc

    def _persistent_callback(self, deadproc):
        if not deadproc.exitstatus:  # abnormal exit
            sys.stderr.write("*** process died: %s (restarting)\n" % (deadproc.exitstatus))
            self.clone(deadproc)
        else:
            sys.stderr.write("*** process exited (NOT restarting)")

    def child_status(self, pid_or_proc):
        pid = int(pid_or_proc)
        try:
            es = self._graveyard[pid]
            del self._graveyard[pid]
            return es
        except KeyError:
            try:
                proc = self._procs[pid]
                return proc.stat()
            except KeyError:
                return None  # XXX exception?

    def waitpid(self, pid, option=0):
        while 1:  # loop to collect all pending exited processes
            try:
                pid, sts = os.waitpid(pid, option)
            except OSError, why:
                if why[0] == ECHILD:  # no children left
                    break
                elif why[0] == EINTR:
                    continue
                else:
                    raise
            else:
                if pid == 0:  # no child ready
                    break
                else:
                    try:
                        proc = self._procs[pid]
                    except KeyError:
                        sys.stderr.write("warning: caught SIGCHLD for unmanaged process (pid: %s).\n" % pid)
                        continue
                    es = ExitStatus(proc.name, sts)
                    proc.set_exitstatus(es)
                    if es.state != ExitStatus.STOPPED:  # XXX untested with stopped processes
                        proc.dead()
                        del self._procs[pid]
                        self._graveyard[pid] = proc.exitstatus


def is_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    if flags & os.O_NONBLOCK:
        return True
    else:
        return False


def get_procmanager():
    """get_procmanager() returns the procmanager. A ProcManager is a singleton
instance. Always use this factory function to get it."""
    global procmanager
    if not procmanager:
        procmanager = ProcManager()
    return procmanager


def remove_procmanager():
    global procmanager
    del procmanager


#######################################
#### Utility functions for Linux ######

# standalone process factory functions
def spawnpipe(cmd, logfile=None, env=None, callback=None,
              persistent=0, merge=1):
    """spawn(cmd, logfile=None, env=None)
Start a child process, connected by pipes."""
    pm = get_procmanager()
    proc = pm.spawnpipe(cmd, logfile, env, callback, persistent, merge)
    return proc


def spawnpty(cmd, logfile=None, env=None, callback=None,
             persistent=0, merge=1):
    """spawnpty(cmd, logfile=None, env=None)
Start a child process using a pty."""
    pm = get_procmanager()
    proc = pm.spawnpty(cmd, logfile, env, callback, persistent, merge)
    return proc


def coprocess(func, args=(), savefiles=None, logfile=None, callback=None):
    """coprocess(func, args, [savefiles, logfile, callback])
Works like fork(), but connects the childs stdio to a pty. Returns a file-like
object connected to the master end of the child pty.  """
    cp = procmanager.coprocess(func, args, savefiles, logfile, callback)
    return cp


def subprocess(method, *args, **kwargs):
    return procmanager.subprocess(method, *args, **kwargs)


##### useful shell-command-like functions.

def pidof(procname):
    """pidof(procname) Returns a list of PIDs (integers) that match the given process name."""
    rv = []
    ps = ProcStat()  # use the ProcStat object as a parser.
    for pfile in os.listdir("/proc"):
        try:
            pid = int(pfile)  # also filters out non-numeric entries in /proc
        except ValueError:
            continue
        ps.read(pid)
        if ps.command == procname:
            rv.append(ps.pid)
    return rv


def ps(argv=None):
    """ print output of ps via ProcStat. """
    if not argv:
        t = ProcStatTable()
        t.read()
        print t
    else:
        for spid in argv:
            try:
                pid = int(spid)
            except:
                continue
            print
            print ProcStat(pid)


def pstree():
    t = ProcStatTable()
    print t.tree()


def killall(procname, sig=SIGTERM):
    """killall(procname, [signal]) Sends a signal (default SIGTERM) to all processes that match the given name."""
    for pid in pidof(procname):
        os.kill(pid, sig)


def which(basename):
    """returns the fully qualified path name (by searching PATH) of the given program name."""
    for pe in os.environ["PATH"].split(os.pathsep):
        testname = os.path.join(pe, basename)
        if os.access(testname, os.X_OK):
            return testname
    raise ValueError, "which: no %s in $PATH." % basename


def getstatusoutput(cmd, logfile=None, env=None, callback=None):
    p = spawnpipe(cmd, logfile, env, callback)
    text = p.read()
    p.wait()
    return p.exitstatus, text


def set_nonblocking(fd, flag=1):
    import fcntl
    try:
        fd = int(fd)
    except TypeError:
        return
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    if flag:
        flags |= os.O_NONBLOCK  # set non-blocking
    else:
        flags &= ~os.O_NONBLOCK  # set blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def system(cmd):
    name = os.path.basename(cmd.split()[0])
    sts = os.system(cmd)
    return ExitStatus(name, sts)


def setpgid(pid_or_proc, pgrp):
    pid = int(pid_or_proc)
    return os.setpgid(pid, pgrp)


# helper to use shparser as command splitter.
class CommandSplitter(object):
    def __init__(self):
        self._argv = None
        self._cmd_parser = shparser.ShellParser(self._cb)

    def _cb(self, argv):
        self._argv = argv

    def feedline(self, text):
        self._cmd_parser.feedline(text)
        return self._argv


_cmd_splitter = CommandSplitter()
split_command_line = _cmd_splitter.feedline

if __name__ == "__main__":
    print "**** normal 'ls' test"
    ls = spawnpipe("ls /usr/bin")
    # files = ls.readlines()
    print ls.stat()
    files = ls.read()
    print repr(files)
    # procmanager.poll()
    print "errors:"
    print repr(ls.readerr())
    print "*** Waiting..."
    es = ls.close()
    print es
    if es:
        print "normal exit"
    else:
        print "ls exited abromally"

    del ls
    print
    print "***** with errors "
    ls = spawnpipe("ls /usr/binxx", merge=0)
    print "output:"
    print ls.read()
    print "errors:"
    print ls.readerr()
    es = ls.close()
    print es

    print
    print "**** readline test"
    lspm = procmanager.spawnpipe("ls /bin")
    print lspm.readlines()
    print lspm.exitstatus
    lspm.close()
    del ls, lspm


    #   from sal.deprecated import expect
    #   py = coprocess()
    #   if py is not None:
    #       #print py.read()
    #       eo = expect.Expect(py)
    #       eo.interact()
    #       print "back to parent"
    #       del eo
    #       py.close()
    #   del py
    #
    def Test():
        import time
        while 1:
            print "XXX printing from child"
            time.sleep(2)


    #   subprocess(Test)

    ps()
