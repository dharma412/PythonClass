#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/policy_trace.py#2 $
# $DateTime: 2019/11/17 23:33:35 $
# $Author: biaramba $

import time
from common.gui.guicommon import GuiCommon

URL_TEXTBOX = 'id=url'
IP_TEXTBOX = 'id=ip'
USERNAME_TEXTBOX = 'id=auth_user'
AUTH_REALMS_LIST = 'id=auth_realm'
PROXY_PORT_TEXTBOX = 'id=fwd_conn_port'
USER_AGENT_TEXTBOX = 'id=user_agent'
OBJECT_SIZE_RESP_TEXTBOX = 'id=object_size'
OBJECT_SIZE_REQ_TEXTBOX = 'req_object_size'
MIME_TYPE_RESP_TEXTBOX = 'id=mime_type'
MIME_TYPE_REQ_TEXTBOX = 'req_mime_type'
REQ_DATE_TEXTBOX = 'id=request_date'
REQ_TIME_TEXTBOX = 'id=request_time'
WBRS_TEXTBOX = 'name=wbrs_score'
URL_CATEGORY_LIST = 'id=url_cat'
APP_LIST = 'application_id'
WEBROOT_VERDICT_RESP_LIST = 'id=webroot_verdict'
WEBROOT_VERDICT_REQ_LIST = 'req_webroot_verdict'
MCAFEE_VERDICT_RESP_LIST = 'id=mcafee_verdict'
MCAFEE_VERDICT_REQ_LIST = 'req_mcafee_verdict'
SOPHOS_VERDICT_RESP_LIST = 'id=sophos_verdict'
SOPHOS_VERDICT_REQ_LIST = 'req_sophos_verdict'
FIND_POLICY_MATCH_BUTTON = 'find_policy_button'
RESULT_CONTAINER = "//div[@id='result_container']"
UPLOAD_TEXTBOX = 'req_body_content'

