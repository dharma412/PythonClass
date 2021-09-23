# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/load_license.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from sal.exceptions import ConfigError
from common.util.misc import Misc
from common.util.systools import SysTools

class LoadLicense(CliKeywordBase):
    """
        cli -> loadlicense
    """
    def get_keyword_names(self):
        return ['load_license',
                ]

    def  load_license(self,
                           conf=None,
                           conf_file=None,
                           paste_conf=None
                           ):
        """
        cli -> loadlicense

        Parameters:
        - `conf`: Used to specify how the input will be entered.
                  Either file or paste_via_cli.
                  Required parameter.

        - `conf_file`: This parameter is used to specify the
                       name of the configuration file.
                       This file is assumed to exist under
                       /data/pub/configuration directory of DUT.
                       This is a required parameter in case conf=file.

        - `paste_conf`: This parameter is used to specify the
                       actual contents of a configuration file
                       which is to be inputed from the CLI session.
                       This is a required parameter in case conf=paste_via_cli

        Examples:

        |  Load License |
        | ... |   conf=file  |
        | ... |   conf_file=super.xml  |

        |  Copy File To DUT  %{SARF_HOME}/tests/testdata/virtual/${name}
                                              /data/pub/configuration/ |

        | ... | Load License  |
        | ... |  conf=paste_via_cli  |
        | ... |   paste_conf=${conf_output}  |

        """

        Misc(self.dut, self.dut_version).wait_until_ready(timeout=300)

        if not (SysTools(self.dut, self.dut_version)._is_dut_a_virtual_model()):
            self._info('Its not a valid Virtual Model, returning ...')
            return

        if not conf:
            raise ConfigError, 'loadlicense: Attribute value\
                                 for conf paramter is required'
        else:
            if conf == 'file':
                conf = 'Load from file'
                if not conf_file:
                    raise ConfigError, 'loadlicense: Attribute value for\
                                        conf_file parameter is required\
                                        when conf parameter is set to file'
                else:
                    return self._cli.loadlicense()._load_license_from_file\
                    (filename=conf_file)

            elif conf == 'paste_via_cli':
                conf = 'Paste via CLI'
                if not paste_conf:
                    raise ConfigError, 'loadlicense: Attribute value for\
                                     paste_conf parameter is required when \
                                     conf parameter is set to paste_via_cli'
                else:
                    return self._cli.loadlicense()._load_license_from_cli\
                    (paste_conf=paste_conf)
