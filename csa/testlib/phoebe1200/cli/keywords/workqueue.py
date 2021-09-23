#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/workqueue.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class WorkQueue(CliKeywordBase):
    """ WorkQueue command displays work-queue statistics over time.
    """

    def get_keyword_names(self):
        return [
            'workqueue_pause',
            'workqueue_resume',
            'workqueue_rate',
            'workqueue_status'
        ]

    def workqueue_pause(self, confirm='YES', reason='RF keyword'):
        """Pauses the work queue.


        *Parameters*:
        - `confirm` : YES|NO
        - `reason` : Reason of pausing the queue

        *Return*:
          None

        *Examples*:

        | WorkQueue Pause | YES |

        """
        self._cli.workqueue().pause(self._process_yes_no(confirm), reason)

    def workqueue_resume(self):
        """ Resumes the work queue.

        *Parameters*:
         None

        *Return*:
          None

        *Examples*:

        | WorkQueue Resume |  |

        """

        self._cli.workqueue().resume()

    def workqueue_rate(self, delay=5, period=1):
        """ Defines the rate of workqueue displays.

        *Parameters*:
        - `delay` : Number of seconds to wait between displays. Default: 5 secs.
        - `period` : Time interval till which the workqueue status will be displayed. Default: 1.

        *Return*:
          Returns list variable with the pending rate, in rate and out rate

        *Examples*:

        | @{rate_list}= | WorkQueue Rate | 10 | 2 |

        """

        obj_list = self._cli.workqueue().rate(delay, int(period))
        rate_list = [obj_list[0].pending_rate, obj_list[0].in_rate, obj_list[0].out_rate]
        return rate_list

    def workqueue_status(self):
        """ Displays the status of the work queue.

        *Parameters*:
         None

        *Return*:
         Returns list variable with the status of workqueue & number of workqueue messages

        *Examples*:

        |@{status_msgs}= | WorkQueue Status |

        """

        out1 = self._cli.workqueue().status()
        list1 = [out1.status, out1.messages]
        return list1
