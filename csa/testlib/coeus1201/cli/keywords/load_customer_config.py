# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/load_customer_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from sal.exceptions import ConfigError

class LoadCustomerConfig(CliKeywordBase):
    """
        cli -> loadcustomerconfig
    """
    def get_keyword_names(self):
        return [
            'load_customer_config',
        ]

    def  load_customer_config(self,
        load_network_settings='Y',
        conf='',
        email_addr='',
        conf_file='',
        paste_conf='',
        ):
        """
        cli -> loadcustomerconfig

        Parameters:
        - `load_network_settings`: 'Y' or 'N'
        - `conf`: Used to specify how the input will be entered.
                  Either file or paste_via_cli.
                  Required parameter.

        - `conf_file`: This parameter is used to specify the
                       name of the configuration file.
                       This is a required parameter in case conf=file.

        - `paste_conf`: This parameter is used to specify the
                       actual contents of a configuration file
                       which is to be inputted from the CLI session.
                       This is a required parameter in case conf=paste_via_cli.

        - `email_addr`: This parameter is used to specify a valid email address.
                        This is a required parameter.

        Exceptions:
        `IafEmailAddrError` : For invalid email address.
        `SarfFileNotFoundError`: For invalid configuration file names specified.
        `SarfConfigurationLoadError`: For invalid configuration input.

        Examples:

        | Load Customer Config  |
        | ... | load_network_settings=Y |
        | ... | conf=file  |
        | ... | conf_file=test1.xml  |
        | ... | email_addr=administrator@example.com  |

        | ${conf_output}=  Run on DUT  cat /data/pub/configuration/test2.xml  |

        | ... | Load Customer Config  |
        | ... | conf=paste_via_cli  |
        | ... | paste_conf=${conf_output}  |
        | ... | email_addr=test@test.com  |

        """
        if not email_addr:
            raise ConfigError, 'loadcustomerconfig: Attribute value for\
                                     email_addr parameter is required'

        if not conf:
            raise ConfigError, 'loadcustomerconfig: Attribute value\
                                 for conf paramter is required'
        else:
            if conf == 'file':
                conf = 'Load from file'
                if not conf_file:
                    raise ConfigError, 'loadcustomerconfig: Attribute value for\
                                        conf_file parameter is required\
                                        when conf parameter is set to file'
                else:
                    self._cli.loadcustomerconfig(). \
                    _enter(load_network_settings). \
                    _load_choice(conf). \
                    _load_customerconfig_from_file(conf_file).\
                    _enter(email_addr)

            elif conf == 'paste_via_cli':
                conf = 'Paste via CLI'
                if not paste_conf:
                    raise ConfigError, 'loadcustomerconfig: Attribute value for\
                                     paste_conf parameter is required when \
                                     conf parameter is set to paste_via_cli'
                else:
                    self._cli.loadcustomerconfig(). \
                    _enter(load_network_settings). \
                    _load_choice(conf). \
                    _load_customerconfig_from_cli(paste_conf). \
                    _enter(email_addr)
