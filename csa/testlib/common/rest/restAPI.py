import requests
import time
from requests import get


class restAPI(object):
    """
    Perform REST Calls (CRUD operations) based on the provided URL, headers and data,
    Returns response.
    """

    def __init__(self, dut, dut_version):
        # dut info attributes
        self.dut = dut
        self.dut_version = dut_version

    def get_keyword_names(self):
        return [
            'get_header_response',
            'get_header_response_and_request']

    def get_header_response(self, location, user_agent):
        headers = {
            'User-Agent': user_agent
        }
        _resp = get(location, headers=headers, verify=False, timeout=300)
        return _resp.headers

    def post(self, url, headers, data):
        response = requests.post(url=url, headers=headers, json=data)
        time.sleep(2)
        return response

    def get(self, url, headers, verify=False, timeout=300):
        response = requests.get(url, headers=headers, verify=verify, timeout=timeout)
        return response

    def update(self, url, headers, data):
        response = requests.put(url=url, headers=headers, json=data)
        return response

    def delete(self, url, headers, data):
        response = requests.delete(url=url, headers=headers, json=data)
        return response

    def get_header_response_and_request(self, location, user_agent):
        headers = {
                  'User-Agent': user_agent
                  }
        response = get(location, headers=headers,verify=False, timeout=300)
        request_headers=response.request.headers
        return response.headers,request_headers
