from __future__ import absolute_import

class UserInputError(Exception): pass  # Incorrect Input

class ElementNotFoundError(Exception): pass  # Element not Found Input

class DataNotFoundError(Exception): pass   #Data not exist

class BackEndProcessingError(Exception): pass   #Backend Processing error

class BackEndWarning(Exception): pass #Backend Warning