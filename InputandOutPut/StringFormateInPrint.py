version=3.9
print("the current version of python is" + str(version))

name='python'
version=3
year=2021
#print(name,version,year)
#print("the current version of python is" + str(version)+str(name))
print("The current version of {} is {} in year of {}".format(name,version,year))

print("The current version of {0} is {1} in year of {2}".format(name,version,year))

print("The current version of {name} is {version} in year of {year}".format(name='python',version=3.9,year=2021))


marks=int(input("enter the marks "))
if marks>=35:
    print("The student passed with {} marks".format(marks))
else:
    print("The student failed with {} marks".format(marks))


#************** formated values ********************#

name='python'
version=3
year=2021

pattern='%s%d+'%(name,version)
print(pattern)

s="This is \" single quote symbol"
print(s)


#******************* formating numbers *********************



