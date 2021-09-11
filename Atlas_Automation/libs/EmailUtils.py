from email import message_from_file
from robot.api import logger
from Logger import exec_log
from CreateCustomer import *
import re
import os

class EmailUtils:

    def __init__(self):
        self.mail_string = None
        self.mail_content= None

    @exec_log
    def read_eml_file(self):
        """
        Purpose :Read Eml files

        Args:None

        Returns:
            Returns string of mail body

        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','smtp_mails', 'mails',
                             'MailReader.eml'))
        print(path)
        with open(path) as email_file:
            mail_body = message_from_file(email_file)
            self.mail_string= str(mail_body)

        return self.mail_string

    @exec_log
    def is_featureexpirynotification_mailsent(self, *args):
        """
        Purpose: Verify attributes of mail body.

        Args: *args

        Returns:
            Return True if all attributes are matched else returns false.
        """
        mail_content=self.read_eml_file()
        mail_content_list=mail_content.split()
        inputdata_list=[]
        for i in args:
            inputdata_list.extend(str(i).split(','))
        print(inputdata_list)
        print(mail_content_list)
        counter=0
        for item in inputdata_list:
            print(item)
            if item in mail_content_list:
                counter=counter+1
        print(counter)
        return True if counter==len(inputdata_list) else False

    @exec_log
    def execute_local_commands(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'smtp_mails', 'commands.sh'))
        print(path)
        os.system('sh'+' '+ path)
