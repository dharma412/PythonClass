import os

from sys import stderr

class FatalOption:
    pass

class MboxUtils:

    def check_multiple_mboxes(self, mbox_filelist):
        mbox_list = mbox_filelist.split(',')
        for each_mbox in mbox_list:
            self.check_option(each_mbox, "Mbox file: %s does not exist." %each_mbox)
        return mbox_list

    def check_option(self, argument, err_text):
        if not os.path.exists(argument):
            print >> stderr, err_text
            raise FatalOption

    def generate_journal_addresslist(self, journal_recipient, duration):
        address_list_file = 'journal-recipient.txt'
        with open(address_list_file, 'w+') as filedata:
            journal_addr = ['%s\n' %journal_recipient]
            filedata.writelines(1000 * int(duration) * journal_addr)
        return address_list_file
