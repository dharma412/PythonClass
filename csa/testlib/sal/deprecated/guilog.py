#!/usr/bin/python

"""
Managing logfile rotation. A ManagedLog object is a file-like object that
rotates itself when a maximum size is reached.

Warning: Deprecated. Consider using standard logging functionality

"""
# $Id: //prod/main/sarf_centos/testlib/sal/deprecated/guilog.py#1 $

from __future__ import absolute_import

#: Reference Symbols: guilog

import sys, os
import cgi
import re
import types
import warnings

warnings.warn("this module is deprecated, use sal.loggin", DeprecationWarning)

__globalGuiLogs = {}


class SizeError(IOError):
    pass


class GuiLog:
    """LogFile(name, [maxsize=1000])
    Opens a new file object. After writing <maxsize> pages a SizeError will be
    raised.  """

    def __init__(self, name, maxsize=1000):
        self.dirname = name
        self.name = name
        self.maxsize = maxsize
        self.written = []
        self.guipage = None

        self._setupdir()

    def _setupdir(self):
        os.makedirs(self.dirname)
        os.chmod(self.dirname, 0777)
        fp = open(self.dirname + "/blank.html", "w")
        fp.close()
        fp = open(self.dirname + "/contents.html", "w")
        fp.write("""
<html>
<head>
<style type="text/css"><!--
    a:link    { text-decoration: none;
                color: #ffffff; }
    a:visited { text-decoration: none;
                color: #eeeeee; }
    a:hover   { text-decoration: underline;
                color: #000000; }

    body {
        background-color: #666699;
        font-color: #000000;
        text-color: #000000;
        font-family: verdana,arial,sans-serif;
        font-size: 10px;
        margin: 0px;
    }

    .regText {
        font-family: verdana,arial,sans-serif;
        font-size: 10px;
    }

    .grayBox {
        background-color: #C8C5B4;
        font-family: verdana,arial,sans-serif;
        font-size: 10px;
    }
--></style>
</head>
<body>
<CENTER>
""")
        fp.close()

        fp = open(self.dirname + "/index.html", "w")
        fp.write("<TITLE>%s</TITLE>" % self.name)
        fp.write("""
<FRAMESET COLS="250,*" BORDER=0>
    <FRAME SRC="contents.html" NAME="contents">
    <FRAME SRC="blank.html" NAME="mainwin">
</FRAMESET>""")
        fp.close()

    def _link(self, href, text):
        s = '<TD ALIGN=LEFT class="regText">'
        s += '<A HREF="%s" TARGET="mainwin">%s</A>' % (href, text)
        s += '</TD>\n'
        return s

    def write(self, name, guipage, type='page'):
        """Currently this method logs 2 types of pages:
            page log: log guipage.html
            form log: log each form in guipage.forms
        """
        assert type in ('page', 'form')

        if name.strip() == '': name = 'noname'

        if self.guipage != guipage:  # new page?
            self.guipage = guipage
            self.written.append(name)
        sysname = name + ".%d" % self.written.count(name)
        self.page_name = name

        if type == 'page':
            # add URL to html page
            url_html = '\nRequestURL(%s):' % (sysname) + guipage.URL + '<hr>\n'
            html = re.sub('<body>', '<body>' + url_html, guipage.html, re.IGNORECASE)

            if guipage.charset:  # if Unicode, encode it prior to writing to file
                assert isinstance(html, types.UnicodeType)
                html = html.encode(guipage.charset)

            # write page
            fp = open(os.path.join(self.dirname, sysname + "_page.html"), "w")
            fp.write(html)
            fp.close()

            # write contents.html
            fp = open(os.path.join(self.dirname, "contents.html"), "a")
            fp.write("<i><b><A HREF='%s' TARGET='mainwin'>%s</a></b></i><br>\n" % (sysname + "_page.html", sysname))
            fp.close()


        elif type == 'form':
            # write form
            fp = open(os.path.join(self.dirname, sysname + "_form.html"), "w")
            fp.write('<PRE>SubmitURL(%s):' % (sysname) + guipage.URLSubmit + "</PRE><HR>\n")
            formcount = 0
            for form in guipage.forms:
                fp.write("<i>%s Form%d</i><br><pre>\n" % (sysname, formcount))
                fp.write(cgi.escape(str(form), 1))
                fp.write("\n</pre><br>\n")
                formcount += 1
            fp.close()

            # write contents.html
            fp = open(os.path.join(self.dirname, "contents.html"), "a")
            fp.write("<A HREF='%s_form.html' TARGET='mainwin'>Submit %s</A>\n" % (sysname, sysname))
            fp.write("<br>\n")
            fp.close()

        if len(self.written) > self.maxsize:
            raise SizeError

    def rotate(self):
        return rotate(self)

    def close(self):
        pass


