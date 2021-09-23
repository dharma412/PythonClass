#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/tarpit.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class Tarpit(CliKeywordBase):
    """
    tarpit

    If on, the system will slow down receiving when it hits the tarpit
    threshold.  The system can optionally monitor the size of the work
    queue and refuse new connections in critical resource conservation
    situations.
    """

    def get_keyword_names(self):
        return ['tarpit_setup']

    def tarpit_setup(self, *args):
        """
        tarpit -> setup

        *Parameters:*
        - `slow_down`: Should the system slow down receiving when memory is low?
                       Either yes or no
        - `memory_usage_for_rcmode` : Enter the percentage of memory usage
                        required to enter resource conservation mode
                        Default is 75
        - `memory_usage_to_refuse_mail` : Enter the percentage of memory usage
                        required to refuse mail. Default is 85
        - `suspend_listener` : Should the system refuse mail by suspending listeners?
                               Either yes or no
        - `suspend_listener_on_work_queue_size` :
                              Do you want to suspend listeners based on work queue size?
                              Either yes or no
        - `no_of_msgs_to_suspend` : Enter the number of work queue messages above
                                    which listeners will be suspended. Default is 1000000
        - `no_of_msgs_to_resume` : Enter the number of work queue messages at or below
                                   which listeners will be resumed. Default is 0

        *Examples:*
        | tarpit setup | slow_down=yes | memory_usage_for_rcmode=80 |
        | tarpit setup | slow_down=yes | suspend_listener=yes | suspend_listener_on_work_queue_size=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.tarpit().setup(**kwargs)
