from api import Api
from auth import BasicAuth
from common.logging import Logger
from credentials import DUT_ADMIN, DUT_ADMIN_SSW_PASSWORD


class EsaApi(Api, Logger):
    def __init__(self, dut, dut_version, api_port=4431):
        self.api_url = 'https://{0}:{1}/esa/api/v2.0/'.format(dut, api_port)
        self.api = Api()
        self.basic_auth = BasicAuth(
            DUT_ADMIN, DUT_ADMIN_SSW_PASSWORD).get_auth()

    def get_keyword_names(self):
        return [
            'create',
            'read',
            'delete'
        ]

    def create(self, url, auth=None, data=None, **kwargs):
        self._debug('INSIDE esa_api.py -> create')
        self._debug('DATA - {}'.format(data))
        return self.api.post(url, auth=self.basic_auth, data=data, **kwargs)

    def read(self, url, auth=True, params={}, headers={}, **kwargs):
        self._debug('INSIDE esa_api.py -> read')
        self._debug('AUTH - {}'.format(auth))
        self._debug('PARAMS - {}'.format(params))
        self._debug('HEADERS - {}'.format(headers))
        if auth:
            return self.api.get(url, auth=self.basic_auth, params=params, headers=headers, **kwargs)
        else:
            return self.api.get(url, params=params, headers=headers, **kwargs)

    # def update(self):
    #     return self.api.put()

    def delete(self, url, auth=None, data=None, **kwargs):
        self._debug('INSIDE esa_api.py -> create')
        self._debug('DATA - {}'.format(data))
        return self.api.delete(url, auth=self.basic_auth, data=data, **kwargs)

    def construct_reporting_api_url(self, uri, category=None, params={}):
        url = self.api_url + 'reporting/' + uri
        if category:
            url += '/' + category
        return self._get_url_with_params(url, params)

    def construct_message_tracking_api_url(self, uri, params={}):
        url = self.api_url + 'message-tracking/' + uri
        return self._get_url_with_params(url, params)

    def construct_quarantine_api_url(self, uri, params={}):
        url = self.api_url + 'quarantine/' + uri
        return self._get_url_with_params(url, params)

    def construct_log_subscriptions_api_url(self, category=None, params=None):
        if not category:
            url = self.api_url + 'config/logs/subscriptions'
        else:
            url = self.api_url + 'logs/' + category
        return self._get_url_with_params(url, params)
    
    #~~~~~~~~~~~~~~~~~~ Helpder Methods ~~~~~~~~~~~~~~~~~~~#
    def _get_url_with_params(self, url, params):
        if params:
            url += '?' + "&".join(["{0}={1}".format(x[0], x[1]) for x in [(k, v)
                                                                          for k, v in params.items()] if x[1]])
            self._info(url)
        return url
