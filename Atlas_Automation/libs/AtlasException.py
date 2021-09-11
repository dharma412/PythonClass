class ConfigErrorException(Exception):
    """ Exception when Config error occured """
    error_msg = "Config error has occured "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(ConfigErrorException.error_msg)

class TemporaryAllocationException(Exception):
    """  Exception when Config error occured   """
    error_msg = "Temporary error has occured "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(TemporaryAllocationException.error_msg)

class CustomerNotProvisionedException(Exception):
    """  Exception when Customer is not provisioned   """
    error_msg = "Customer is not provisioned "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(CustomerNotProvisionedException.error_msg)

class AtlasServerUnAssignedException(Exception):
    """  Exception when Customer is not ASSIGNED state  """
    error_msg = "Server is not moved to assigned state "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(AtlasServerUnAssignedException.error_msg)

class WelcomeLetterNotPresentException(Exception):
    """  Exception when Customer welcome letter is not present  """
    error_msg = "Welcome letter not sent to customer"
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(WelcomeLetterNotPresentException.error_msg)

class NotificationNotPresentException(Exception):
    """  Exception when Notification is not present  """
    error_msg = "Notification is not Present"
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(NotificationNotPresentException.error_msg)

class AtlasDbConnectionFailedException(Exception):
    """  Exception when connection to atlas db fails  """
    error_msg = "Connection to Atlas Database failed"
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(AtlasDbConnectionFailedException.error_msg)

class AtlasDbUpdateFailedException(Exception):
    """  Exception when update query against atlas db fails  """
    error_msg = "Update query failed "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(AtlasDbUpdateFailedException.error_msg)

class ExportCustomerImportFailedException(Exception):
    """  Exception when connection to atlas db fails  """
    error_msg = "Importing customer from exportsdb failed"
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(ExportCustomerImportFailedException.error_msg)

class AtlasDbDeleteFailedException(Exception):
    """  Exception when connection to atlas db fails  """
    error_msg = "Delete query failed "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(AtlasDbDeleteFailedException.error_msg)

class LicensePushFailException(Exception):
    """  Exception while pushing license on ESA or SMA has failed """
    error_msg = "License pushed failed to push license "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(LicensePushFailException.error_msg)

class FeatureNotActivatedException(Exception):
    """  Exception while activating the feature on ESA or SMA"""
    error_msg = "Feature activation has failed "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(FeatureNotActivatedException.error_msg)

class FetchCustomerCronLockedException(Exception):
    """ Exception when cron is locked after running fetch customer  """
    error_msg = "Fetch customer cron is locked after fetching customer from exports db"
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(FetchCustomerCronLockedException.error_msg)

class NoSuchAtlasCustomerException(Exception):
    """  Exception when atlas has no such Customer   """
    error_msg = "Atlas has no such Customer "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(NoSuchAtlasCustomerException.error_msg)
