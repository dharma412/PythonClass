class ConfigErrorException1(Exception):
    """ Exception when Config error occured """
    error_msg = "Config error has occured "
    def __init__(self,*args):
        if args:
            super().__init__(args[0])
        else:
            super().__init__(ConfigErrorException1.error_msg)
