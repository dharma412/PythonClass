""" qabdbase.py: Take all common components of qabackdoors
    for different platforms and put them here.
"""

# $Id: //prod/main/sarf_centos/testlib/sal/net/services/qabdbase.py#1 $

# Python imports
import htmllib
import formatter
import urllib
import re
import os

# IAF imports
from sal.containers import odict
import sal.net.sshlib

# Globals
DEFAULTPORT = 8123


class Getter(htmllib.HTMLParser):
    """Download HTML from a URL.
    This base class is used by PreGetter and ParaGetter"""

    def _reset(self):
        """Reset Getter state"""
        self.state = 0
        self._text = []

    def parse(self, url):
        """Open URL via socket. Read contents from socket until EOF.
        Data is passed to HTML parser and processed.
        Return None"""
        fo = urllib.urlopen(url)
        self.parseFile(fo)
        fo.close()

    def parseFile(self, fo):
        """Read all data from file object until no more data is available.
        Pass data to HTMLParser's feed() method.
        Return None"""
        data = fo.read(16384)
        while data:
            self.feed(data)
            data = fo.read(16384)


class PreGetter(Getter):
    """Process <pre></pre> html tags.

    Populate self._text with data enclosed by <pre> start/end tags.
    Call self.callback() with self._text as argument when </pre>
    end tag is encountered."""

    def __init__(self, callback, verbose=0):
        fmt = formatter.AbstractFormatter(formatter.NullWriter())
        htmllib.HTMLParser.__init__(self, fmt, verbose)
        self.callback = callback
        self._reset()

    def handle_starttag(self, tag, meth, attrs):
        """Handle <pre> start tag."""
        if tag == "pre":
            self.state = 1

    def handle_data(self, data):
        """Handle <pre> data."""
        if self.state == 1:
            self._text.append(data)

    def handle_endtag(self, tag, meth):
        """Handle </pre> end tag."""
        if tag == "pre" and self.state == 1:
            self.callback("".join(self._text))
            self._reset()


class ParaGetter(Getter):
    """Get data after <p> tag"""

    def do_p(self, attrs):
        """Method called when <p> start tag is encountered."""
        self.formatter.add_flowing_data("\n")
        try:
            self._paras.append(self.formatter.getvalue())
        except AttributeError:
            self._paras = []
            self._paras.append(self.formatter.getvalue())

    def getvalue(self):
        """Return paragraph as a string"""
        return "".join(self._paras)


class ParaGetterFormatter(formatter.NullFormatter):
    """Instance of this formatter class passed to ParaGetter"""

    def add_flowing_data(self, text):
        """Appened text to self._text"""
        try:
            self._text += text
        except AttributeError:
            self._text = text

    def getvalue(self):
        """Return self._text. Clear self._text"""
        rv = self._text
        self._text = ""
        return rv


class TextGetter(object):
    """Same interface as HTML parser, but just save the text. use for text/plain
    message content.  """

    def __init__(self, callback, verbose=0):
        self._callback = callback
        self._text = ""

    def close(self):
        self._callback(self._text)

    def parse(self, url):
        fo = urllib.urlopen(url)
        self.parseFile(fo)
        fo.close()

    def parseFile(self, fo):
        s = []
        data = fo.read(16384)
        while data:
            s.append(data)
            data = fo.read(16384)
        self._text = "".join(s)


