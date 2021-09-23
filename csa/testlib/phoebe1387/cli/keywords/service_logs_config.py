#!/usr/bin/env python
from common.cli.clicommon import CliKeywordBase

class ServiceLogsConfig(CliKeywordBase):
    """
    Manage Service Logs configuration.
    CLI command: servicelogsconfig
    """

    def get_keyword_names(self):
        return ['service_logs_config_setup',
                'service_logs_config_full',
                'service_logs_config_status']

    def service_logs_config_setup(self, *args):
        """Setup service logs config

        CLI command: servicelogsconfig > setup

        *Parameters:*
        - `share_stats`: Share limited data with Service Logs Information Service.
                         YES or NO.

        *Return:*
        None

        *Examples:*
        | Servicelogs Config Setup | share_stats=yes |
        | Servicelogs Config Setup | share_stats=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.servicelogsconfig().setup(**kwargs)

    def service_logs_config_status(self):
        """This keyword to get the current status of the service logs config
        *Return:*
        Enabled or Disabled
        *Examples:*
        $status=    |ServiceLogs Config Status|
        """
        return self._cli.servicelogsconfig().status()

    def service_logs_config_full(self, *args):
        """fullsenderbaseconfig hidden command

        CLI command: senderbaseconfig > fullsenderbaseconfig
        Note: _fullsenderbaseconfig_ is a hidden sub-command.

        *Parameters:*
        - `max_sampling_rate`: Enter the maximum rate of sampling messages for
                               improved efficacy (value in percent upto two
                               places after decimal point)
        *Return:*
        None

        | Senderbase Config Full |
        | ... | max_sampling_rate=7.05 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.servicelogsconfig().fullsenderbaseconfig(**kwargs)
