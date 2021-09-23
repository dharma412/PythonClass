#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/antivirus_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class AntivirusConfig(CliKeywordBase):
    """
    antivirusconfig

    Edit Anti-Virus settings.

    antivirusconfig <engine> setup enable [options]
    antivirusconfig <engine> setup disable

        engine  - sophos|mcafee
            Anti-Virus engine to use.

        options - Various options to modify antivirusconfig parameters
             --scan-timeout    To specify the Anti-Virus scanning timeout (in
                               seconds). Integer between 30 to 900.
    """

    def get_keyword_names(self):
        return ['antivirus_config_tune',
                'antivirus_config_sophos_setup',
                'antivirus_config_sophos_tune',
                'antivirus_config_sophos_pdf',
                'antivirus_config_mcafee_setup'
                ]

    def antivirus_config_tune(self, *args):
        """
        This will Set global Tune option for antivirus

        antivirusconfig -> tune

        *Parameters*:
        - `conf` : Specify Anti-Virus server performance tuning as per table
          |1| Default - moderate settings
          |2| Fast - favor system throughput - no timeout handling, aggressive scanning
          |3| Custom
        - `num_msg` : Maximum number of messages concurrently processed in the work-queue
        - `traffic` : Limit traffic when aggregate message size over (in bytes)
        - `rescan` : Rescan messages, if necessary, to avoid timeouts?
                     Either 'yes' or 'no'
        - `num_retries` : Number of retries to allow if Anti-Virus server restarts
        - `sleep_time` : Time to sleep before rescanning a message (in secs)

        *Examples*:

        | Antivirus Config tune | conf=1 |
        | Antivirus Config tune | conf=3 | num_msg=5 | rescan=yes |

        """

        kwargs = self._convert_to_dict(args)
        self._cli.antivirusconfig(vendor=None).tune(**kwargs)

    def antivirus_config_sophos_setup(self, *args):
        """
        This will setup sophos configuration

        antivirusconfig -> sophos -> setup

        *Parameters*:
        - `use_av` : enable Antivirus
                     Either 'yes' or 'no'
        - `scan_timeout`: scanning timeout in secs
                          Value must be an integer from 30 to 900
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'

        *Examples*:

        | Antivirus Config Sophos Setup | use_av=yes | scan_timeout=40 |
        | Antivirus Config Sophos Setup | use_av=no | confirm_disable=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antivirusconfig(vendor='sophos').setup(**kwargs)

    def antivirus_config_sophos_tune(self, *args):
        """
        This will tune sophos settings

        antivirusconfig -> sophos -> tune

        *Parameters*:
        - `num_obj` : Number of low-level scanning objects within the
                      Anti-virus server (usually five)
        - `scan_policy` : server scanning policy
          |1| Default - moderate settings
          |2| Fast - Early exit on virus and unscannable errors
          |3| Aggressive - Prevent repair actions in server

        *Examples*:

        | Antivirus Config Sophos tune | num_obj=10 |
        | Antivirus Config Sophos tune | scan_policy=2 |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antivirusconfig(vendor='sophos').tune(**kwargs)

    def antivirus_config_sophos_pdf(self, *args):
        """
        This will edit the configuration of Sophos PDF settings

        antivirusconfig -> Sophos -> pdf

        *Parameters*:
        - `report_clean` : Report unscannable PDFs as clean?
                           Either 'yes' or 'no'

        *Examples*:

        | Antivirus Config Sophos pdf | report_clean=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antivirusconfig(vendor='sophos').pdf(**kwargs)

    def antivirus_config_mcafee_setup(self, *args):
        """
        This will setup mcafee configuration

        antivirusconfig -> mcafee -> setup

        *Parameters*:
        - `use_av` : enable Antivirus
                     Either 'yes' or 'no'
        - `scan_timeout`: scanning timeout in secs
                          Value must be an integer from 30 to 900
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'

        *Examples*:

        | Antivirus Config Mcafee Setup | use_av=yes | scan_timeout=50 |
        | Antivirus Config Mcafee Setup | use_av=no | confirm_disable=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antivirusconfig(vendor='mcafee').setup(**kwargs)
