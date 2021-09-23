#!/usr/bin/env python

# Import Python modules
import base64
import commands
import datetime
import json
import pprint
import random
import re
import socket
import time
import SSHLibrary

# Import SARF modules
from common.util.utilcommon import UtilCommon
from common.util.backdoor_interface import BackdoorInterface
from common.util.misc import Misc

from credentials import TESTUSER,\
            TESTUSER_PASSWORD, \
                RTESTUSER,\
                    RTESTUSER_PASSWORD

pp = pprint.PrettyPrinter(indent=4)

class Misc(BackdoorInterface, UtilCommon, Misc):
    """
    SMA miscellenious keywords (release specific)
    """

    def get_keyword_names(self):
        return [
            'threatgrid_rekey_esa_sma',
            'threatgrid_rekey_wsa_sma',
        ]

    def threatgrid_rekey_esa_sma(self):
        tg_url = 'https://panacea.threatgrid.com'
        tg_register_uri = '/private/1/key/register'
        tg_rekey_uri = '/private/1/rekey'
        esa_code = '01'
        esa_serial = '00221926E3BF-D8VFLJ1'
        esa_model = 'C660'
        padding = '0000000000000000000000000000000'
        count = '20'
        random_val = str(random.randint(1000, 9999))

        tg_register_url = tg_url + tg_register_uri + '?apikey=' \
                          + esa_code + '_' + esa_serial + '_' + esa_model \
                          + '_' + random_val + padding + '&count=' + count
        self._info('Threatgrid regestration URL: %s' % tg_register_url)
        tg_rekey_url = tg_url + tg_rekey_uri + ' --data "apikey=' \
                       + esa_code + '_' + esa_serial + '_' + esa_model \
                       + '_' + random_val + padding + '"'
        self._info('Threatgrid Rekey URL: %s' % tg_rekey_url)

        reg_out = commands.getoutput('curl -vv -k -X PUT "' + tg_register_url + '"')
        self._debug(reg_out)

        rekey_out = commands.getoutput('curl -vv -k -X POST ' + tg_rekey_url)
        self._debug(rekey_out)

        tg_new_apikey = re.search(r'{\"apikey\":\"(\S+)\"}', rekey_out, re.I).group(1)
        self._info('New Threatgrid API key: %s' % tg_new_apikey)

        #self.copy_file_to_dut('/tmp/analysis.key', '/data/fire_amp/db/preserve/')
        #self.run_on_dut('/data/bin/heimdall_svc -r thirdparty')
        host_ip=self._get_parameter("${CLIENT_IP}")
        host_sma=self._get_parameter("${SMA}")
        host_esa=self._get_parameter("${ESA}")
        ssh = SSHLibrary.SSHLibrary()
        copy_command="echo %s %s > /tmp/analysis.key" % (tg_url, tg_new_apikey)
        try:
            ssh.open_connection(host=host_ip, prompt="$",
                timeout=120)

            ssh.login(username = 'rtestuser', password = 'ironport')
            ssh.write(text = copy_command)
        finally:
            ssh.close_connection()
        self.scp(
        recursive='',
 #      from_parameters
            from_host = host_ip,
            from_user = RTESTUSER,
            from_password = RTESTUSER_PASSWORD,
            from_prompt = '$',
            from_location = '/tmp/analysis.key',

 #      to_parameters
            to_host = host_esa,
            to_user = RTESTUSER,
            to_password = RTESTUSER_PASSWORD,
            to_location = '/data/fire_amp/db/preserve/',
            )
        self.scp(
        recursive='',
 #      from_parameters
            from_host = host_ip,
            from_user = RTESTUSER,
            from_password = RTESTUSER_PASSWORD,
            from_prompt = '$',
            from_location = '/tmp/analysis.key',

 #      to_parameters
            to_host = host_sma,
            to_user = RTESTUSER,
            to_password = RTESTUSER_PASSWORD,
            to_location = '/data/fireamp/',
            )
        self.run_on_dut('/data/bin/heimdall_svc -r thirdparty', host_esa)

    def threatgrid_rekey_wsa_sma(self):
        tg_url = 'https://panacea.threatgrid.com'
        tg_register_uri = '/private/1/key/register'
        tg_rekey_uri = '/private/1/rekey'
        esa_code = '02'
        esa_serial = '00221926E3BF-D8VFLJ1'
        esa_model = 'C660'
        padding = '0000000000000000000000000000000'
        count = '20'
        random_val = str(random.randint(1000, 9999))

        tg_register_url = tg_url + tg_register_uri + '?apikey=' \
                          + esa_code + '_' + esa_serial + '_' + esa_model \
                          + '_' + random_val + padding + '&count=' + count
        self._info('Threatgrid regestration URL: %s' % tg_register_url)
        tg_rekey_url = tg_url + tg_rekey_uri + ' --data "apikey=' \
                      + esa_code + '_' + esa_serial + '_' + esa_model \
                      + '_' + random_val + padding + '"'
        self._info('Threatgrid Rekey URL: %s' % tg_rekey_url)




        host_ip=self._get_parameter("${CLIENT_IP}")
        host_sma=self._get_parameter("${SMA}")
        host_wsa=self._get_parameter("${WSA}")
        ssh = SSHLibrary.SSHLibrary()
        try:
           ssh.open_connection(host=host_ip, prompt="$",
                                 timeout=120)

           ssh.login(username = RTESTUSER, password = RTESTUSER_PASSWORD)
           ssh.execute_command('curl -vv -k -X PUT "' + tg_register_url + '"')
           rekey_out=ssh.execute_command('curl -vv -k -X POST ' + tg_rekey_url)
           tg_new_apikey = re.search(r'{\"apikey\":\"(\S+)\"}', rekey_out, re.I).group(1)
           self._info('New Threatgrid API key: %s' % tg_new_apikey)
           ssh.execute_command("echo %s %s > /tmp/analysis.key" % (tg_url, tg_new_apikey))
           self.scp(
                    recursive='',
           #      from_parameters
                   from_host = host_ip,
                   from_user = RTESTUSER,
                   from_password = RTESTUSER_PASSWORD,
                   from_prompt = '#',
                   from_location = '/tmp/analysis.key',
           #      to_parameters
                   to_host = host_wsa,
                   to_user = RTESTUSER,
                   to_password = RTESTUSER_PASSWORD,
                   to_location = '/data/fire_amp/db/preserve/',
                   )
        finally:
           ssh.close_connection()
        time.sleep(30)
        self.run_on_dut('/data/bin/heimdall_svc -r thirdparty', host_wsa)