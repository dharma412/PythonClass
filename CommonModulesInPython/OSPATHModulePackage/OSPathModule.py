# return the file name of the path.
import os
out = os.path.basename("C:/Users/dhchaluv/Learning/RobotLearning/OSPATHModulePackage/OSPathModule.py")
print(out)

# return directroy name of the path.
import os
out = os.path.dirname("C:/Users/dhchaluv/Learning/RobotLearning/OSPATHModulePackage/OSPathModule.py")
print(out)

#It specifies whether the path is absolute or not.
#In Unix system absolute path means path begins with the slash(‘/’)
#In Windows that it begins with a (back)slash after chopping off a potential drive letter.
import os
out=os.path.isabs("C:/Users/dhchaluv/Learning/RobotLearning/OSPATHModulePackage/OSPathModule.py")
print(out)

# This function specifies whether the path is existing directory or not.
import os
out=os.path.isdir(r'C:\Users\dhchaluv\Learning\RobotLearning\OSPATHModulePackage\OSPathModule.py')
print(out)

# This function specifies whether the path is file or not.
import os
out=os.path.isfile(r'C:\Users\dhchaluv\Learning\RobotLearning\OSPATHModulePackage\OSPathModule.py')
print(out)

#This function normalizes the case of the pathname specified.
# In Unix and Mac OS X system it returns the pathname as it is .
#But in Windows it converts the path to lowercase and forward slashes to backslashes.
import os
out = os.path.normcase("C:/Users/dhchaluv/Learning/RobotLearning/OSPATHModulePackage/OSPathModule.py")
print(out)


# normpath function in Unix
import os
out = os.path.normpath("C:/Users/dhchaluv/Learning/RobotLearning/OSPATHModulePackage/OSPathModule.py")
print(out)

import os
path1=os.path.abspath('OSPathModule.py')
path1=path1+'\ospath.py'
print(path1)


