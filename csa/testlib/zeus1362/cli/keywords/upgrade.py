#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/upgrade.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Upgrade(CliKeywordBase):
    """Select and install an upgrade."""
    def get_keyword_names(self):
        return ['upgrade',
                'upgrade_downloadinstall',
                'upgrade_download',
                'upgrade_canceldownload',
                'upgrade_delete',
                'upgrade_downloadstatus',
                'upgrade_install', ]

    def upgrade_downloadinstall(self,
                                version=None,
                                seconds=0,
                                save_cfg='',
                                include_pw='',
                                email='',
                                email_addr=''):
        """Perform an upgrade downloadinstall.
        *Parameters:*
        - `version`: version to upgrade SMA to. Should be in format N.X.Y-ZZZ
        (i.e., 8.1.0-400). If unspecified do an upgrade-in-place.
        - `seconds`: number of seconds to close connections before reboot.
        - `save_cfg`: specify 'yes' to save current configuration to the
        configuration directory before upgrading, or 'no' if you don't want to
        save it.
        - `include_pw`: specify 'yes' if you want to include passwords in
        configuration file, or 'no' if you don't. Please be aware that a
        configuration without passwords will fail when reloaded with loadconfig.
        - `email`: specify 'yes' if you want saved configuration to be sent by
        email to you or 'no' if you don't.
        - `email_addr`: email address configuration to be sent to. Multiple
        email addresses separated by commas are allowed.

        *Examples:*
        | Upgrade Downloadinstall |
        | ... | 8.1.0-400 |
        | ... | seconds=10 |
        | ... | save_cfg=yes |
        | ... | include_pw=yes |
        | ... | email=yes |
        | ... | email_addr=user@cisco.com |
        or
        | Upgrade Downloadinstall |
        | ... | 8.1.0-400 |
        | ... | seconds=10 |
        | ... | save_cfg=yes |
        | ... | include_pw=yes |
        | ... | email=yes |
        | ... | email_addr=user@cisco.com |
        """

        kwargs = {}
        if save_cfg:
            kwargs['save_cfg'] = self._process_yes_no(save_cfg)
            if include_pw:
                kwargs['include_pw'] = self._process_yes_no(include_pw)
            if email:
                kwargs['email'] = self._process_yes_no(email)
                if email_addr:
                    kwargs['email_addr'] = email_addr

        self._cli.upgrade().downloadinstall(version, seconds, **kwargs)

    def upgrade(self, version=None, seconds=0, *args):
        self._warn('Upgrade keyword is deprecated. Use Upgrade Downloadinstall instead')
        kwargs = self._convert_to_dict(args)
        self.upgrade_downloadinstall(version, seconds, **kwargs)

    def upgrade_download(self, version=None, cancel='', delete=''):
        """Perform an upgrade download.
        *Parameters:*
        - `version`: version of SMA to download . Should be in format N.X.Y-ZZZ
        (i.e., 8.1.0-400). If unspecified do an upgrade-in-place.
        - `delete`: specify 'yes' or 'no' to delete previously downloaded image.
        - `cancel': confirm canceling any upgrade
                    download that is currently in progress.

        *Examples:*
        | Upgrade Download |
        | ... | 8.1.0-400 |
        | ... | delete=yes |

        """

        kwargs = {}
        if delete:
            kwargs['delete'] = self._process_yes_no(delete)
        if cancel:
            kwargs['cancel'] = self._process_yes_no(cancel)

        self._cli.upgrade().download(version, **kwargs)

    def upgrade_canceldownload(self, cancel=''):
        """Cancel upgrade.
        *Parameters:*
        - `cancel': confirm canceling any upgrade
                    download that is currently in progress.

        *Examples:*
        | Upgrade Canceldownload | cancel=Yes |
        """

        kwargs = {}
        if cancel:
            kwargs['cancel'] = self._process_yes_no(cancel)

        self._cli.upgrade().canceldownload(**kwargs)

    def upgrade_delete(self, delete=''):
        """Delete previously downloaded image.
        *Parameters:*
        - `delete': confirm deleting previously downloaded image.
        *Examples:*
        | Upgrade Delete | delete=Yes |
        """

        kwargs = {}
        if delete:
            kwargs['delete'] = self._process_yes_no(delete)

        self._cli.upgrade().delete(**kwargs)

    def upgrade_downloadstatus(self):
        """Return status of download process.

        *Return:*
            Returns integer that indicates the percentage of download process.
            Returns 100 if download is complete.

        *Examples:*
        | ${out}= | Upgrade Downloadstatus |
        """

        return self._cli.upgrade().downloadstatus()

    def upgrade_install(self,
                        version=None,
                        seconds=0,
                        save_cfg='',
                        include_pw='',
                        email='',
                        email_addr=''):

        """Perform an install of already downloaded image.

        *Parameters:*
        - `seconds`: number of seconds to close connections before reboot.
        - `save_cfg`: specify 'yes' to save current configuration to the
        configuration directory before upgrading, or 'no' if you don't want to
        save it.
        - `include_pw`: specify 'yes' if you want to include passwords in
        configuration file, or 'no' if you don't. Please be aware that a
        configuration without passwords will fail when reloaded with loadconfig.
        - `email`: specify 'yes' if you want saved configuration to be sent by
        email to you or 'no' if you don't.
        - `email_addr`: email address configuration to be sent to. Multiple
        email addresses separated by commas are allowed.

        *Examples:*
        | Upgrade Install |
        | ... | seconds=10 |
        | ... | save_cfg=yes |
        | ... | include_pw=yes |
        | ... | email=yes |
        | ... | email_addr=user@cisco.com |
        """

        kwargs = {}
        if save_cfg:
            kwargs['save_cfg'] = self._process_yes_no(save_cfg)
            if include_pw:
                kwargs['include_pw'] = self._process_yes_no(include_pw)
            if email:
                kwargs['email'] = self._process_yes_no(email)
                if email_addr:
                    kwargs['email_addr'] = email_addr

        self._cli.upgrade().install(seconds, **kwargs)
