import json

class ReponseParser():

    def __init__(self, *args, **kwargs):
        pass

    def get_keyword_names(self):
        return [
            'get_response_headers',
            'get_response_body'
        ]

    def get_response_code(self, response):
        return str(response.status_code)

    def get_response_headers(self, response):
        headers = {}

        h_object = response.headers
        for header_name, header_value in h_object.items():
            headers[header_name] = header_value
        
        return headers
    
    def get_response_body(self, response, raw_output=False):
        if raw_output:
            try:
                body = response.text
            except:
                body = response.body
        else:
            body = response.json()
        
        return body