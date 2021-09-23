import secure_smtpd
import logging

# methodlogy for validating credentials, e.g.,
# lookup credentials for a user in Redis.
CREDENTIALS = {'rtestuser': 'ironport',
               'user1': 'pwd1',
               'user2': 'pwd2'
               }


class FakeCredentialValidator(object):
    def validate(self, username, password):
        logger = logging.getLogger(secure_smtpd.LOG_NAME)
        print "username: pwd", username, username
        if CREDENTIALS.has_key(username):
            if CREDENTIALS[username] == password:
                return True
        else:
            return False
