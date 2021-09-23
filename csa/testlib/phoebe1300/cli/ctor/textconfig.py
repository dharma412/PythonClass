#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/textconfig.py#1 $


import clictorbase
from clictorbase import IafCliParamMap, REQUIRED, DEFAULT
from sal.exceptions import TimeoutError


class textconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('textconfig')
        return self

    def new(self, resource_type=DEFAULT, resource_name=DEFAULT,
            encoding_type=DEFAULT, notification_template=DEFAULT,
            auto_diff=DEFAULT, plain_template=DEFAULT):
        data = notification_template or "automation test"
        data1 = plain_template or "automation test"
        self._query_response('NEW')
        self._query_select_list_item(resource_type)
        self._query_response(resource_name)
        self._query_select_list_item(encoding_type)
        self._writeln(data + "\n.")
        idx = self._query('Use the auto-generated plain text version', \
                          'Choose the operation')
        if idx == 0:
            self._query_select_list_item(auto_diff)
            if auto_diff == '2':
                self._writeln(data1 + "\n.")

        self._to_the_top(1)

    def import_method(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='created.')

        param_map['resource_type'] = ['kind of text resource', DEFAULT, 1]
        param_map['resource_name'] = ['create a name', REQUIRED]
        param_map['file_name'] = ['file to import', REQUIRED]
        param_map['encoding_type'] = ['encoding', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        self._query_response('import')
        return self._process_input(param_map)

    def export(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='written')

        param_map['resource_name'] = ['resource to export', REQUIRED]
        param_map['file_name'] = ['file to export', REQUIRED]
        param_map['encoding_type'] = ['encoding', DEFAULT, 1]

        param_map.update(input_dict or kwargs)

        self._query_response('export')
        return self._process_input(param_map)

    def export_saved(self, resource_name=DEFAULT, file_name=DEFAULT,
                     encoding_type=DEFAULT):
        self._query_response('EXPORT')
        self._query_select_list_item(resource_name)
        self._query_response(file_name)
        self._query_select_list_item(encoding_type)
        self._to_the_top(2)

    def print_method(self, resource_name=DEFAULT):
        self.clearbuf()
        self._query_response('PRINT')
        self._query_response(resource_name)
        self._expect('\n')
        while 1:
            try:
                self._expect(['-Press Any Key For Exit-', 'Choose the operation'],
                             timeout=10)
                raw = self.getbuf()
                if self._expectindex != 0:
                    break
                else:
                    self._writeln('')
                    continue
            except TimeoutError:
                raise TimeoutError, "Text Resource details not found"
                break
        self._to_the_top(1)
        return raw

    def edit(self, resource_name=DEFAULT, encoding_type=DEFAULT,
             new_text=DEFAULT, auto_diff=DEFAULT, plain_template=DEFAULT):
        data = new_text or "another automation test"
        data1 = plain_template or "automation test"
        self._query_response('EDIT')
        self._query_response(resource_name)
        self._query_select_list_item(encoding_type)
        self._writeln(data + "\n.")
        idx = self._query('Use the auto-generated plain text version', 'Choose the operation')
        if idx == 0:
            self._query_select_list_item(auto_diff)
            if auto_diff == '2':
                self._writeln(data1 + "\n.")

        self._to_the_top(1)

    def delete(self, resource_name=DEFAULT):
        from sal.containers.yesnodefault import YES
        self._query_response('DELETE')
        self._query_response(resource_name)
        self._expect(['WARNING:', 'Choose the operation'])
        if self._expectindex == 0:
            self._query_response(YES)
        self._to_the_top(1)

    def list(self):
        self._query_response('LIST')
        self._query('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(2)
        return raw


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    text_cfg = textconfig(cli_sess)
    text_cfg().new(resource_type='5', resource_name='notify-template-one', \
                   encoding_type='US-ASCII', notification_template="notify-template-one\r\n.", \
                   auto_diff='2', plain_template='chumma\r\n.')
    text_cfg().edit(resource_name='notify-template-one', \
                    encoding_type='US-ASCII', new_text="notify-template-one\r\n.", \
                    auto_diff='2', plain_template='chummachanged\r\n.')
    text_cfg().export(resource_name='notify-template-one', file_name='export_test.txt',
                      encoding_type='US-ASCII')
    print text_cfg().print_method(resource_name='notify-template-one')
    text_cfg().delete(resource_name='notify-template-one')
    text_cfg().import_method(resource_type='5',
                             resource_name='MyTest1', file_name='export_test.txt',
                             encoding_type='US-ASCII')
    text_cfg().new(resource_type='Notification Template',
                   resource_name='MyTest',
                   encoding_type='Unicode (UTF-8)',
                   notification_template="automation test\r\n.")

    # export test
    text_cfg().export(resource_name='MyTest', file_name='export_test.txt',
                      encoding_type='Unicode (UTF-8)')

    # print test
    print text_cfg().print_method(resource_name='MyTest')

    # delete test
    text_cfg().delete(resource_name='MyTest')

    # import test
    text_cfg().import_method(resource_type='Notification',
                             resource_name='MyTest', file_name='export_test.txt',
                             encoding_type='UTF-8')

    # edit test
    text_cfg().edit(resource_name='MyTest', encoding_type='US-ASCII')

    print 'textconfig test PASSED!'
