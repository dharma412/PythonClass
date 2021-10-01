import os
#**************** file rading *****************
#var1=open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt')

with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt') as var1:
    content = var1.readlines()
    print(content)


#content=var1.read()
content=var1.readlines()
#content=var1.readline()
print(content)
var1.close()

#*********************** file modes *******************
with open("Files.txt") as f1:
    pass

with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt','w') as var1:
    var1.write("This is python")
    #content = var1.readlines()
    #print(content)

with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt','t') as var1:
    var1.write("This is python ")
    #content = var1.readlines()
    #print(content)

with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt','b') as var1:
    var1.write("This is python ")
    #content = var1.readlines()
    #print(content)

with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\Files\Files.txt','r+') as var1:
    var1.write("This is python ")
    content = var1.readlines()
    print(content)
    #print(content)

#read file
with open('Files\\Files.txt', "r") as file:
    print(file.read())
    print(file.tell())
    print(file.seek(0))
    print(file.tell())


with open('Files\\Files.txt', "r") as file:
    data = file.readlines()
    for line in data:
        word = line.split()
        print (word)

with open("Files/Files1.txt",'x') as f:
   f.write("my first file\n")
   f.write("This file\n\n")
   f.write("contains three lines\n")




