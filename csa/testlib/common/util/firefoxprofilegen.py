#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/util/firefoxprofilegen.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from __future__ import absolute_import

import os
import pexpect
import re
import shutil
import socket
import subprocess
import tempfile
import time

# SARF imports
from common.logging import Logger
import common.Variables

VAR_TMP_DIR = '/var/tmp'
# These keys can be found in cert_override.txt on the client side once the exceptions are added for each wsa cert on the browser
WSA71_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\t5A:8C:03:BF:19:F8:A0:AA:53:75:94:36:49:A1:BF:2F:B9:B7:77:59:A4:47:AE:07:1A:7C:8F:1E:8D:75:45:A0\tMU\tAAAAAAAAAAAAAAABAAAAiAEwgYUxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxp  Zm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xHzAdBgNVBAoTFklyb25Qb3J0IFN5  c3RlbXMsIEluYy4xLDAqBgNVBAMTI0lyb25Qb3J0IEFwcGxpYW5jZSBEZW1vIENl  cnRpZmljYXRl")
WSA75_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\tBC:F1:C7:77:8D:D3:F7:A8:53:8F:49:FF:24:CB:99:42:5B:BF:AA:9B:D7:BB:43:2B:2D:D7:0D:5B:40:67:E6:C0\tMU\tAAAAAAAAAAAAAAABAAAAmAEwgZUxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxp  Zm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xHDAaBgNVBAoTE0Npc2NvIFN5c3Rl  bXMsIEluYy4xPzA9BgNVBAMTNkNpc2NvIElyb25Qb3J0IFdlYiBTZWN1cml0eSBB  cHBsaWFuY2UgRGVtbyBDZXJ0aWZpY2F0ZQ==")
SMA_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\t30:D6:48:C3:31:DD:0F:45:46:0B:F5:4B:5C:63:31:99:B0:94:FC:F9:35:D5:A1:37:38:B1:94:8F:40:9C:38:01\tMU\tAAAAAAAAAAAAAAAJAAAAhAC8f4FZHKufuzCBgTELMAkGA1UEBhMCVVMxEzARBgNV  BAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEbMBkGA1UEChMSQ2lz  Y28gU3lzdGVtcywgSW5jMSwwKgYDVQQDEyNJcm9uUG9ydCBBcHBsaWFuY2UgRGVt  byBDZXJ0aWZpY2F0ZQ==")
ESA_KEY = (
    "AAAAAAAAAAAAAAAJAAAAfwDfpe19JFPKaTB9MQswCQYDVQQGEwJVUzETMBEGA1UE  CBMKQ2FsaWZvcm5pYTERMA8GA1UEBxMIU2FuIEpvc2UxGzAZBgNVBAoTEkNpc2Nv  IFN5c3RlbXMsIEluYzEpMCcGA1UEAxMgQ2lzY28gQXBwbGlhbmNlIERlbW8gQ2Vy  dGlmaWNhdGU=")
WSA77_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\tF0:6D:66:A2:B1:5A:3E:C4:97:5C:30:C1:DF:C8:15:FE:84:34:A6:53:15:D4:B4:63:09:4A:EE:B4:79:F5:D0:CA\tMU\tAAAAAAAAAAAAAAABAAAAlAEwgZExCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxp  Zm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xJTAjBgNVBAoTHENpc2NvIElyb25Q  b3J0IFN5c3RlbXMsIEluYy4xMjAwBgNVBAMTKUNpc2NvIElyb25Qb3J0IEFwcGxp  YW5jZSBEZW1vIENlcnRpZmljYXRl")
WSA80_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\tF0:6D:66:A2:B1:5A:3E:C4:97:5C:30:C1:DF:C8:15:FE:84:34:A6:53:15:D4:B4:63:09:4A:EE:B4:79:F5:D0:CA\tMU\tAAAAAAAAAAAAAAABAAAAlAEwgZExCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxp  Zm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xJTAjBgNVBAoTHENpc2NvIElyb25Q  b3J0IFN5c3RlbXMsIEluYy4xMjAwBgNVBAMTKUNpc2NvIElyb25Qb3J0IEFwcGxp  YW5jZSBEZW1vIENlcnRpZmljYXRl")
WSA85_KEY = (
    "%s\tOID.2.16.840.1.101.3.4.2.1\tE4:18:70:31:A6:9D:0D:59:BE:D5:68:2C:7C:CE:E2:40:AC:4D:CD:BA:81:07:72:F1:BD:49:B0:AE:03:76:34:3D\tMU\tAAAAAAAAAAAAAAABAAAAfwEwfTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlm  b3JuaWExETAPBgNVBAcTCFNhbiBKb3NlMRswGQYDVQQKExJDaXNjbyBTeXN0ZW1z  LCBJbmMxKTAnBgNVBAMTIENpc2NvIEFwcGxpYW5jZSBEZW1vIENlcnRpZmljYXRl")


