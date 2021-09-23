#!/usr/bin/env python

# Import Python modules
from bs4 import BeautifulSoup
import commands
import random
import re

# Import SARF modules
from common.util.utilcommon import UtilCommon
from common.util.backdoor_interface import BackdoorInterface
from common.util.misc import Misc


class Misc(BackdoorInterface, UtilCommon, Misc):
    """
    ESA miscellenious keywords (release specific)
    """

    def get_keyword_names(self):
        return [
            'get_pvo_minimum_allowed_quota',
            'threatgrid_rekey_esa',
            'get_messages_info_from_quarantine_notification',
        ]

    def get_pvo_minimum_allowed_quota(self, dut_model):
        code_list = (
            'import model_features',
            "print '@@@', model_features.baseline_" \
            + dut_model \
            + ".quarantine_vof_space, '@@@'"
        )

        output = self.backdoor_run(app_name='hermes', code_list=code_list)
        self._info('Dut backdoor run output:\n%s' % output)
        pvo_min_allowed_quota = re.search(r'@@@\s+(\d+)\s+@@@', output).group(1)
        pvo_min_allowed_quota = int(int(pvo_min_allowed_quota) / 1024)

        return pvo_min_allowed_quota

    def threatgrid_rekey_esa(self):
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

        commands.getoutput('echo %s %s > /tmp/analysis.key' % (tg_url, tg_new_apikey))

        self.copy_file_to_dut('/tmp/analysis.key', '/data/fire_amp/db/preserve/')
        self.run_on_dut('/data/bin/heimdall_svc -r thirdparty')

    def get_messages_info_from_quarantine_notification(self,
                                                       notification_email_body=None, notification_format='HTML'):

        quar_messages = []
        if notification_format == 'HTML' or notification_format == 'HTML/Text':
            soup = BeautifulSoup(notification_email_body, 'html.parser')
            table = soup.find('div', id='content')
            table_rows = table.find_all('tr')
            for tr in table_rows:
                table_columns = tr.find_all('td')
                if len(table_columns) > 1:
                    href = table_columns[2].a
                    regex = r'href\=\"(http\S+)\">' + table_columns[2].text.strip() + '<'
                    link = re.search(regex, str(href)).group(1)
                    quar_messages.append(
                        {
                            'action': table_columns[0].text.strip(),
                            'from': table_columns[1].text.strip(),
                            'subject': table_columns[2].text.strip(),
                            'date': table_columns[3].text.strip(),
                            'link': link.strip(),
                        }
                    )
                else:
                    continue
        else:
            regex = """New Quarantine Messages -+\\n\\n\\s*(.*)\\n-+"""
            messages = re.compile(regex, re.M | re.S).search(notification_email_body).group(1).split("\n\n")
            for index in range(len(messages)):
                quar_messages.append({})
                columns = messages[index].split("\n")
                for column in columns:
                    if not column or re.search(r'Message \d+', column, re.I):
                        continue
                    else:
                        (key, value) = column.split(': ')
                        quar_messages[index][key.lower().strip()] = value.strip()

        return quar_messages
