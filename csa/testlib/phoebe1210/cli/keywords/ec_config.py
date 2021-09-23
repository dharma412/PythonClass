# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/ec_config.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class ecconfig(CliKeywordBase):
    """
    cli -> ecconfig
    ecconfig: Edit configuration for the Enrollment Client.
    """

    def get_keyword_names(self):
        return ['ecconfig_setup']

    def ecconfig_setup(self, *args):
        """
        This will edit the configuration of Enrollment Client.

        ecconfig -> setup

        Parameters:
        - `use_enrollment_server` : to use non-default Enrollment server. Either 'yes' or 'no'
        - `new_enrollment_server` : details of new Enrollment server in the format: <server_name:port>,where
		    server_name - Enrollment server hostname or IPv4 address
            port - Port on Enrollment server to connect to
			Make sure to provide proper server_name and port number.

        Examples:
        | ecconfig setup | use_enrollment_server=yes | new_enrollment_server=10.76.69.207:22

        """
        kwargs = self._convert_to_dict(args)
        self._cli.ecconfig().setup(**kwargs)
