#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/reporting_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT
import common.cli.cliexceptions as cliexceptions

class ReportingConfig(CliKeywordBase):
    """Configure reporting system."""

    def get_keyword_names(self):
        return [
            'reporting_config_counters',
            'reporting_config_avg_obj_size',
            'reporting_config_web_event_bucketing',
            'reporting_config_centralized',
        ]

    def reporting_config_counters(self, level=DEFAULT):
        """Limit counters recorded by the reporting system.

        reportingconfig > counters

        Parameter:
        - `level`: level of reporting system limitation.
                   'Unlimited', 'Minimally' or 'Moderately'

        Example:
        | Reporting Config Counters | level='Minimally' |

        """
        self._cli.reportingconfig().counters(level)

    def reporting_config_avg_obj_size(self, size=DEFAULT):
        """Average HTTP Object Size used for Bandwidth Savings
           Calculation.

        reportingconfig > averageobjectsize

        Parameter:
        - `size`: Average HTTP Object Size (in bytes)

        Example:
        | Reporting Config Avg Obj Size | size=12288 |

        """
        self._cli.reportingconfig().averageobjectsize(size)

    def reporting_config_web_event_bucketing(self, enable=None):
        """Enable or Disable web transaction event bucketing.

        reportingconfig > webeventbucketing

        Parameter:
        - `enable`: Enable or Disable web transaction event bucketing.
                    'yes' to enable, 'no' to disable

        Example:
        | Reporting Config Web Event Bucketing | enable=no |

        """
        if enable is not None:
            if enable.lower() == 'yes':
                self._cli.reportingconfig().webeventbucketing().enable()
            elif enable.lower() == 'no':
                self._cli.reportingconfig().webeventbucketing().disable()
            else:
                raise cliexceptions.CliValueError(\
                'Enable can be either \'Yes\' or \'No\'.')

    def reporting_config_centralized(self, enable=DEFAULT, anonymize=DEFAULT):
        """Enable/Disable Centralized Reporting for this WSA appliance.

        reportingconfig > centralized

        Parameters:
        - `enable`: enable Centralized Reporting.
                    'yes' to enable, 'no' to disable
        - `anonymize`: anonymize usernames in reports.
                       'yes' to enable, 'no' to disable

        Example:
        | Reporting Config Centralized | enable=yes | anonymize=no |

        """
        kwargs = {'enable': enable,
                  'anonymize': anonymize}
        self._cli.reportingconfig().centralized(**kwargs)
