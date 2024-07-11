#dir() will gives detials of package
import os
print(dir(os))

# To check if file has access right, return True if it has elase return false.
#The mode can take one of four values:

# os.F_OK  — Found
# os.R_OK  — Readable
# os.W_OK  — Writable
# os.X_OK  — Executable
import os
print(os.access('OSModule.py',os.X_OK))

#chdir(path)
# changes the current working directory to the path we specify.
# returns none
print(os.chdir("c:\\mydocuments"))

# getced
import os
print(os.getcwd())

#listdir
import os
print(os.listdir(os.getcwd()))

# mkdir
import os
os.mkdir(os.getcwd()+"/Teja")

#rmdir(path)
import os
os.rmdir(os.getcwd()+"/Teja")

#rename(source,destination)
import os
os.rename(os.getcwd()+"/Teja",os.getcwd()+"/Teja1")

#

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
# pathExists = os.path.lexists('8_Modules/CommonModulesInPython')
# print(pathExists)