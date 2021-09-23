#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/diskquota_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class diskquotaconfig(CliKeywordBase):
    """
    cli -> diskquotaconfig

    Configures or Get the disk quotas for following services.
    - Spam Quarantine (EUQ)
    - Policy, Virus & Outbreak Quarantines
    - Reporting
    - Tracking
    - Misc
    """

    def get_keyword_names(self):
        return ['diskquota_config_get_quotas',
                'diskquota_config_get_service_quota',
                'diskquota_config_get_usages',
                'diskquota_config_get_service_usage',
                'diskquota_config_get_total_available_quotas',
                'diskquota_config_get_total_allocated_quotas',
                'diskquota_config_get_total_unallocated_quotas',
                'diskquota_config_get_total_usages',
                'diskquota_config_edit_quotas',
                'diskquota_config_batch']

    def diskquota_config_get_quotas(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns disk quotas for all the services including total used quota.

        *Parameters:*
        - None

        *Return:*
        A dictionary in a format shown below:
        quotas: { service1 : value1,
                 service2 : {
                     sub_service1: sub_value1,
                     sub_service2: sub_value2,
                 },
                 service2 : value2,
            }

        *Example:*
        | ${quotas}= | Diskquota Config Get Quotas |
        | Log         | ${quotas} |
        """
        return self._cli.diskquotaconfig().get_quotas()

    def diskquota_config_get_service_quota(self, service):
        """This keyword executes the CLI->diskquotaconfig command
        and returns disk quota for a specific service.

        *Parameters:*
        - service: Name of the service.
        Options are:
        | Total |
        | Spam Quarantine |
        | Reporting |
        | Tracking |
        | Miscellaneous Files |
        | Policy Virus Outbreak Quarantines |

        *Return:*
        Current configured disk quota for a service.

        *Example:*
        | ${service_quota}= | Diskquota Config Get Service Quota |
        | ... | Spam Quarantine |
        | Log | ${service_quota} |
        """
        return self._cli.diskquotaconfig().get_service_quota(service)

    def diskquota_config_get_usages(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns disk usages for all the services including total used quota.

        *Parameters:*
        - None

        *Return:*
        A dictionary in a format shown below:
        quotas: { service1 : value1,
                 service2 : {
                     sub_service1: sub_value1,
                     sub_service2: sub_value2,
                 },
                 service2 : value2,
            }

        *Example:*
        | ${usages}= | Diskquota Config Get Usages |
        | Log         | ${usages} |
        """

        return self._cli.diskquotaconfig().get_usages()

    def diskquota_config_get_service_usage(self, service):
        """This keyword executes the CLI->diskquotaconfig command
        and returns disk usage for a specific service.

        *Parameters:*
        - service: Name of the service.
        Options are:
        | Total |
        | Spam Quarantine |
        | Reporting |
        | Tracking |
        | Miscellaneous Files |
        | Policy Virus Outbreak Quarantines |

        *Return:*
        Current configured disk quota for a service.

        *Example:*
        | ${service_usage}= | Diskquota Config Get Service Usage |
        | ... | Spam Quarantine |
        | Log | ${service_usage} |
        """
        return self._cli.diskquotaconfig().get_service_usage(service)

    def diskquota_config_get_total_available_quotas(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns the total disk quota available on the appliance.

        *Parameters:*
        - None

        *Return:*
        Total disk quota available on the appliance.

        *Example:*
        | ${total_available_quotas}= | Diskquota Config Get Total Available Quotas |
        | Log | ${total_available_quotas} |
        """
        return self._cli.diskquotaconfig().get_total_available_quotas()

    def diskquota_config_get_total_allocated_quotas(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns the total allocated disk quota for all the services.

        *Parameters:*
        - None

        *Return:*
        Total configured disk quota for all the servies.

        *Example:*
        | ${total_allocated_quotas}= | Diskquota Config Get Total Allocated Quotas |
        | Log | ${total_allocated_quotas} |
        """
        return self._cli.diskquotaconfig().get_total_allocated_quotas()

    def diskquota_config_get_total_unallocated_quotas(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns the total unallocated disk quota on the appliance.

        *Parameters:*
        - None

        *Return:*
        Total remaining disk quota on the appliance.

        *Example:*
        | ${total_unallocated_quotas}= | Diskquota Config Get Total Unallocated Quotas |
        | Log | ${total_unallocated_quotas} |
        """
        return self._cli.diskquotaconfig().get_total_unallocated_quotas()

    def diskquota_config_get_total_usages(self):
        """This keyword executes the CLI->diskquotaconfig command
        and returns the total used disk spave by all the services.

        *Parameters:*
        - None

        *Return:*
        Total configured used disk space by all the servies.

        *Example:*
        | ${total_usages}= | Diskquota Config Get Total Usages |
        | Log | ${total_usages} |
        """
        return self._cli.diskquotaconfig().get_total_usages()

    def diskquota_config_edit_quotas(self, *args):
        """This keyword edits the disk quota for the following services:
        - 1. Spam Quarantine (EUQ)
        - 2. Policy, Virus & Outbreak Quarantines
        - 3. Reporting
        - 4. Tracking
        - 5. Misc

        CLI: diskquotaconfig -> edit

        *Parameters:*
        - `service`:    Enter the number of the service for which you would like to edit disk quota.
                        If not provided will use the default one.
        - `quota_size`: Enter the new disk quota size. Must be an integer.
                        If not provided will use the default value.

        *Examples:*
        | Diskquota Config Edit Quotas | service=3 | quota_size=7 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.diskquotaconfig().edit_quotas(**kwargs)

    def diskquota_config_batch(self, *args):
        """This keyword runs the 'diskquotaconfig edit' command in
        batch mode for a given service.

        CLI: diskquotaconfig edit --<service_name> <disk_quota>

        *Parameters:*
        - `service`:    Name of the service for which diskquota will be edited.
                        Allowed services are:
                            'euq', 'pvo', 'reporting', 'tracking', 'misc'
        - `disk_quota`: New disk quota size. Must be an integer.

        *Examples:*
        | Disk Quota Config Batch | service=euq | disk_quota=10 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.diskquotaconfig().batch(**kwargs)
