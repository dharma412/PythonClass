# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/graymail_config.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class graymailconfig(CliKeywordBase):
    """
    cli -> graymailconfig

    Edit configuration for the GrayMail engine.
    """

    def get_keyword_names(self):
        return [
            'graymailconfig_setup',
            'graymailconfig_batch_setup',
            'graymailconfig_is_graymail_enabled',
        ]

    def graymailconfig_setup(self, *args):
        """
        This will edit the configuration of GrayMail engine

        cli -> graymailconfig -> setup

        Parameters:
        - `use_graymail_detection`:        Whether to enable Graymail Detection or not (Default: Yes).
        - `maximum_message_scanning_size`:    Maximum Message Size to Scan (Add a trailing K for kilobytes,
                                              M for megabytes, or no letters for bytes.)
                                              Default: 1M. Recommened: Less than 10M
        - `message_scanning_timeout`:         Timeout for Scanning Single Message (in seconds).
        - `use_graymail_safe_unsubscribe`: Whether to use Graymail Safe Unsubscribe or not (Default: Yes).

        Examples:
        Enable graymail with default settings
        | GraymailConfig Setup |

        Enable graymail with user provided settings
        | GraymailConfig Setup |
        | ... | use_graymail_detection=yes |
        | ... | use_graymail_safe_unsubscribe=no |

        | GraymailConfig Setup |
        | ... | use_graymail_detection=yes |
        | ... | use_graymail_safe_unsubscribe=no |

        | GraymailConfig Setup |
        | ... | use_graymail_detection=Yes |
        | ... | maximum_message_scanning_size=2M |
        | ... | message_scanning_timeout=30 |
        | ... | use_graymail_safe_unsubscribe=No |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.graymailconfig().setup(**kwargs)

    def graymailconfig_batch_setup(self, *args):
        """
        This keyword runs the 'graymailconfig setup' command in batch mode.

        CLI -> graymailconfig setup enable
            -> graymailconfig setup disable
            -> graymailconfig setup enable --max_scan_size=5M --scan_timeout=45 --unsubscription_enable=1

        *Parameters:*
        - `action`: Whether to enable or disable Graymail scanning. Allowed values: enable or disable

        Below parameters are valid only if 'action' param is set to 'enable'.
        - `max_scan_size`: Maximum message size for Graymail scanning. (Add a trailing K for kilobytes,
                           M for megabytes, or no letters for bytes.)
                           Default: 1M. Recommended: Less than 10M
        - `scan_timeout`:  Timeout for Scanning Single Message (in seconds).
                           Accepted values: From 1 to 60.
        - `unsubscription_enable`: Whether to use Graymail Safe Unsubscribe or not.
                                   Accepted values: 0 or 1
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.graymailconfig().batch_setup(**kwargs)

    def graymailconfig_is_graymail_enabled(self):
        """
        This keyword will return the status of the Graymail Engine (enabled/disabled).

        cli -> graymailconfig

        Parameters:
        None

        Examples:
        | ${is_graymail_enabled}= | Graymailconfig Is Graymail Enabled |

        """
        return self._cli.graymailconfig().is_graymail_enabled()
