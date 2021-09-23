
class URLMissingException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidArgumentsError(Exception):
    def __init__(self, args):
        self.args = args
        self.error = "Invalid arguments for the request query: " + str(args)

    def __str__(self):
        return repr(self.error)