class PolicyTrace(GuiCommon):

    def _open_page(self):
        self._navigate_to('System Administration', 'Policy Trace')

    def get_keyword_names(self):
        return ['policy_trace_find_policy_match']

    def _fill_url_textbox(self, url):
        self.input_text(URL_TEXTBOX, url)

    def _fill_client_ip_textbox(self, ip):
        self.input_text(IP_TEXTBOX, ip)

    def _fill_username_textbox(self, username):
        self.input_text(USERNAME_TEXTBOX, username)

    def _select_auth_realm(self, auth_realm, auth_sgt=None):
        auth_sgt_textbox = 'id=auth_sgt'
        auth_realms_list = self.get_list_items(AUTH_REALMS_LIST)

        if auth_realm in auth_realms_list:
            self.select_from_list(AUTH_REALMS_LIST, auth_realm)
            self._input_text_if_not_none(auth_sgt_textbox, auth_sgt)
        else:
            raise ValueError('"%s" auth realm does not exist' % (auth_realm,))

    def _fill_proxy_port_textbox(self, port):
        self.input_text(PROXY_PORT_TEXTBOX, port)

    def _fill_user_agent_textbox(self, user_agent):
        self.input_text(USER_AGENT_TEXTBOX, user_agent)

    def _fill_upload_file_textbox(self, upload_file):
        self.choose_file(UPLOAD_TEXTBOX, upload_file)

    def _fill_request_time_textbox(self, request_time):
        time_directives = ('%m/%d/%Y', '%H:%M')
        try:
            st = time.strptime(request_time, ' '.join(time_directives))
        except ValueError, err_msg:
            raise ValueError('Time format is invalid. Error message - %s' % \
                             (err_msg,))

        for box_id, time_directive in zip((REQ_DATE_TEXTBOX, REQ_TIME_TEXTBOX),
                                           time_directives):
            time_val = time.strftime(time_directive, st)
            self.input_text(box_id, time_val)

    def _select_url_category(self, url_category):
        url_cat_list = self.get_list_items(URL_CATEGORY_LIST)

        if url_category in url_cat_list:
            self.select_from_list(URL_CATEGORY_LIST, url_category)
        else:
            raise ValueError('"%s" url category does not exist' % \
                            (url_category,))

    def _select_application(self, application):
        application_list = self.get_list_items(APP_LIST)

        # get application's name
        try:
            # assume application is a Constant from constants.py
            app_name = application.name
        except:
            app_name = str(application)
        if app_name in application_list:
            self.select_from_list(APP_LIST, app_name)
        else:
            raise ValueError('"%s" application does not exist' % \
                            (app_name,))

    def _fill_object_size_textbox(self, obj_size, obj_textbox):
        self.input_text(obj_textbox, obj_size)

    def _fill_mime_type_textbox(self, mime_type, mime_textbox):
        self.input_text(mime_textbox, mime_type)

    def _fill_wbrs_score_textbox(self, wbrs_score):
        self.input_text(WBRS_TEXTBOX, wbrs_score)

    def _select_verdict(self, verdict, verdict_list):
        verdicts = self.get_list_items(verdict_list)
        if verdict in verdicts:
            self.select_from_list(verdict_list, verdict)
        else:
            raise ValueError\
             ('"%s" Verdict does not exist' % (verdict,))

    def _click_find_policy_match(self):
        self.click_button(FIND_POLICY_MATCH_BUTTON)

    def _parse_trace_output(self, trace_output):
        # mapping of keywords of trace output to attributes of result object
        keys_map = {'URL Category': 'url_cat',
                    'User Name': 'auth_user',
                    'Access policy': 'access_policy',
                    'Identity policy': 'identity_policy',
                    'Routing policy': 'routing_policy',
                    'IronPort Data Security policy': 'ids_policy',
                    'Details': 'details',
                    'Decryption policy': 'decryption_policy',
                    'User-Agent': 'user_agent'}

        trace_result = {}
        # Retrieve all lines from trace output that match
        # "trace keyword: value" pattern and convert this
        # information to dictionary
        result_lines = map(lambda line: line.split(':', 1), trace_output.splitlines())
        result_dict = dict(filter(lambda x: len(x) == 2, result_lines))

        for trace_keyword, attribute in keys_map.iteritems():
            value = result_dict.get(trace_keyword)
            if value:
                value = value.strip(' ')

            trace_result[attribute] = str(value)
        # in case of error - return error message in corresponding key
        if 'Trace request failed' in trace_output.splitlines():
            trace_result['error'] = trace_output

        return trace_result

    def _get_trace_result(self):
        self._wait_for_text(RESULT_CONTAINER, 'session complete')
        trace_result = self.get_text(RESULT_CONTAINER)

        return self._parse_trace_output(trace_result)

    def _open_advanced_settings(self):
        advanced_link_open = "arrow_open"
        advanced_link_close = "arrow_closed"
        if not self._is_visible(advanced_link_open):
            self.click_element(advanced_link_close, "don't wait")

    def policy_trace_find_policy_match(self,
                 url,
                 client_ip=None,
                 username=None,
                 auth_realm=None,
                 auth_sgt=None,
                 proxy_port=None,
                 user_agent=None,
                 request_time=None,
                 upload_file=None,
                 url_category=None,
                 application=None,
                 object_size_req=None,
                 object_size_resp=None,
                 mime_type_resp=None,
                 mime_type_req=None,
                 wbrs_score=None,
                 webroot_verdict_resp=None,
                 webroot_verdict_req=None,
                 mcafee_verdict_resp=None,
                 mcafee_verdict_req=None,
                 sophos_verdict_resp=None,
                 sophos_verdict_req=None):
        """Trace request and details how WSA processes the request to specified URL.

        Parameters:
            - `url`: URL to simulate request to.
            - `client_ip`: IP address of the client machine to simulate.
            - `username`: user name of the authentication user.
            - `auth_realm`: name of the authentication realm.
            - `auth_sgt`: SGT - applicable for ise authentication
            - `proxy_port`: proxy port to use for the trace request.
            - `user_agent`: user agent to simulate in the request.
            - `request_time`: the day and time of the request
                              in 'MM/DD/YYYY HH:MM' format.
            - `upload_file`: file to upload
            - `url_category`: URL category of the transaction response
                              to override.
            - `application`: Application of the transaction response
                             to override.
            - `object_size_resp`: the size of the response object. Add a
                                  trailing K, M, or G to indicate size unit
            - `object_size_req`: the size of the request object. Add a
                                 trailing K, M, or G to indicate size unit
            - `mime_type_resp`: MIME type of the response object.
            - `mime_type_req`: MIME type of the request object.
            - `wbrs_score`: web reputation score to use.
            - `webroot_verdict_resp`: Webroot verdict of response object.
            - `webroot_verdict_req`: Webroot verdict of request object.
            - `mcafee_verdict_resp`: McAfee verdict of response object.
            - `mcafee_verdict_req`: McAfee verdict of request object.
            - `sophos_verdict_resp`: Sophos verdict of response object.
            - `sophos_verdict_req`: Sophos verdict of request object.

        Return:
           Dictionary with results of policy match. In case of error, error
           message is returned in dictionary item with key 'error'.

           All available dictionary keys: 'url_cat', 'access_policy',
           'identity_policy', 'routing_policy', 'ids_policy', 'details',
           'decryption_policy', 'user_agent', 'error'.

        Example:
        | Policy Trace Find Policy Match | http://yahoo.com |
        | | client_ip=10.7.1.160 |
        | | username=myUser |
        | | auth_realm=myLdapRealm |
        | | proxy_port=3128 |
        | | user_agent=${useragents.MSIE} |
        | | request_time=04/07/2010 10:15 |
        | | upload_file=%{HOME}/work/sarf_centos/tests/coeus75/unittests/gui/saas.txt |
        | | object_size_req=1000K |
        | | object_size_resp=2000K |
        | | mime_type_req=${mimetypes.TEXT_RTF} |
        | | mime_type_resp=${mimetypes.TEXT_RTF} |
        | | webroot_verdict_req=${mwcats.WORM} |
        | | webroot_verdict_resp=${mwcats.WORM} |
        | | mcafee_verdict_req=${mwcats.VIRUS} |
        | | mcafee_verdict_resp=${mwcats.VIRUS} |
        | | sophos_verdict_req=${mwcats.UNSCANNABLE} |
        | | sophos_verdict_resp=${mwcats.UNSCANNABLE} |
        | | url_category=${webcats.GAMES} |
        | | application=${applications.MPEG} |
        | | wbrs_score=2.3 |

        """
        self._open_page()

        self._fill_url_textbox(url)
        if client_ip:
            self._fill_client_ip_textbox(client_ip)
        if username:
            self._select_auth_realm(auth_realm, auth_sgt)
            self._fill_username_textbox(username)

        # open advanced settings panel
        self._open_advanced_settings()

        if proxy_port:
            self._fill_proxy_port_textbox(proxy_port)
        if user_agent:
            self._fill_user_agent_textbox(user_agent)
        if request_time:
            self._fill_request_time_textbox(request_time)
        if upload_file:
            self._fill_upload_file_textbox(upload_file)
        if url_category:
            self._select_url_category(url_category)
        if application:
            self._select_application(application)
        if object_size_resp:
            self._fill_object_size_textbox(object_size_resp,
                                           OBJECT_SIZE_RESP_TEXTBOX)
        if object_size_req:
            self._fill_object_size_textbox(object_size_req,
                                           OBJECT_SIZE_REQ_TEXTBOX)
        if mime_type_resp:
            self._fill_mime_type_textbox(mime_type_resp,
                                         MIME_TYPE_RESP_TEXTBOX)
        if mime_type_req:
            self._fill_mime_type_textbox(mime_type_req,
                                         MIME_TYPE_REQ_TEXTBOX)
        if wbrs_score:
            self._fill_wbrs_score_textbox(wbrs_score)
        if webroot_verdict_resp:
            self._select_verdict(webroot_verdict_resp,
                                 WEBROOT_VERDICT_RESP_LIST)
        if webroot_verdict_req:
            self._select_verdict(webroot_verdict_req, WEBROOT_VERDICT_REQ_LIST)
        if mcafee_verdict_resp:
            self._select_verdict(mcafee_verdict_resp, MCAFEE_VERDICT_RESP_LIST)
        if mcafee_verdict_req:
            self._select_verdict(mcafee_verdict_req, MCAFEE_VERDICT_REQ_LIST)
        if sophos_verdict_resp:
            self._select_verdict(sophos_verdict_resp, SOPHOS_VERDICT_RESP_LIST)
        if sophos_verdict_req:
            self._select_verdict(sophos_verdict_req, SOPHOS_VERDICT_REQ_LIST)

        self._click_find_policy_match()
        time.sleep(5)

        result = self._get_trace_result()
        return result
