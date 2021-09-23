from common.cli.clicommon import CliKeywordBase


class techsupport(CliKeywordBase):
    """This is the cli commandfor techsupport

    Enable or disable remote service access to your system by a
    Cisco IronPort Customer Support representative, either using
    ssh access or setting up a secure tunnel.
    Cli -> Techsupport

    The variour options are
    - `sshaccess`:Allow a Cisco IronPort Customer Support representative to rem
    otely access your system, without establishing a tunnel.
    - `tunnel` - Allow a Cisco IronPort Customer Support representative to
    remotely access your system, and establish a secure tunnel for
    communication.
    - `status` - Display the current techsupport status.
    """

    def get_keyword_names(self):
        return ['techsupport_sshaccess',
                'techsupport_tunnel',
                'techsupport_disable',
                'techsupport_status',
                ]

    def techsupport_sshaccess(self, *args):
        """ This option helps in allowing a Cisco IronPort Customer Support
        representative to remotely access your system, without establishing a
        tunnel.
        *Parameters*
        -`temp_pwd`: A temporary password for customer support to use.
                   - the password must be between 6 and 128 characters long;
                   - it cannot be blank or consist only of spaces;
                   - it must be different from your password.
        -`confirm` : To confirm if we want to enable the ssh access.
                   Value can be YES or NO
        -`password_option`:A random seed string is required for this operation
                   1. Generate a random string to initialize secure communication (recommended)
                   2. Enter a random string
                   Value can be "random_generated" or "user_input"

        *Example*
        | Techsupport Sshaccess | temp_pwd='123456' | confirm=YES | password_option = random_generated

        """
        kwargs = self._convert_to_dict(args)
        return str(self._cli.techsupport().sshaccess(**kwargs))

    def techsupport_tunnel(self, *args):
        """ This option helps in allowing a Cisco IronPort Customer Support
            representative to remotely access your system, and establish a
            secure tunnel for communication
        *Parameters*
        -`temp_pwd`: A temporary password for customer support to use.
                   - the password must be between 6 and 128 characters long;
                   - it cannot be blank or consist only of spaces;
                   - it must be different from your password.
        -`port_number`: The port number for tunnel connection. Can be a number
        -`confirm` : To confirm if we want to enable the tunnel access.
                   Value can be YES or NO
        -`password_option`:A random seed string is required for this operation
                    1. Generate a random string to initialize secure communication (recommended)
                    2. Enter a random string
                    Value can be "random_generated" or "user_input" 

        *Example*
        | Techsupport Sshaccess | temp_pwd='123456' | confirm=YES |password_option = user_input

        """

        kwargs = self._convert_to_dict(args)
        return str(self._cli.techsupport().tunnel(**kwargs))

    def techsupport_disable(self, *args):
        """ This option is used to prevent Cisco IronPort Customer Supporti
        representative from remotely accessing your system.
        *Parameters*
        -`confirm` : To confirm if we want to disable the access.
                    Value can be YES or NO
        *Example*
        | TechSupport Disable | confirm=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.techsupport().disable(**kwargs)

    def techsupport_status(self):
        """ This option is used to display the status of the techsupport.
        *Return*
        - The status - whether enabled or disabled.
        - Tunnel status - Active or not.
        - Serial Number of the machine.

        *Example*
        | ${log}= | Techsupport Status |
        | Log | ${log} |
        """
        return str(self._cli.techsupport().status())