class FirefoxProfile(Logger):
    """ Library for Firefox profile management.

    Main purpose of this library is overriding of HTTPS certificates to avoid
    HTTPS certificate exception during the initial login through GUI.
    """

    def __init__(self, ff_profile_dir=None):
        self.directory = ff_profile_dir

    def generate(self):
        """ Generate new empty Firefox profile and return its directory
        location.
        """
        # create new directory for Firefox profile
        self.directory = ('%s/customProfileDir%s' % (VAR_TMP_DIR, time.time()))
        os.mkdir(self.directory)

        # create new cert8.db database
        self._create_new_cert8_db()

        self._enable_ipv6_config()

        self._setup_firefox_prefs()

        self._debug('Generated Firefox Profile directory: %s' % self.directory)
        return self.directory

    def remove(self):
        """ Removed the Firefox profile directory. """

        if self.directory:
            self._debug('Removed Firefox profile directory: %s'
                        % self.directory)
            if os.path.exists(self.directory):
                shutil.rmtree(self.directory)
            # set to None, directory is deleted
            self.directory = None

    def add_certificate(self, hostname, version, port):
        """ Add certificate for the specified hostname and port.

        Parameters:
            - `hostname`: hostname of the appliance under test.
            - `version` : version of the libraries used for appliance.
                          e.g.  coeus75, zeus78, etc.
            - `port`    : HTTPS port.  Defaulted to 8443.
        """
        # get firefox magic key
        if version.startswith('zeus') or version.startswith('sma'):
            ff_magic_key = SMA_KEY
        elif version.startswith('phoebe') or 'phoebe' in version:
            cert_signature = self._get_cert_signature(hostname, port)
            ff_magic_key = ("%s\tOID.2.16.840.1.101.3.4.2.1\t" + cert_signature + "\tMU\t" + ESA_KEY)
        elif version.startswith('coeus'):
            if version < 'coeus75':
                ff_magic_key = WSA71_KEY
            elif version < 'coeus77':
                ff_magic_key = WSA75_KEY
            elif version <= 'coeus775':
                # Penglai(Virtual) and Pikespeak have the same keys
                ff_magic_key = WSA77_KEY
            elif version < 'coeus85':
                ff_magic_key = WSA80_KEY
            else:
                ff_magic_key = WSA85_KEY
        else:
            raise Exception('Unrecognized asyncos version: %s' % (version,))

        # generate initial certificate
        certificate = self._fetch_host_cert(hostname, port)
        self._add_cert_to_cert8_db(hostname, certificate)
        self._write_firefox_cert_override(
            "%s:%d" % (hostname, port), ff_magic_key)

        # add certificate exception for IP address
        # after SSW on SMA user is redirected to IP address
        ip = socket.gethostbyname(hostname)
        self._write_firefox_cert_override(
            "%s:%d" % (ip, port), ff_magic_key)

    def _get_cert_signature(self, host, port):
        cmd = "openssl s_client -connect %s:%d < /dev/null 2>/dev/null |" % (host, port) + \
              "openssl x509 -sha256 -fingerprint -noout -in /dev/stdin"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stdout.read()
        errors = p.stderr.read()
        if output:
            return output.strip().split("=")[-1]
        else:
            raise RuntimeError, \
                "Failed to get certificate signature:" \
                "%s\nCommand Output:\n%s\nCommand Errors:\n%s" % \
                (cmd, output, errors)

    def _write_firefox_cert_override(self, host, key):
        """ Output a key to cert_override.txt, inserting a given hostname. """
        path_to_file = os.path.join(self.directory, 'cert_override.txt')
        print "Host:", host, "Key:", key
        if os.path.exists(path_to_file):
            # read into memory current records then replace or add
            # one for needed host
            current_keys = []
            with open(path_to_file) as key_file:
                current_keys = [line for line in key_file.readlines()
                                if line.strip() != '']
            with open(path_to_file, 'w') as key_file:
                no_key = True
                for current_key in current_keys:
                    if no_key and current_key.startswith(host):
                        # replace current key with new one
                        print >> key_file, key % host
                        no_key = False
                    else:
                        # just add rest of current keys
                        print >> key_file, current_key
                if no_key:
                    # add key such as there is no such key
                    print >> key_file, key % host
        else:
            # just create new file with given key
            with open(path_to_file, 'w') as key_file:
                print >> key_file, key % host

    def _add_cert_to_cert8_db(self, name, cert):
        """ Add a certificate (using name as a nickname) to a cert8.db file in a
            given directory.
        """
        tmp_fds, filename = tempfile.mkstemp(text=True)
        filehdl = os.fdopen(tmp_fds, 'w+')
        filehdl.write(cert)
        filehdl.close()
        cmd = 'certutil -A -n %s -t ",," -i %s -d %s' \
              % (name, filename, self.directory)
        self._debug(cmd)
        retcode = subprocess.call(cmd, shell=True)
        os.remove(filename)

    def _create_new_cert8_db(self):
        """ Use certutil to create a new, empty cert8.db database. """
        create_db_cmd = "certutil -N -d %s" % self.directory

        # Use pexpect.spawn because certutil deals with the controlling
        # terminal only. (subprocess doesn't work in this case)
        self._debug(create_db_cmd)
        certutil_proc = pexpect.spawn(create_db_cmd)
        certutil_proc.expect("Enter new password:")
        certutil_proc.write("\n")
        certutil_proc.expect("Re-enter password:")
        certutil_proc.write("\n")
        certutil_proc.close()

    def _fetch_host_cert(self, host, port):
        """ Return the certificate for a given host/port combo."""
        begin_cert = "-----BEGIN CERTIFICATE-----"
        end_cert = "-----END CERTIFICATE-----"

        cmd = "openssl s_client -connect %s:%d < /dev/null" % (host, port)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        output = p.stdout.read()
        errors = p.stderr.read()
        if begin_cert not in output or end_cert not in output:
            raise RuntimeError, \
                "Didn't seem to get a certificate from openssl command: " \
                "%s\nCommand Output:\n%s\nCommand Errors:\n%s" % \
                (cmd, output, errors)
        return output[output.find(begin_cert):output.find(end_cert) + 25]

    def _enable_ipv6_config(self):
        """ Add user preference for ipv6 dns config."""
        self.prefs_js_path = os.path.join(self.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')
        try:
            prefs_js.write('# Mozilla User IPv6 Preferences\n')
            prefs_js.write('user_pref("network.dns.disableIPv6", true);\n')
        finally:
            prefs_js.close()

    def _setup_firefox_prefs(self):
        """
        Add custom settings to firefox profile
        The settings are specified in variables ${firefox_prefs_XXX}
        Example:
            ${firefox_prefs_network.proxy.type} = 0
            ${firefox_prefs_network.proxy.share_proxy_settings} = true
            ${firefox_prefs_network.proxy.socks} = squid.home-server
            ${firefox_prefs_network.proxy.socks_port} = 3128

            The following lines are added to prefs.js:
                user_pref("network.proxy.type", 0);
                user_pref("network.proxy.share_proxy_settings", true);
                user_pref("network.proxy.socks", "squid.home-server");
                user_pref("network.proxy.socks_port", 3128);
        """
        custom_settings = {}
        pattern = "${firefox_prefs_"
        pattern_len = len(pattern)

        variables = common.Variables.get_variables()
        for item in variables.keys():
            if item.startswith(pattern):
                custom_settings[item[pattern_len: -1]] = variables[item]
        if custom_settings == {}: return

        self.prefs_js_path = os.path.join(self.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')
        try:
            prefs_js.write('# Adding custom setting\n')
            self._info('# Adding custom setting')
            for key in custom_settings.keys():
                value = custom_settings[key]
                if value.lower() in ('true', 'false'):
                    value = value.lower()
                else:
                    try:
                        if not type(eval(value)) in (int, float):
                            raise
                    except:
                        value = '"' + value + '"'
                prefs_js.write('user_pref("%s", %s);\n' % (key, value))
                self._info('user_pref("%s", %s);' % (key, value))
        finally:
            prefs_js.close()
