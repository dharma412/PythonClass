#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/upgrade.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
                                seconds=5,
                                proceed_upgrade="YES",
                                *args):
        """Perform an upgrade downloadinstall.

        Parameters:
        - `proceed_upgrade` : proceed with upgrade, either 'YES' or 'NO'
        - `version`: version to upgrade ESA to. Should be in format N.X.Y-ZZZ
        (i.e., 8.0.0-611). If unspecified do an upgrade-in-place.
        - `seconds`: number of seconds to close connections before reboot.
        - `save_cfg`: specify 'yes' to save current configuration to the
        configuration directory before upgrading, or 'no' if you don't want to
        save it.
        - `save_pw`: Choose the password option. (Default: 3)
                Options are:
                    1. Mask passwords
                    2. Encrypt passwords
                    3. Plain passwords
        - `email_cfg`: specify 'yes' if you want saved configuration to be sent by
        email to you or 'no' if you don't.
        - `email_addr`: email address configuration to be sent to. Multiple
        email addresses separated by commas are allowed.

        Examples:

        | Upgrade |
        | ... | 8.0.0-615 |
        | ... | 10 |
        | ... | YES |
        | ... | save_cfg=yes |
        | ... | save_pw=yes |
        | ... | email_cfg=yes |
        | ... | email_addr=user@cisco.com |

        or

        | Upgrade Downloadinstall |
        | ... | 8.0.0-615 |
        | ... | 10 |
        | ... | YES |
        | ... | save_cfg=yes |
        | ... | save_pw=yes |
        | ... | email_cfg=yes |
        | ... | email_addr=user@cisco.com |
        """

        kwargs = self._convert_to_dict(args)
        return self._cli.upgrade().downloadinstall(version, seconds, proceed_upgrade, **kwargs)

    # Symlink for backward compatibility
    upgrade = upgrade_downloadinstall

    def upgrade_download(self, version, proceed_upgrade, *args):
        """Perform an upgrade download.

        Parameters:
        - `proceed_upgrade` : proceed with upgrade, either 'YES' or 'NO'
        - `version`: version of ESA to download . Should be in format N.X.Y-ZZZ
        (i.e., 8.0.0-611). If unspecified do an upgrade-in-place.
        - `delete`: specify 'yes' or 'no' to delete previously downloaded image.

        Examples:

        | Upgrade Download |
        | ... | 8.0.0-615 |
        | ... | YES |
        | ... | delete=yes |

        """
        kwargs = self._convert_to_dict(args)
        return self._cli.upgrade().download(version, proceed_upgrade, **kwargs)

    def upgrade_canceldownload(self, cancel=True):
        """Cancel upgrade.

        Parameters:
        - `cancel': specify ${True} or ${False} to cancel any upgrade
                    download that is currently in progress.

        Examples:

        | Upgrade Canceldownload |
        | ... | cancel=${True} |

        """
        return self._cli.upgrade().canceldownload(cancel)

    def upgrade_delete(self, delete=True):
        """Delete previously downloaded image.

        Parameters:
        - `delete': specify ${True} or ${False} to delete previously downloaded image.

        Examples:

        | Upgrade Delete |
        | ... | delete=${True} |

        """
        return self._cli.upgrade().delete(delete)

    def upgrade_downloadstatus(self):
        """Return status of download process.

        Return:
            Returns integer that indicates the percentage of download process.
            Returns 100 if download is complete.

        Examples:

        | Upgrade Downloadstatus |

        """
        return self._cli.upgrade().downloadstatus()

    def upgrade_install(self,
                        seconds=5,
                        proceed_upgrade="YES",
                        *args):
        """Perform an install of already downloaded image.

        Parameters:
        - `proceed_upgrade` : proceed with upgrade, either 'YES' or 'NO'
        - `seconds`: number of seconds to close connections before reboot.
        - `save_cfg`: specify 'yes' to save current configuration to the
        configuration directory before upgrading, or 'no' if you don't want to
        save it.
        - `save_pw`: specify 'yes' if you want to include passwords in
        configuration file, or 'no' if you don't. Please be aware that a
        configuration without passwords will fail when reloaded with loadconfig.
        - `email_cfg`: specify 'yes' if you want saved configuration to be sent by
        email to you or 'no' if you don't.
        - `email_addr`: email address configuration to be sent to. Multiple
        email addresses separated by commas are allowed.

        Examples:

        | Upgrade Install |
        | ... | 10 |
        | ... | YES |
        | ... | save_cfg=yes |
        | ... | save_pw=yes |
        | ... | email_cfg=yes |
        | ... | email_addr=user@cisco.com |
        """

        kwargs = self._convert_to_dict(args)
        return self._cli.upgrade().install(seconds, proceed_upgrade, **kwargs)
