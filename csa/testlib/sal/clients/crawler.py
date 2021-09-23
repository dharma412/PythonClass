#!/usr/bin/env python -tt
import copy
import httplib
import re
import socket
import ssl
from urlparse import urlparse
from urllib import urlencode
import urllib2
from urllib2 import Request

class DownloadLinkBuilder(object):
    CUSTOM_DATETIME_QUERY_PARAMS = {'custom_range[from][date]': '',
                                    'custom_range[end][date]': '',
                                    'custom_range[from][time]': '',
                                    'custom_range[end][time]': ''}
    RANGES = {'Day': 'current_day',
              'Week': 'current_week',
              'Month': 'current_month',
              'Quarter': 'current_quarter',
              'Year': 'current_year',
              'Previous Day': 'calendar_day',
              'Previous Month': 'calendar_month'}
    DATE_TEMPLATE = '%m/%d/%Y'
    TIME_TEMPLATE = '%H'

    def _get_query(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_path(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def _add_formatted_range_parameter(self, time_range, querydict):
        if time_range is None:
            time_range = 'Day'

        if time_range in self.RANGES.keys():
            # Predefined range detected
            querydict['date_range'] = self.RANGES[time_range]
        else:
            # Custom range detected
            querydict.update(self.CUSTOM_DATETIME_QUERY_PARAMS)
            try:
                from_date_time, end_date_time = \
                    tuple(map(lambda x: x.strip(), time_range.split(',')))
                querydict['custom_range[from][date]'], querydict['custom_range[from][time]'] = \
                    tuple(map(lambda x: x.strip(), from_date_time.split()))
                querydict['custom_range[end][date]'], querydict['custom_range[end][time]'] = \
                    tuple(map(lambda x: x.strip(), end_date_time.split()))
            except Exception as e:
                raise ValueError('Range value "{0}" is not correct. Expected string value' \
                                 ' format: "%m/%d/%Y %H, %m/%d/%Y %H"'.format(time_range))

    def get_link(self):
        return '%s/?%s' % (self._get_path(), self._get_query())


class LoginError(Exception):
    pass


class ApplianceCrawler(object):
    CSRF_PATTERN = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def __init__(self, dut, username, password):
        dut_app_str = ".sgg.cisco.com"
        # added domain .devit.ciscolabs.com for any CS network (eg: cs2, cs14, cs21 etc)
        dut_domain = dut.split(".")[-1:]
        if 'cs' in dut_domain[0]:
            dut_app_str = ".devit.ciscolabs.com"
        dut_new = dut + dut_app_str
        dut = dut_new
        self._base_url = 'https://%s' % (dut,)
        self._username = username
        self._password = password
        print 'DEBUG >>> self._base_url:', self._base_url
        print 'DEBUG >>> self._username:', self._username
        print 'DEBUG >>> self._password:', self._password

        hsh = urllib2.HTTPSHandler()
        cookie_processor = urllib2.HTTPCookieProcessor()
        self._opener = urllib2.build_opener(hsh, cookie_processor)
        self._csrf_key = None

    def _extract_csrf_key(self, html):
        matches = re.findall(self.CSRF_PATTERN, html)
        if matches:
            return matches[0]
        else:
            return ''

    def _get_post_response(self, url, postdata):
        data = copy.copy(postdata)
        data = urlencode(postdata)
        postreq = Request(url, data=data)
        postreq.add_unredirected_header('Content-Length', len(data))
        return self._opener.open(postreq)

    def _login(self):
        response = self._opener.open('%s/login?action=Logout' % (self._base_url,))
        response = self._get_post_response(response.geturl(),
                                           {'username': self._username,
                                            'password': self._password,
                                            'action': 'Login',
                                            'screen': 'login'})
        response_scheme = urlparse(response.geturl())
        if response_scheme.path.find('login') >= 0:
            raise LoginError('Failed to log in to %s' % (self._base_url,))
        self._csrf_key = self._extract_csrf_key(response.read())

    def download(self, url, postdata=None):
        """
        Used to download data from appliance

        :Parameters:
            @url - Link to the download target. It can be absolute or relative url.
                   In case CSRFKey parameter is present it will be automatically exchanged
                   with correct one.
            @postdata - Dictionary with data to be sent via POST request.
                        Leave it as None to send GET request

        :Returns:
            urllib2.Request file-like object with downloaded result

        :Raises:
            LoginError - if failed to log in with given credentials
        """
        self._login()

        url_scheme = urlparse(url)
        path = url_scheme.path
        if not path.startswith('/'):
            path = '/' + path
        query = url_scheme.query
        if postdata is not None and isinstance(postdata, dict):
            data_for_send = copy.copy(postdata)
            data_for_send.update({'CSRFKey': self._csrf_key})
            if len(query):
                url = '%s%s?%s' % (self._base_url, path, query)
            else:
                url = '%s%s' % (self._base_url, path)
            if url[-1] == '/':
                url = url[:-1]
            return self._get_post_response(url, data_for_send)
        else:
            if query.find('CSRFKey=') >= 0:
                query = re.sub(self.CSRF_PATTERN, self._csrf_key, query)
            elif len(query):
                query += '&CSRFKey=%s' % (self._csrf_key,)
            else:
                query = 'CSRFKey=%s' % (self._csrf_key,)
            url = '%s%s?%s' % (self._base_url, path, query)
            return self._opener.open(url)


def download(dut, url, username='admin', password='ironport', postdata=None):
    crawler = ApplianceCrawler(dut, username, password)
    return crawler.download(url, postdata)


if __name__ == '__main__':
    download('c670q11.ibqa',
             'monitor/reports/report?format=csv&' \
             'CSRFKey=85244a22-c3d6-475a-93e4-3c5da230f014&' \
             'report_query_id=mga_overview_incoming_mail_summary&' \
             'date_range=current_day&report_def_id=mga_overview&' \
             'sort_col_ss_1_0_1=MAIL_INCOMING_TRAFFIC_SUMMARY.BLOCKED_REPUTATION')