class QABackdoorBase(object):
    """QABackdoorBase(hostname, [port])
    Interface to the QA backboor process on the DUT (which is really an
    HTTP/HTML server).  Supply a host name and optional port number.
    """

    def __init__(self, hostname, port=None):
        self._hostname = hostname  # save for debugging (otherwise not used)
        if not port:
            port = DEFAULTPORT
        self.base = "http://%s:%d/" % (hostname, port)
        self._pretext = ""

    def gethostname(self):
        return self._hostname

    def _callback(self, text):
        """PreGetter() and TextGetter() use this callback to pass text
        back to QABackdoor() instance"""
        self._pretext = text

    def _get(self, page):
        """Get <pre> text from 'page'"""
        getter = PreGetter(self._callback)
        getter.parse("%s%s" % (self.base, page))
        getter.close()

    def _get_text(self, page):
        """Get ascii non-html text from 'page'"""
        getter = TextGetter(self._callback)
        getter.parse("%s%s" % (self.base, page))
        getter.close()

    def _get_para(self, page):
        """Get <p> text from 'page'"""
        fmt = ParaGetterFormatter()
        getter = ParaGetter(fmt)
        getter.parse("%s%s" % (self.base, page))
        getter.close()
        rv = getter.getvalue()
        return rv

    def top(self):
        """Top - toplevel page."""
        return self._get_para("")

    def get_info(self):
        """ Return dictionary with information about the box.

        List of keys:
            - host
            - model
            - release_tag
            - version
            - build_date
            - serial_number

        Examples:
        | ${info}= | QA Backdoor Get Info |
        | ${version}= | Get From Dictionary | ${info} | version |
        """
        top = self.top()

        host = model = release_tag = version = build_date = serial_number = 'unknown'

        try:
            host = re.findall('Backdoor Server for (.*)\.', top)[0]
        except:
            pass
        try:
            model = re.findall('model: (.*)', top)[0]
        except:
            pass
        try:
            release_tag = re.findall('release tag: (.*)', top)[0]
        except:
            pass
        try:
            version = re.findall('current version: (.*)', top)[0]
        except:
            pass
        try:
            build_date = re.findall('build date: (.*)', top)[0]
        except:
            pass
        try:
            serial_number = re.findall('serial number: (.*)', top)[0]
        except:
            pass

        info = odict.odict()
        info['host'] = host
        info['model'] = model
        info['release_tag'] = release_tag
        info['version'] = version
        info['build_date'] = build_date
        info['serial_number'] = serial_number
        return info

    def processes(self):
        """Processes - return report of processes."""
        self._get("processes")
        return self._pretext

    def stop_application_manager(self):
        """not implemented"""
        raise NotImplementedError

    def start_application_manager(self):
        """not implemented"""
        raise NotImplementedError

    def kill_all_applications(self):
        """not implemented"""
        raise NotImplementedError

    def reboot(self):
        """Reboot - reboots the box."""
        return self._get_para("commit_reboot")

    def netstat_active_sockets(self):
        """Netstat_active_sockets - report of active sockets."""
        self._get("netstat_active_sockets")
        return self._pretext

    def netstat_routes(self):
        """Netstat_routes - report of active routes."""
        self._get("netstat_routes")
        return self._pretext

    def netstat_buffers(self):
        """Netstat_buffers - netstat -m. Show statistics recorded
        by the memory management routines"""

        self._get("netstat_buffers")
        return self._pretext

    def current_interface_config(self):
        """Current_interface_config - report of current active interfaces."""
        self._get("current_interface_config")
        return self._pretext

    def list_open_files(self):
        """List_open_files - report of all open files."""
        self._get("list_open_files")
        return self._pretext

    def browse_logs(self, d, f, lines=25, offset=-1):
        """browse_logs show log file <f> in directory <d>"""
        self._get("browse_logs?dir=%s&file=%s&lines=%s&offset=%s" % (d, f,
                                                                     lines, offset))
        return self._pretext

    def whole_log(self, d, f, do_check=True):
        """whole_log returns entire log file <f> in directory <d>"""
        self._get_text("raw/whole_log?dir=%s&file=%s" % (d, f))
        return self._pretext

    def purge_logs(self):
        """not implemented"""
        raise NotImplementedError

    def cli_status(self):
        """Status message identical to CLI "status" command."""
        self._get("cli_status")
        return self._pretext

    def reset_counters(self):
        """Reset counters on device."""
        self._get("reset_counters")
        return self._pretext

    def config(self, d, f):
        """Show config file <f> in directory <d>.

        Parameters:
            - `d`: name of the config directory
            - `f`: config filename

        Examples:
        | ${config}= | QA Backdoor Config | avc.command_manager | data.cfg |
        | Log | ${config} |
        """
        self._get("config?dir=%s&file=%s" % (d, f))
        return self._pretext

    def parse_config(self, d, f='data.cfg'):
        """Like config(). Get data.cfg formatted file <f> in
        directory <d> convert to DataParse object for easy
        config setting access."""
        from utils.DataParse import DataParse
        self._get_text("raw/whole_config?dir=%s&file=%s" % (d, f))
        cfg = DataParse.parse_config(self._pretext)
        return cfg  # access like a dict. eg. cfg[cfg_setting_name].value

    def backup_config(self):
        """not implemented"""
        raise NotImplementedError

    def restore_config(self):
        """not implemented"""
        raise NotImplementedError

    def download_config(self):
        """Config - download /usr/godspeed/config dir as a tarfile"""
        self._get_text("raw/commit_download_config")
        return self._pretext

    def download_xml_config(self):
        """config - show xml formatted config file """
        self._get_text("raw/commit_download_xml_config")
        return self._pretext

    def rebuild_queue(self):
        """not implemented"""
        raise NotImplementedError

    def ssh_public_keys(self):
        """not implemented"""
        raise NotImplementedError

    def redo_netinstall(self):
        """redo_netinstall - forces a netinstall."""
        self._get("commit_redo_netinstall")
        return self._pretext

    def set_qlog_buffer_size(self, buffer_size=0):
        """Set the log buffer size.
        When buffer_size is zero, appliance writes immediately to the log
        files without buffering. (no need to wait for log files to update.)
        On success returned string contains: set qlog buffer size to <bsize>."""
        self._get_text("commit_set_qlog_buffer_size?buffer_size=" +
                       str(buffer_size))
        m = re.search('.*(set qlog.*to \d+)', self._pretext)
        if m:
            return m.group(1)
        else:
            return self._pretext

    def replace_keys(self, keys):
        """Rewrite .ssh/authorized keys file on appliance.

        Parameters:
            - `keys`: a string of new line character separated keys

        Examples:
        | ${key1}= | Set Variable | ssh-rsa AAAAB3Nza...v/7h3MKPEQoxp7qLM8w== |
        | ${key2}= | Set Variable | ssh-rsa BBBBB3Nza...v/7h3MKPEQoxp7qLM8w== |
        | QA Backdoor Replace Keys | ${key1}\\n${key2} |
        """
        data = {'user': 'root',
                'authorized_keys': keys}
        args = urllib.urlencode(data)
        self._get_text("commit_ssh_authorized_keys?" + args)

    def add_key(self, key):
        """Append a public key to .ssh/authorized_keys file on appliance.

        Parameters:
            - `key`: string with public key

        Examples:
        | QA Backdoor Add Key | ssh-rsa AAAAB3Nza...v/7h3MKPEQoxp7qLM8w== |
        """
        keys = self.get_keys().strip()
        if key in keys.split('\n'):
            # key already exists on appliance. Do nothing.
            return
        keys += '\n' + key
        self.replace_keys(keys)

    def add_iaf_key(self):
        """Add iaf user's public key to .ssh/authorized_keys file on appliance"""
        public_iaf_key = sal.net.sshlib.iaf_key.public_key
        if not os.access(public_iaf_key, os.R_OK):
            raise RuntimeError, 'Error: %s not readable' % public_iaf_key
        iaf_key = open(public_iaf_key).read().strip()
        self.add_key(iaf_key)

    def get_keys(self):
        """Return contents of .ssh/authorized_keys file on appliance.

        Examples:
        | QA Backdoor Get Keys |
        """
        import BeautifulSoup
        self._get_text("raw/ssh_authorized_keys?user=root")
        if re.search('Error code 404', self._pretext):
            raise RuntimeError, "Can't set authorized keys on this appliance"
        bs = BeautifulSoup.BeautifulSoup(self._pretext)
        auth_keys = bs.first('textarea').contents[0]
        return str(auth_keys)


def get_qabackdoor(host, port=None):
    return QABackdoorBase(host, port)
