#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/backup_config.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class BackupConfig(CliKeywordBase):
    """Configure system configuration backup."""

    def get_keyword_names(self):
        return ['backup_config_view',
                'backup_config_verify',
                'backup_config_schedule',
                'backup_config_cancel',
                'backup_config_status']

    def backup_config_view(self):
        """View backup configuration.

        backupconfig > view

        Examples:
        | Backup Config View |
        """
        out =  self._cli.backupconfig().view()
        self._info(out)
        return out

    def backup_config_verify(self, *args):
        """Edit dynamic host name.

        backupconfig > verify

        Parameters:
            - `ip`: IP address of a machine to transfer data to.
            - `name`: name to identify this appliance.
            - `user`: username to verify the connection.
            - `passwd`: password for user to verify the connection.

        Examples:
        | Backup Config Verify | ip=${DUT_IP} | name=${DUT} | user=admin | passwd=ironport |
        """
        kwargs = self._convert_to_dict(args)
        out =  self._cli.backupconfig().verify(**kwargs)
        self._info(out)
        return out

    def backup_config_schedule(self, *args):
        """Schedule backup configuration.

        backupconfig > schedule

        Parameters:
            - `job_name`: name of the backup that will be scheduled.
            - `backup_type`: type of the backup that will be scheduled:
              Repeating, single or now.
            - `period`: period for scheduling: daily, weekly or monthly.
            - `single_date`: date for the backup schedule. Available in
              case if backup type is single or repeating.
            - `day_of_month`: day of month for the backup schedule.
              Available in case backup period is monthly.
            - `day_of_week`: day of week for the backup schedule. Available
              in case backup period is weekly.
            - `rep_time`: time for backup schedule. Available in case
              backup perion is daily.
            - `ip`: IP address of a machine to transfer data to.
            - `name`: name to identify this appliance.
            - `user`: username to verify the connection.
            - `passwd`: password for user to verify the connection.
            - `backup_all`: Specify if all data should be backed up. Either Yes
              or No.
            - `backup_isq`: Specify if isq data should be backed up. Available
              in case backup_all value is No. Either Yes or No.
            - `backup_email_tracking`:Specify if email tracking
              data should be backed up. Either Yes or No. Available in case
              backup_all value is No.
            - `backup_web_tracking`: Specify if web trackingb data should be
              backed up. Either Yes or No. Available in case backup_all
              value is No.
            - `backup_reporting`: Specify if reporting data should be backed
              up. Either Yes or No. Available in case backup_all value is
              No.            - `backup_policy_quarantine`: Specify if Policy Quarantine data
              should be backed up. Either Yes or No. Available in case backup_all
              value is No.
            - `backup_slbl`: Specify if slbl data should be backed up. Either
              Yes or No. Available in case backup_all value is No
            - `backup_policy_quarantine` : Specify if policy quarantine data should be backed up.
               Either Yes or No. Available in case backup_all value is No

        Examples:
            | Backup Config Schedule |
            | ... | job_name=test_job_sin |
            | ... | backup_type=single |
            | ... | single_date=17/1/2012 1:10:11 |
            | ... | day_of_month=1 |
            | ... | day_of_week=monday |
            | ... | ip=${DUT_IP} |
            | ... | name=${DUT} |
            | ... | user=admin |
            | ... | passwd=ironport |
            | ... | backup_all=No |
            | ... | backup_isq=YES |
            | ... | backup_email_tracking=No |
            | ... | backup_web_tracking=YES |
            | ... | backup_reporting=YES |
            | ... | backup_policy_quarantine=YES |
            | ... | backup_slbl=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.backupconfig().schedule(**kwargs)

    def backup_config_cancel(self, job_name):
        """Cancel backup configuration.

        backupconfig > cancel

        Parameters:
            - `job_name`: name of the backup to be canceled.

        Examples:
            | Backup Config Cancel | test_job_rep |
        """
        self._cli.backupconfig().cancel(job_name)

    def backup_config_status(self):
        """Backup status configuration.

        backupconfig > status

        Examples:
        | Backup Config Status |
        """
        out =  self._cli.backupconfig().status()
        self._info(out)
        return out

