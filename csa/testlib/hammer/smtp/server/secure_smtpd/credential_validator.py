import secure_smtpd
import logging

# methodlogy for validating credentials, e.g.,
# lookup credentials for a user in Redis.
CREDENTIALS = {'rtestuser': 'ironport',
               'user1': 'pwd1',
               'user2': 'pwd2',
               'Tvh1270411c': '1234',
               'test': '1234',
               'user': 'password',
               'admin': 'ironport',
               'qatest': 'qatest',
               }


class CredentialValidator(object):
    def validate(self, username, password):
        logger = logging.getLogger(secure_smtpd.LOG_NAME)
        print "username: pwd:", username, password
        if CREDENTIALS.has_key(username):
            if CREDENTIALS[username] == password:
                return True
        else:
            return False
