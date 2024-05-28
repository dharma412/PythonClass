
#**************** file rading *****************

# var1=open('9_Files.txt','r')
#
# # var1.re
#
# var1.close()


with open(r'C:\Users\eachhda\OneDrive - Ericsson\Desktop\p\PythonClass\Files\Files.txt') as var1:
    content = var1.readable()
    print(content)


#content=var1.read()
content=var1.readlines()
#content=var1.readline()


#way 1
f=open('9_Files/sample.txt','r')
content=f.read()
print(content)
f.close()

#way2
with open('9_Files/sample.txt','r') as f:
    content = f.read(250)
    print((content))

#methods

with open('9_Files/sample.txt','r') as f:
    content = f.read()
    print(type(content))

with open('9_Files/sample.txt','r') as f:
    content = f.readlines()
    print((content))


with open('9_Files/sample.txt','r') as f:
    content = f.readline(250)
    print((content))

with open('9_Files/sample.txt','r') as f:
    content = f.seek(0)  #bring file cursor to initial position

with open('9_Files/sample.txt','r') as f:
    print(f.tell())    # current postion of cursor
    content = f.read(20)
    print((content))
    print(f.tell())
    f.seek()   #bring file cursor to initial position
    print(f.tell())

with open('9_Files/sample.txt','r') as f:
    content = f.readable()
    print(f.writable())
    print((content))

with open('9_Files/sample2.txt','w') as f:
    print(f.writable())

with open('9_Files/sample.txt','w') as f:
    f.truncate(5)
    #print((f.read()))


with open('9_Files/sample.txt','r') as f:
    f.flush()
    print(f.read())
    #print((f.read()))

with open('9_Files/sample.txt','r') as f:
    print(f.read())
    print(f.read())
    #print((f.read()))


#flush
#https://www.geeksforgeeks.org/file-flush-method-in-python/

#*********************** file modes *******************
# which is default mode of the file.
with open('9_Files/sample.txt','r') as f:
    content = f.readline(250)
    print((content))

# write mode
with open('9_Files/sample2.txt','w') as f:
    f.write("This is file")  # data  will be replaced if data present in existing file
    #print(f.read())

with open('9_Files/sample2.txt','w') as f:
    f.writelines(["python\n","ddfdfd","dsfdsfd"])  #
    #print(f.read())

#append mode
with open('9_Files/sample2.txt','a') as f:
    f.write("\nThis is file")  #
    #print(f.read())

# binary mode
with open('9_Files/sample2.txt','rb') as f:
    content=f.read()  #
    print(type(content))

with open(r'C:\Users\eachhda\OneDrive - Ericsson\Desktop\p\PythonClass\Files\Files.txt','a') as var1:
    var1.write("This is pythonfdfs")
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
with open('9_Files\\9_Files.txt', "r") as file:
    print(file.read())
    print(file.tell())
    print(file.seek(0))
    print(file.tell())


with open('9_Files\\9_Files.txt', "r") as file:
    data = file.readlines()
    for line in data:
        word = line.split()
        print (word)

with open("9_Files/Files1.txt",'x') as f:
   f.write("my first file\n")
   f.write("This file\n\n")
   f.write("contains three lines\n")




