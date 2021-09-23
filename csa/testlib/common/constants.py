class CONSTANTS:
    class ConstantRebindError(TypeError):
        pass

    class ConstantDoesNotExist(NameError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstantRebindError, \
                "Cannot rebind a constant. Constant Name: {} | Current Value: {} | New Value: {}".format(
                    name,
                    self.__dict__[name],
                    value
                )
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            raise self.ConstantDoesNotExist, "Constant not created. Constant Name: {}".format(name)
        return self.__dict__[name]