def get_global_logs():
    global __globalGuiLogs
    return __globalGuiLogs


class GlobalGuiLogInterface:
    """GlobalGuiLogInterface(name, [maxsize=1000], [maxsave=9], [source=None])
    Similar in functionality to a ManagedLog, except that logs are written through the GlobalLog which manages log entries from multiple sources"""

    def __init__(self, name, maxsize=1000, maxsave=9, source=None):
        self.source = source
        self.name = name
        gl = get_global_logs()
        # if there's already a global log with this name, hook into that log
        # otherwise, create a new global log with the specified name
        if gl.has_key(name):
            self._gl = gl[name]
        else:
            if os.path.isdir(name):
                shiftlogs(name, maxsave)
            self._gl = GlobalGuiLog(name, maxsize, maxsave)
            gl[name] = self._gl

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__, self._gl.name, self._gl.maxsize, self.maxsave)

    def write(self, name, guipage, type='page'):
        self._gl.write(name, guipage, type)

    def written(self):
        return self._gl.written()

    def close(self):
        if self._gl is not None:
            self._gl.close()
            self._gl = None
            # delete the log from __globalGuiLogs
            gl = get_global_logs()
            if gl.has_key(self.name):
                del gl[self.name]

    def rotate(self):
        self._gl.rotate()

    # auto-delegate remaining methods (but you should not read or seek an open
    # log file).
    def __getattr__(self, name):
        return getattr(self._gl, name)


class GlobalGuiLog:
    """GlobalLog(name, [maxsize=1000], [maxsave=9])
    Opens a new (possibly shared) file object. After writing <maxsize> pages, the log directory will be rotated."""

    def __init__(self, name, maxsize=1000, maxsave=9):
        self._gl = GuiLog(name, maxsize)
        self.maxsave = maxsave
        self.name = name

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__, self._gl.name, self._gl.maxsize, self.maxsave)

    def write(self, name, guipage, type='page'):
        try:
            self._gl.write(name, guipage, type)
        except SizeError:
            self._gl = rotate(self._gl, self.maxsave)

    def written(self):
        return len(self._gl.written)

    def close(self):
        if self._gl is not None:
            self._gl.close()
            self._gl = None

    def rotate(self):
        self._gl = rotate(self._gl, self.maxsave)

    # auto-delegate remaining methods (but you should not read or seek an open
    # log file).
    def __getattr__(self, name):
        return getattr(self._gl, name)


def rotate(fileobj, maxsave=9):
    name = fileobj.name
    maxsize = fileobj.maxsize
    fileobj.close()
    shiftlogs(name, maxsave)
    return GuiLog(name, maxsize)


def shiftlogs(basename, maxsave):
    topname = "%s.%d" % (basename, maxsave)
    if os.path.isdir(topname):
        for filename in os.listdir(topname):
            try:
                os.unlink(os.path.join(topname, filename))
            except:
                pass
        os.rmdir(topname)

    for i in range(maxsave, 0, -1):
        oldname = "%s.%d" % (basename, i)
        newname = "%s.%d" % (basename, i + 1)
        try:
            os.rename(oldname, newname)
        except OSError:
            pass
    try:
        os.rename(basename, "%s.1" % (basename))
    except OSError:
        pass


"""
def open(name, mode="w"):
    return LogFile(name, mode)


def writelog(logobj, data):
    try:
        logobj.write(data)
    except SizeError:
        return rotate(logobj)
    else:
        return logobj


def _test(argv):
    basename = "/var/tmp/logfile_test"
    lf = ManagedLog(basename, maxsize=1000)
    for i in xrange(10000):
        lf.write("testing %i (%d) %s\n" % (i, lf.written(), string.ascii_letters))
    lf.note("test note")
    lf.close()

if __name__ == "__main__":
    import sys, string
    _test(sys.argv)



"""
