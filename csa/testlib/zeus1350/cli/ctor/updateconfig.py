# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/updateconfig.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import clictorbase as ccb
import re

from functools import partial
from sal.containers.yesnodefault import YES, NO
from sal.exceptions import ConfigError

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
default_timeout = 10
RegexObject = type(re.compile(''))


class CliConfiguratorBase(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)

    def _processinput(self, param_map, do_restart=True,
                      timeout=default_timeout, find_answer_key=None):
        if find_answer_key == None:
            return

        answer_map = param_map
        while 1:
            try:
                idx = self._query(answer_map.ending_string,
                                  self._sub_prompt,
                                  timeout=timeout)
                block = self._get_last_matched_text()

            except TimeoutError:
                # need to escase timeout errors in case no
                # prompt appears(eg. multiline input prompted)
                idx = None
                block = self._sess.getbuf()

                # press any key several times to read EULA completely
                if block.endswith('-Press Any Key For More-'):
                    self._writeln()
                    continue

            question_text = re.sub('[\r\n]+', ' ', block, re.MULTILINE)

            # found terminating string
            if idx == 0:
                unanswered = answer_map.get_missing_questions()
                if unanswered and \
                        not IafCliConfiguratorBase.ignore_unanswered_questions:
                    self._restart_nosave()
                    raise ConfigError, 'Unanswered questions:%s' % unanswered

                if do_restart:
                    self._restart()
                return

            # select the answer object to use to answer the question
            key = find_answer_key(question_text, answer_map)
            answer_obj = answer_map[key]
            answer_str = answer_map._get_answer_str(key)

            # answer the question
            if answer_obj['is_input_list']:
                try:
                    self._select_list_item(answer_str, block)
                except (ConfigError, ccb.IafCliValueError,
                        ccb.DuplicateEntry, ccb.UnknownOptionError):
                    self._restart_nosave()
                    raise
            else:
                self._writeln(answer_str)

            # markup answer_map to indicate this answer obj has been used up
            answer_obj['answer_qty'] += 1

    def _find_answer_key_from_list(self, question_text, answer_map):
        for answer_key in answer_map.keys():
            # find text_string in 'question_text'
            text_list = answer_map[answer_key]['text_string']
            comparisons = len(text_list)
            for text_string in text_list:
                found = (isinstance(text_string, RegexObject) and \
                         text_string.search(question_text)) \
                        or \
                        (isinstance(text_string, basestring) and \
                         question_text.find(text_string) >= 0)
                if found and not answer_map.has_been_answered(answer_key):
                    if comparisons > 1:
                        comparisons = comparisons - 1
                    else:
                        return answer_key
                else:
                    break
        if not found:
            raise ConfigError, "Unrecognized question: %r" % (question_text,)


class updateconfig(CliConfiguratorBase):
    def __call__(self):
        self._writeln('updateconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        param_map['update_from'] = [['Feature Key updates'], DEFAULT, True]
        param_map['update_server'] = [['URL of the update server'], DEFAULT]
        param_map['timezone_image_from'] = [['Timezone rules', \
                                             'updates from (images)'], DEFAULT, True]
        param_map['timezone_image_server'] = [['download updates (images)'],
                                              DEFAULT]
        param_map['asyncos_image_from'] = [['AsyncOS upgrades', \
                                            'updates from (images)'], DEFAULT, True]
        param_map['asyncos_image_server'] = [['download updates (images)'],
                                             DEFAULT]
        param_map['timezone_list_from'] = [['Timezone rules', \
                                            'download the list'], DEFAULT, True]
        param_map['timezone_list_server'] = [['HTTP URL of the update list'], \
                                             DEFAULT]
        param_map['asyncos_list_from'] = [['AsyncOS upgrades', \
                                           'download the list'], DEFAULT, True]
        param_map['asyncos_list_server'] = [['HTTP URL of the update list'],
                                            DEFAULT]
        param_map['interval'] = [['time interval between checks'], DEFAULT]
        param_map['routing_table'] = [['choose a specific interface'],
                                      DEFAULT, True]
        param_map['use_proxy'] = \
            [['proxy server for HTTP updates', \
              'Feature Key updates'], DEFAULT]
        param_map['proxy_server'] = [['the URL of the proxy server'], REQUIRED]
        param_map['use_proxy_for_asyncos'] = \
            [['proxy server for HTTP updates for ALL', \
              'AsyncOS upgrades'], REQUIRED]
        param_map['proxy_server_for_asyncos'] = \
            [['the URL of the proxy server'], REQUIRED]
        param_map['use_https_proxy'] = \
            [['an HTTPS proxy server'], DEFAULT]
        param_map['https_proxy_server'] = \
            [['URL of the proxy server. The default'],
             REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')

        return self._processinput(param_map, \
                                  find_answer_key=partial(self._find_answer_key_from_list))

    def validate_certificates(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['validate_certificates'] = ['Should server certificates from Cisco update servers be validated?',
                                              DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('VALIDATE_CERTIFICATES')
        return self._process_input(param_map)

    def dynamichost(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        param_map['dynamic_host'] = ['Enter new manifest hostname:port', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DYNAMICHOST')
        return self._process_input(param_map)
