import os

# print(os.path.abspath(os.curdir))
# print(os.path.basename(os.curdir))

#commonpath
# paths = ['/home/User/Desktop', '/home/User/Documents','/home/User/Downloads']
# paths=['','','']  # if paths are empty it will return empty string.
# prefix = os.path.commonpath(paths)
#
# print("Longest common sub-path:", prefix)


#commonprefix
# paths=['/home/User/Desktop', '/home/User/Documents',
#          '/home/User/Downloads']
#
# print(os.path.commonprefix(paths))

#dirname
#print(os.path.dirname(os.path.abspath(os.curdir)))

# exists
# isExist = os.path.exists(os.path.abspath(os.curdir))
# print(isExist)

#lexists
pathExists = os.path.lexists('Modules/CommonModulesInPython')
print(pathExists)