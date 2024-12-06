################# Read Mode without "with" keyword ##################
file1=open('ContentFile.txt','r')
result=file1.read()
print((result))
file1.close()


#**************** file rading with "with" keyword *****************


#way2
with open('ContentFile.txt','r') as f:
    content = f.read(250)
    print((content))

#methods
with open('ContentFile.txt','r') as var1:
    content = var1.readable()
    print(content)

with open('ContentFile.txt','r') as f:
    content = f.read()
    print(type(content))

with open('ContentFile.txt','r') as f:
    content = f.readlines()
    print((content))


with open('ContentFile.txt','r') as f:
    content = f.readline(250)
    print((content))

# Seek method changes the cursor position in file.
with open('ContentFile.txt','r') as f:
    print(f.seek(5)) #bring file cursor to initial position
    print(f.read())

# tell method gives the current position of cursor
with open('ContentFile.txt','r') as f:
    print(f.tell())    # current postion of cursor
    content = f.read(20)
    print((content))
    print(f.tell())
    print(f.seek(0))   #bring file cursor to initial position
    print(f.tell())

with open('ContentFile.txt','r') as f:
    content = f.readable()
    print(f.writable())
    print((content))

with open('ContentFile.txt','w') as f:
    print(f.writable())

with open('ContentFile.txt','w') as f:
    f.truncate(5)
    print((f.read()))


with open('ContentFile.txt','r') as f:
    f.flush()
    print(f.read())
    #print((f.read()))


#flush
#https://www.geeksforgeeks.org/file-flush-method-in-python/

#*********************** file modes *******************
# which is default mode of the file.
with open('ContentFile.txt','r') as f:
    content = f.readline(250)
    print((content))

# write mode
with open('ContentFile.txt','w') as f:
    f.write("This is file")  # data  will be replaced if data present in existing file
    #print(f.read())

with open('ContentFile.txt','w') as f:
    f.writelines(["python\n","ddfdfd","dsfdsfd"])  #
    #print(f.read())

#append mode
with open('ContentFile.txt','a') as f:
    f.write("\nThis is file")  #
    #print(f.read())

# binary mode
with open('ContentFile.txt','rb') as f:
    content=f.read()  #
    print(type(content))

with open(r'ContentFile.txt','a') as var1:
    var1.write("This is pythonfdfs")
    #content = var1.readlines()
    #print(content)