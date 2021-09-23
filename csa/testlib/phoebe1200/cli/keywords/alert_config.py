#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/alert_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO, is_yes


class AlertConfig(CliKeywordBase):
    """Configure Cisco IronPort system alerts."""

    def get_keyword_names(self):
        return ['alert_config_new',
                'alert_config_edit',
                'alert_config_delete',
                'alert_config_clear',
                'alert_config_setup',
                'alert_config_print_alerts',
                'alert_config_from_edit',
                'alert_config_from_default',
                ]

    def alert_config_new(self, *args):
        """Add a new email address to send alerts.

        alertconfig > new

        Parameters:
        - `address`: email address to send alerts.
        - `alert_classes`: Alert Classes.
        Specify class numbers according to this table:
        | Class Number | Class Name |
        | 1 | All |
        | 2 | System |
        | 3 | Hardware |
        | 4 | Updater |
        | 5 | Outbreak Filters |
        | 6 | Anti-Virus |
        | 7 | Anti-Spam |
        | 8 | Directory Harvest Attack Prevention |
        | 9 | Release and Support Notifications |
        String of comma separated values. Default value 1.
        - `severity_levels`: Severity Levels. Applicable for all alert classes 
	except Release and Support Notifications.
	Specify level numbers according to this table:
        | Level Number | Level Name |
        | 1 | All |
        | 2 | Critical |
        | 3 | Warning |
        | 4 | Information |
        String of comma separated values. Default value 1.

        Examples:
        | Alert Config New | address=admin@example.com |

        | Alert Config New | address=administrator@example.com |
        | ... | alert_classes=2,3 |
        | ... | severity_levels=1 |

	| Alert Config New | address=administrator@example.com |
        | ... | alert_classes=9 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.alertconfig().new(**kwargs)

    def alert_config_edit(self, *args):
        """Modify alert subscription for an email address.

        alertconfig > edit

        Parameters:
        - `address`: specify either email address to edit or email address
        number.
        - `alert_class`: Alert Class. String. Specify class number (only one)
        according to this table:
        | Class Number | Class Name |
        | 1 | All |
        | 2 | System |
        | 3 | Hardware |
        | 4 | Updater |
        | 5 | Outbreak Filters |
        | 6 | Anti-Virus |
        | 7 | Anti-Spam |
        | 8 | Directory Harvest Attack Prevention |
        | 9 | Release and Support Notifications |
        - `enable`: applicable only if 'alert_class' is selected as 9.
           Enables "Release and Support Notifications". Either 'yes' or 'no'.
           Default is 'no'.
        - `disable`: applicable only if 'alert_class' is selected as 9.
           Disables "Release and Support Notifications". Either 'yes' or 'no'.
           Default is 'no'.
        - `severity_levels`: Severity Levels. Specify level numbers according to
        this table:
        | Level Number | Level Name |
        | 1 | All |
        | 2 | Critical |
        | 3 | Warning |
        | 4 | Information |
        | 5 | None |
        String of comma separated values. Default value 1. Default value 1.
        NOTE: You cannot pick None while also picking other levels.

        Example:
        | Alert Config Edit | address=administrator@example.com |
        | ... | alert_class=1 |
        | ... | severity_levels=1 |

	| Alert Config Edit | address=administrator@example.com |
        | ... | alert_class=9 | enable=yes |

        | Alert Config Edit | address=administrator@example.com |
        | ... | alert_class=9 | enable=no |

        | Alert Config Edit | address=administrator@example.com |
        | ... | alert_class=9 | disable=yes |

        | Alert Config Edit | address=administrator@example.com |
        | ... | alert_class=9 | disable=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.alertconfig().edit(**kwargs)

    def alert_config_clear(self):
        """Remove all email addresses (disable alerts).

        alertconfig > clear

        Returns 0 if cleared some alerts
        Returns -1 if was no one alert configured (nothing to clear).

        Examples:
        | Alert Config Clear |

        | ${result}= | Alert Config Clear |
        | Log | ${result} |
        """

        output = self._cli.alertconfig().clear()
        return output

    def alert_config_delete(self, address):
        """Remove an email address.

        alertconfig > delete

        Parameters:
        - `address`: email address or valid email index to delete.

        Examples:
        | Alert Config Delete | address=admin@example.com |

        | Alert Config Delete | address=1 |
        """

        self._cli.alertconfig().delete(address)

    def alert_config_setup(self,
                           initial_debounce_interval=None,
                           max_debounce_interval=None,
                           auto_support=None,
                           reports=None,
                           max_alerts=None,
                           interface=None):
        """Configure alert settings.

        alertconfig > setup

        Parameters:
        - `initial_debounce_interval`: Initial number of seconds to wait before
        sending a duplicate alert. Enter a value of 0 to disable duplicate alert
        summaries. Default value: 300.
        - `max_debounce_interval`: Maximum number of seconds to wait before
        sending a duplicate alert. Default value: 3600. Note that maximum
        debounce interval cannot be less than the initial value. If option
        `initial_debounce_interval` set to 0, this option should be skipped.
        - `auto_support`: 'Yes' to enable Cisco IronPort AutoSupport, which
        automatically emails system alerts and weekly status reports directly
        to Cisco IronPort Customer Support, or 'No' to disable. Default: 'No'.
        - `reports`: 'Yes' if you want to receive a copy of the weekly
        AutoSupport reports, or 'No'. Setting this option makes sense only if
        `auto_support` is enabled.
        - `max_alerts`: Maximum number of alerts to save. Optional.
        - `interface`: The default interface to be used to deliver alerts. Optional.

        Examples:
        | Alert Config Setup |

        | Alert Config Setup | initial_debounce_interval=500 |
        | ... | max_debounce_interval=1200 |
        | ... | auto_support=Yes |
        | ... | reports=Yes |
        """

        kwargs = {}
        if initial_debounce_interval:
            kwargs['initial_debounce_interval'] = initial_debounce_interval
        if max_debounce_interval:
            kwargs['max_debounce_interval'] = max_debounce_interval
        if auto_support:
            kwargs['auto_support'] = self._process_yes_no(auto_support)
            if is_yes(auto_support):
                if reports:
                    kwargs['reports'] = self._process_yes_no(reports)
        if max_alerts:
            kwargs['max_alerts'] = max_alerts
        if interface:
            kwargs['interface'] = interface
        output = self._cli.alertconfig().setup(**kwargs)
        return (output)

    def alert_config_print_alerts(self):
        """Print configured alerts.

        Examples:
        | Alert Config Print Alerts |

        | ${alerts}= | Alert Config Print Alerts |
        | Log | ${alerts} |
        """

        output = self._cli.alertconfig().print_alerts()
        self._info(output)
        return output

    def alert_config_from_edit(self, address):
        """Edit the From Address of alert emails.

        alertconfig > from > edit

        Parameters:
        - `address`: From Address to be used for alert emails.

        Examples:
        | Alert Config From Edit | sarf@mail.com |
        """

        self._cli.alertconfig().from_address().edit(address)

    def alert_config_from_default(self):
        """Use the System Default From Address.

        alertconfig > from > default

        Examples:
        | Alert Config From Default |
        """

        self._cli.alertconfig().from_address().default()
