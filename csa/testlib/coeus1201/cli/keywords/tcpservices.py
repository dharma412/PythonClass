# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/tcpservices.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class Tcpservices(CliKeywordBase):
    """
    Returns output of cli/tcpservices
    """
    def get_keyword_names(self):
        return [
            'tcpservices',
        ]

    def tcpservices(self, option=None):
        """Tcpservices

        Returns the output of cli command 'tcpservices'

        Parameters:
        - 'option': Either \'system\' or \'features\' or
        \'info\'.

        Example:
        | Tcpservices | #Display information about open TCP/IP services. |

        | Tcpservices | option=system | #Display list of current system processes only. |

        | Tcpservices | option=features | #Display list of current feature processes only. |

        | Tcpservices | option=info | #Display information defining the process names that may appear. |
        """

        return str(self._cli.tcpservices(option))
