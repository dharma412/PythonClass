import requests

from common.logging import Logger


class Misc(Logger):
    def __init__(self, dut, dut_version):
        pass

    def get_keyword_names(self):
        return [
            'get_adfs_access_token'
        ]

    def get_adfs_access_token(self, params={}):
        """
        API Library keyword to generate ADFS access token

        *Params*
          A dictionary containing below keys
            `adfs_auth_url` - API end point URL for generating the access token
            `adfs_username` - ADFS server username
            `adfs_password` - ADFS server password
            `adfs_resource` - ADFS server resource url
            `adfs_client_id` - ADFS client id
            `adfs_scope` - ADFS scope
            `adfs_grant_type` - Access token grant type
        
        *Return*
          Returns the response object containing response headers and response body
        
        *Examples*
        ${adfs_data}=  Create Dictionary
        ...  adfs_auth_url      ${ADFS_AUTH_URL}
        ...  adfs_resource      ${ADFS_RESOURCE}
        ...  adfs_username      ${ADFS_USERNAME}
        ...  adfs_password      ${ADFS_PASSWORD}
        ...  adfs_client_id     ${ADFS_CLIENT_ID}
        ...  adfs_scope         ${ADFS_SCOPE}
        ...  adfs_grant_type    ${ADFS_GRANT_TYPE}
        ${response}=  Get Adfs Access Token  ${adfs_data}
        Log  ${response}
        ${body}=  Get Response Body  ${response}
        Log Dictionary  ${body}
        ${access_token}=  Get From Dictionary  ${body}  access_token
        Log  ${access_token}
        """
        data = {
            'UserName': params.adfs_username,
            'Password': params.adfs_password,
            'resource': params.adfs_resource,
            'client_id': params.adfs_client_id,
            'scope': params.adfs_scope,
            'grant_type': params.adfs_grant_type
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self._debug('Request URL - {}'.format(params.adfs_auth_url))
        self._debug('Request Headers - {}'.format(headers))
        self._debug('Request Body - {}'.format(data))
        return requests.post(params.adfs_auth_url, headers=headers, data=data, verify=False)
