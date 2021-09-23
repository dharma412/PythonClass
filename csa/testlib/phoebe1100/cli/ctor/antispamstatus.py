#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/antispamstatus.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
    IAF 2 CLI ctor - antispamstatus
"""

import clictorbase as ccb

import re
from sal.containers import cfgholder


class antispamstatus(ccb.IafCliConfiguratorBase):
    """antispamstatus
        - when there's feature key for both CASE and Brightmail,
          need to specify vendor=(ironport, brightmail)
    """

    def __call__(self, vendor=None):
        self.parser_class = {'ironport': antispamstatusIPAS,
                             'ipas': antispamstatusIPAS,
                             'brightmail': antispamstatusBrightmail,
                             'cloudmark': antispamstatusCloudmark,
                             'multiscan': antispamstatusMultiscan
                             }

        self.clearbuf()
        self._writeln('antispamstatus')
        idx = self._query(self._get_prompt(), 'Choose the operation')
        lines = self.getbuf()
        if idx == 0 and not vendor:
            return lines
        elif idx == 0 or idx == 1:
            assert vendor in self.parser_class.keys(), \
                'Invalid AS vendor: %s. Expected one of:[%s]' % (vendor,
                                                                 ','.join(self.parser_class.keys()))
            if idx == 1:
                self._query_response(vendor)
                lines = self._wait_for_prompt()
        else:
            raise ccb.IafCliError, 'Unexpected response: %r' % lines

        return self.parser_class[vendor](lines)


class antispamstatusInfo(cfgholder.CfgHolder):
    def _parse_line(self, line):
        result = self.parse_patt.search(line)
        if not result:
            return ()
        else:
            return result.groups()

    def _starts_with_key(self, line):
        # abstract method
        raise NotImplementedError

    def __init__(self, raw):
        cfgholder.CfgHolder.__init__(self)
        self._parse_lines(raw.split('\n')[3:-1])

    def _parse_lines(self, lines):
        """ Parses given lines and composes a dictionary of antispam status info

        Component              Last Update                  Version
        CASE Core Files        Base Version                 2.2.0-010
        Structural Rules       10 Dec 2007 14:07 (GMT)      2.2.0-010-20071209_054101
        Content Rules          10 Dec 2007 14:07 (GMT)      20071210_140320
        Content Rules Update   10 Dec 2007 14:11 (GMT)      20071210_140804
        CASE Utilities         Base Version                 2.2.0-010
        Web Reputation DB      10 Dec 2007 14:07 (GMT)      20071206_230000
        Web Reputation Rules   10 Dec 2007 14:07 (GMT)      20071206_230000-20071210_140000

        Following cases should be handled correctly
            - each line contains component definition, update date, version
            - line can be splitted due to console width limitations (80 chars)
            - missed components mean bug in product
            - duplicated components mean bug in product
        """

        comp_dict = dict(zip(self.components, [False] * len(self.components)))

        iter_lines = iter(lines)
        try:
            while 1:
                line = iter_lines.next().strip()
                print '*' * 5, line, '*' * 5
                # extract cells
                cells = self._parse_line(line)
                print '*' * 5, cells, '*' * 5

                while len(cells) != len(self.columns):
                    # non enough... append followed lines
                    line += self.col_sep + iter_lines.next().strip()
                    print '*' * 10, line, '*' * 10
                    cells = self._parse_line(line)
                    print '*' * 10, cells, '*' * 10
                    # TODO: extra data capturing control

                if comp_dict.has_key(cells[0]) and not comp_dict[cells[0]]:
                    comp_dict[cells[0]] = True
                    attr_name = cells[0].lower().replace(' ', '_').replace('-', '_')
                    attributes = dict(zip(self.columns[1:], cells[1:]))
                    self[attr_name] = cfgholder.CfgHolder(attributes)
                else:
                    pass
                    # print 'antispamstatus(): unexpected line[%s]' % line

        except StopIteration:
            pass

    def __str__(self):
        return '\n'.join(map(
            lambda (key, value): '%s:%s' % \
                                 (' '.join([i.capitalize() for i in key.split('_')]).ljust(20),
                                  ':'.join(map(lambda x: self[key][x], self.columns[1:])),
                                  ),
            self.iteritems()))


class antispamstatusIPAS(antispamstatusInfo):
    columns = ('component', 'update_date', 'version')
    parse_patt = re.compile(r'(\w[\S ]+\w) {2,}(\S[\S ]+\S) {2,}([\d\.\-_]+)')
    col_sep = '   '
    components = ['CASE Core Files',
                  'Structural Rules',
                  'Content Rules',
                  'Content Rules Update',
                  'CASE Utilities',
                  'Web Reputation DB',
                  'Web Reputation Rules',
                  ]


class antispamstatusBrightmail(antispamstatusInfo):
    columns = ('component', 'update_date')
    parse_patt = re.compile(r'(\w[\S ]+\w) {3,}(\S[\S ]+\S)')
    col_sep = '   '
    components = ['Header Rules',
                  'Body Hash Rules',
                  'Heuristic Rules',
                  'BrightSig2 Rules',
                  'Intsig Rules',
                  'Open Proxy List',
                  ]


class antispamstatusCloudmark(antispamstatusInfo):
    columns = ('component', 'update_date', 'version')
    parse_patt = re.compile(r'(\w[\w\-]+\w) {3,}(\S[\S ]+\S) {2,}([\d\.]+)')
    col_sep = '   '

    components = ['meta-data-mfl',
                  'meta-data-dpl',
                  'meta-data-mpl',
                  'meta-data-rpl',
                  'meta-data-ipl',
                  'categories',
                  'meta-data-wpl',
                  'meta-data-rplv2',
                  'cartridge',
                  'meta-data-xrl',
                  'meta-data-ebl',
                  'meta-data-impl',
                  'meta-data-fsl',
                  'meta-data-lgl',
                  'meta-data-csl',
                  ]


class antispamstatusMultiscan(antispamstatusInfo):
    def __init__(self, lines):
        status = antispamstatusIPAS(lines)
        status.update(antispamstatusCloudmark(lines))
        for key in status.keys():
            self[key] = status[key]


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    ass = antispamstatus(cli_sess)
    print ass('ironport')
    print ass('brightmail')
    print ass('ironport').content_rules.update_date
    print ass('ironport').case_core_files.version
    print ass('ironport').web_reputation_db.version
