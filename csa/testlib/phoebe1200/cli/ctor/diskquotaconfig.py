#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/diskquotaconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
import re
from clictorbase import DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX
from sal.containers.yesnodefault import YES


class diskquotaconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        self._service_dict = {
            'total': 'Total',
            'spam_quarantine': 'Spam Quarantine (EUQ)',
            'reporting': 'Reporting',
            'tracking': 'Tracking',
            'miscellaneous_files': 'Miscellaneous Files',
            'policy_virus_outbreak_quarantines': 'Policy, Virus & Outbreak Quarantines',
        }
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('diskquotaconfig')
        return self

    def _get_diskquotaconfig_command_output(self):
        disk_quota = ''
        try:
            disk_quota = self._read_until('Choose the operation')
            self._info(disk_quota)
            if disk_quota.find('Service') < 0:
                disk_quota = ''
        finally:
            # return to the CLI prompt
            self._writeln()  # not self._to_the_top(self.level) since
            # _query() has timeout read after
            # _read_until() call
            self._wait_for_prompt()  # to be sure of CLI state

        return disk_quota

    def _get_info_dict(self):
        info_dict = {}
        disk_quota = self._get_diskquotaconfig_command_output()
        for service in self._service_dict.keys():
            regex = ''
            info_dict[service] = {}
            if service is 'total':
                regex = re.escape(self._service_dict[service]) + r'\s+(\S+)\s+(\S+)\s+of\s+(\S+)'
                diskquota_info = re.search(regex, disk_quota, re.I)
                info_dict[service]['usage'] = int(float(diskquota_info.group(1)))
                info_dict[service]['allocated_quota'] = int(float(diskquota_info.group(2)))
                info_dict[service]['available_quota'] = int(float(diskquota_info.group(3)))
                info_dict[service]['unallocated_quota'] = \
                    int(float(diskquota_info.group(3)) - float(diskquota_info.group(2)))

            else:
                regex = re.escape(self._service_dict[service]) + r'\s+(\S+)\s+(\S+)'
                diskquota_info = re.search(regex, disk_quota, re.I)
                info_dict[service]['usage'] = int(float(diskquota_info.group(1)))
                info_dict[service]['quota'] = int(float(diskquota_info.group(2)))

        return info_dict

    def get_quotas(self):
        info_dict = {}
        diskquota_info_dict = self._get_info_dict()
        for service in self._service_dict.keys():
            if service is 'total':
                continue
            info_dict[service] = diskquota_info_dict[service]['quota']
        return info_dict

    def get_service_quota(self, service):
        pattern = re.compile(' ')
        service = pattern.sub('_', service).lower()
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict[service]['quota']

    def get_usages(self):
        info_dict = {}
        diskquota_info_dict = self._get_info_dict()
        for service in self._service_dict.keys():
            info_dict[service] = diskquota_info_dict[service]['usage']
        return info_dict

    def get_service_usage(self, service):
        pattern = re.compile(' ')
        service = pattern.sub('_', service).lower()
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict[service]['usage']

    def get_total_available_quotas(self):
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict['total']['available_quota']

    def get_total_allocated_quotas(self):
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict['total']['allocated_quota']

    def get_total_unallocated_quotas(self):
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict['total']['unallocated_quota']

    def get_total_usages(self):
        diskquota_info_dict = self._get_info_dict()
        return diskquota_info_dict['total']['usage']

    def edit_quotas(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='[]>')

        self._query_response('EDIT')
        param_map['service'] = ['for which you would like to edit disk quota', DEFAULT]
        param_map['quota_size'] = ['Enter the new disk quota', DEFAULT]
        param_map['confirm_quota_srink'] = ['below the current disk usage', YES]

        param_map.update(input_dict or kwargs)
        self._process_input(param_map)
        return self.getbuf()

    def batch(self, input_dict=None, **kwargs):
        params = input_dict or kwargs

        allowed_services = ['euq', 'pvo', 'reporting', 'tracking', 'misc']
        service = params.get('service')
        disk_quota = params.get('disk_quota')

        if service is None:
            raise ValueError('Service name cannot be None. Allowed services are: %s' \
                             % allowed_services)
        if service not in allowed_services:
            raise ValueError('Wrong service name provided. Allowed services are: %s' \
                             % allowed_services)
        if disk_quota is None:
            raise ValueError('Disk quota cannot be None. Must provide disk quota value.')
        if re.search(r'\d+\.\d+|-\d+', disk_quota) or \
                not re.search(r'\d+', disk_quota):
            raise ValueError('Wrong disk quota value provided. Disk quota MUST be an integer')

        cmd = 'diskquotaconfig edit --' + service + ' ' + disk_quota
        self._info('COMMAND to execute: %s' % cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(cmd)
        self._wait_for_prompt()
