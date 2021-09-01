version=3.9
print("This is python and version is "+ str(version))

name='python'
version=3.9
year=2021
print("The current version of {} is {} in year of {}".format(name,version,year))
print("The current version of {0} is {1} in year of {2}".format(name,version,year))
print("The current version of {name} is {version} in year of {year}".format(name='python',version=3.9,year=2021))


marks=int(input("enter the marks "))
if marks>=35:
    print("The student passed with {} marks".format(marks))
else:
    print("The student failed with {} marks".format(marks))