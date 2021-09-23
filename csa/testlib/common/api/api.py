
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from exceptions import URLMissingException


class Api(object):
    
    def get(self, url, auth=None, params={}, headers={}, **kwargs):
        if auth:
            response = requests.get(
                url, auth=auth, params=params, headers=headers, verify=False)
        else:
            response = requests.get(
                url, params=params, headers=headers, verify=False)
        return response

    def post(self, url, auth=None, data=None, **kwargs):
        if auth:
            response = requests.post(url, auth=auth, json=data, verify=False)
        else:
            response = requests.post(url, json=data, verify=False)
        return response
    
    def delete(self, url, auth=None, data=None, **kwargs):
        if auth:
            response = requests.delete(url, auth=auth, json=data, verify=False)
        else:
            response = requests.post(url, json=data, verify=False)
        return response
    
    # def put():
    #     place holder for PUT method.
