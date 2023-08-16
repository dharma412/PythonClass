# class ObjectCount:
#     ob=0

#     def __init__(self,name):
#         self.name=name
#         self.__updateobvalues()


#     @classmethod
#     def __updateobvalues(cls):
#         cls.ob=cls.ob+1
#         print("Obejct values is ",cls.ob)

#     @classmethod
#     def __del__(cls):
#         cls.ob=cls.ob-1

# class  count(ObjectCount):

#     def __init__(self,name,co):
#         super().__init__(name)

#     def printcount(self):
#         print(self.name)

#     def __del__(self):
#         pass

# ob1=ObjectCount('python')

# del ob1

# ob2=ObjectCount('java')

# ob3=ObjectCount("ruby")

# obj4=count('python','3.6')

# del obj4

# obj5=count('python','3.6')


# def rec(count):
#     try:
#         count=count+1
#     except RecursionError:
#         print("max count is ", count)
#     return rec(count)

# print(rec(1))

