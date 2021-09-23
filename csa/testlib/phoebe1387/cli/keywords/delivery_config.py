#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/delivery_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class DeliveryConfig(CliKeywordBase):
    """
    Configure delivery parameters.
    CLI command: deliveryconfig
    """

    def get_keyword_names(self):
        return ['delivery_config_setup',
                'delivery_config_get_settings',]

    def delivery_config_setup(self, *args):
        """
        Edit delivery configuration.
        CLI command: deliveryconfig > setup

        *Parameters:*
        - `ifname`: Default interface to deliver mail.
        - `enable_poss_delivery`: Enable "Possible Delivery". YES or NO. YES by default.
        - `max_outbound_concur`: Default system wide maximum outbound message delivery concurrency. String. Optional.
        - `max_tls_outbound_concur`: Default system wide TLS maximum outbound message delivery concurrency. String. Optional.
        - `attempt_to_connect_without_TLS`: Should an attempt to connect without TLS be made when TLS concurrency
                                            limit has been reached. YES or NO. YES by default.

        *Return:*
        None

        *Examples:*
        | Delivery Config Setup |
        | ... | ifname=Management |
        | ... | enable_poss_delivery=NO |
        | ... | max_outbound_concur=1000 |
        | ... | max_tls_outbound_concur=500 |

        | Delivery Config Setup |
        | ... | ifname=Auto |
        | ... | enable_poss_delivery=YES |
        | ... | max_outbound_concur=2000 |
        | ... | max_tls_outbound_concur=1000 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.deliveryconfig().setup(**kwargs)

    def delivery_config_get_settings(self, as_dictionary='y'):
        """
        Get delivery configuration settings.
        CLI command: deliveryconfig

        *Parameters:*
        None

        *Return:*
        Dictionary if 'as_dictionary' is YES.
        Dictionary has keys:
        'ifname', 'poss_delivery', 'max_outbound_concur', 'max_tls_outbound_concur'.

        Raw output if 'as_dictionary' is NO

        *Examples:*
        | ${settings}= | Delivery Config Get Settings | as_dictionary=no |
        | Log | ${settings} |

        | ${settings}= | Delivery Config Get Settings |
        | Log Dictionary | ${settings} |
        | ${pd}= | Get From Dictionary | ${settings} | poss_delivery |
        | Should Be Equal | ${pd} | Enabled |
        """
        return self._cli.deliveryconfig().\
        get_settings(as_dictionary=as_dictionary)
