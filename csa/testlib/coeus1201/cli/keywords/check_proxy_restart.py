#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/check_proxy_restart.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class CheckProxyRestart(CliKeywordBase):
    """Checks if changes to the current config requires a proxy restart or not.
    """

    def get_keyword_names(self):
        return [
                'check_proxy_restart',
               ]

    def check_proxy_restart(self):
        """Checks if changes to the
                             current config requires a proxy restart or not.

        Parameters:
           None

        Returns:
        -`NO_CHANGE`- corresponds to command output -
                       `There are no changes in current config`.

        -`RESTART_NOT_REQUIRED` - corresponds to command output -
          `In order to process these changes proxy
                                    restart will not be required`.

        -`RESTART_AFTER_COMMIT` - corresponds to command output -
           `Warning: In order to process these changes,
            the proxy process will restart after Commit.
            This will cause a brief interruption in service.
            Additionally, the authentication cache will be cleared,
            which might require some users to authenticate again.`


        Examples:
        | ${out} = Check Proxy Restart |

        """
        return self._cli.checkproxyrestart()
