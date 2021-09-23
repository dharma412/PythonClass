#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/sscconfig.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
SARF CLI command: sscconfig

On SSC:
sscconfig >
    Edit Security Services Cluster settings.

    sscconfig enable <service_name> <interface_name> <port_number>
    sscconfig disable <service_name>
    sscconfig show
    sscconfig list

    Sub-commands:
        enable           - Enable a service to run on this host.
        disable          - Disable a service on this host
        show             - Show statuses of SSC services
        list             - List all SSC services

    Options:
        service_name     - Name of the scanning engine/service
        Interface_name   - Name of the interface on which service should run.

On MG:
sscconfig >
    Edit Security Services Cluster settings.

    sscconfig offbox <service_name> <service_address>
    sscconfig onbox <service_name>
    sscconfig show
    ssconfig list

    Sub-commands:
        offbox           - Move a service offbox
        onbox            - Restore a service to on-box
        show             - Show statuses of SSC services
        list             - List all SSC services

    Options:
        service_name     - Name of the scanning engine/service
        service_address  - Remote address of the service in '<IP>:<Port Number>' format.
"""

import clictorbase as ccb

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
from sal.containers.yesnodefault import YES, is_yes


class sscconfig(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        return self

    def enable(self, service_name=REQUIRED, \
               interface_name=REQUIRED, port=DEFAULT):
        command = 'sscconfig enable %s %s %s' % \
                  (service_name, interface_name, port)
        self._writeln(command)

    def disable(self, service_name=REQUIRED):
        command = 'sscconfig disable %s' % service_name
        self._writeln(command)

    def onbox(self, service_name=REQUIRED):
        command = 'sscconfig onbox %s' % service_name
        self._writeln(command)

    def offbox(self, service_name=REQUIRED, \
               service_address=REQUIRED, port=DEFAULT):
        command = 'sscconfig offbox %s %s:%s' % \
                  (service_name, service_address, port)
        self._writeln(command)

    def list(self):
        self.clearbuf()
        self._writeln('sscconfig list')
        self._wait_for_prompt()
        output = self.getbuf()

        """ sscconfig list output
        vm30esa0045.ibqa> sscconfig list

        Following services can run as a Security Service Cluster
        sophos
        mcafee
        vm30esa0045.ibqa>
        """
        services = [x.rstrip() for x in (output.split('\n')[3:-1])]
        return services

    def show(self, as_dictionary=YES):
        self.clearbuf()
        self._writeln('sscconfig show')
        self._wait_for_prompt()
        self.output = self.getbuf()
        self.dict = {}

        """  sscconfig show output
        On SSC:
        vm30esa0045.ibqa> sscconfig show

        Status of Security Services Cluster
        -------------------------------------------------------------------------------------
        Service                                       Location           Service Address
        -------------------------------------------------------------------------------------
        sophos                                        Management (onbox) 10.76.68.138:8004
        -------------------------------------------------------------------------------------
        vm30esa0045.ibqa>

        On MG using offbox:
        vm30esa0108.ibqa> sscconfig show

        Status of Security Services Cluster
        -------------------------------------------------------------------------------------
        Service                                       Location           Service Address
        -------------------------------------------------------------------------------------
        sophos                                        offbox             10.76.68.138:8004
        -------------------------------------------------------------------------------------
        vm30esa0108.ibqa>

        On MG using onbox:
        vm30esa0108.ibqa> sscconfig show

        Status of Security Services Cluster
        -------------------------------------------------------------------------------------
        Service                                       Location           Service Address
        -------------------------------------------------------------------------------------
        sophos                                        onbox              -
        -------------------------------------------------------------------------------------
        vm30esa0108.ibqa>
        """

        if is_yes(as_dictionary):
            import re
            list = re.findall('(\w+)\s+' \
                              '(\w+\s\(\w+\)|\w+|-)\s+' \
                              '(\d+\.\d+\.\d+\.\d+:\d+|-)\s+', self.output)
            for item in list:
                service = item[0]
                self.dict[service] = {}
                self.dict[service]['Location'] = item[1]
                self.dict[service]['Service Address'] = item[2]
        else:
            self.dict = self.output
        return self.dict
