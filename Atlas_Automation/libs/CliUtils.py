import pexpect

from robot.api import logger

from Logger import exec_log

DEFAULT_PROMPTS = {
       'ROOT_PROMPT':'\]#',
       'ESA_SMA_PROMPT':'>',
       'USER_PROMPT':'\$'
     }

class CliUtils:
    """ Utilities for interacting with CLI using SSH """
    @exec_log
    def __init__(self):
        self.session = None
        self.log =  None
        self.isconnected = False

    @exec_log
    def ssh_login(self, host, user, password,log_filename):
        """
        Purpose: Launches SSH session with host

        Args:
            host                : SSH server ip or FQDN name
            user                : User name to login in as
            password            : Password of the user
            log_filename        : Log file name to dump the command information

        Returns:
            Returns the SSH session

        """
        self.log = open(log_filename+'.log','wb')
        ssh_command =  'ssh -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no  {0}@{1}'.format(user,host)
        self.session =  pexpect.spawn(ssh_command,logfile=self.log)
        if self.session:
            self.isconnected = True
        self.session.expect('password:',timeout=120) 
        self.session.sendline(password)
        self.session.expect(DEFAULT_PROMPTS['USER_PROMPT'],timeout=120)
        return self.session.before.decode("us-ascii") + self.session.after.decode("us-ascii")


    @exec_log
    def ssh_login_to_appliance(self, host, user, password,log_filename):
        """
        Purpose: Launches SSH session with host

        Args:
            host                : SSH server ip or FQDN name
            user                : User name to login in as
            password            : Password of the user
            log_filename        : Log file name to dump the command information

        Returns:
            Returns the SSH session

        """
        self.log = open(log_filename+'.log','wb')
        ssh_command =  'ssh -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no  {0}@{1}'.format(user,host)
        self.session =  pexpect.spawn(ssh_command,logfile=self.log)
        if self.session:
            self.isconnected = True
        self.session.expect('[pP]assword:',timeout=120)
        self.session.sendline(password)
        self.session.expect(DEFAULT_PROMPTS['ESA_SMA_PROMPT'],timeout=120)
        return self.session.before.decode("us-ascii") + self.session.after.decode("us-ascii")

    @exec_log
    def execute_command(self, command, prompt=DEFAULT_PROMPTS['ROOT_PROMPT'], wait_time=10):
        """
        Purpose: Command to run using SSH

        Args:
            command             : Command to be executed
            prompt              : Prompted executed after command execution
            wait_time           : Wait time for the command execution to complete

        Returns:
            Returns the output of the command

        """
        try:
            logger.info("Executing the command - {}".format(command))
            logger.info("Expecting prompt {}".format(prompt))
            self.session.sendline(command)
            self.session.expect(prompt,timeout=wait_time)
            cmd_output = self.session.before.decode("us-ascii") + self.session.after.decode("us-ascii")
            return cmd_output
        except pexpect.TIMEOUT:
            logger.info("The {0} command did not execute in the given time {1} seconds ".format(command,wait_time))
            return False

    @exec_log
    def execute_command_and_return_command_output_as_list(self, command, prompt=DEFAULT_PROMPTS['ROOT_PROMPT'], wait_time=10):
        """
        Purpose: Command to run using SSH

        Args:
            command             : Command to be executed
            prompt              : Prompted executed after command execution
            wait_time           : Wait time for the command execution to complete

        Returns:
            Returns list if output is available else False would be returned

        """

        try:
            logger.info("Executing the command - {}".format(command))
            logger.info("Expecting prompt {}".format(prompt))
            self.session.sendline(command)
            self.session.expect(prompt, timeout=wait_time)
            value = self.session.before.decode("us-ascii")
            if value:
                val_list = value.split('\n')
                return val_list
            else:
                logger.info("No output for the command - {}".format(command))
                return False
        except pexpect.TIMEOUT:
            logger.info("The {0} command did not execute in the given time {1} seconds ".format(command, wait_time))
            return False

    @exec_log
    def close_session(self):
        """
        Purpose: Closes the SSH session

        Args:
          None
        Returns:
          None
        """
        if self.isconnected:
            self.session.close()

