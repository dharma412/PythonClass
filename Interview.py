#f.read() # return content of the whole file.
#f.readlines # retun the list of all lines
#f.close()

with open('C:/Users/dhchaluv/Learning/PythonLearnings/data.txt','r') as f:
    print(f.read())
    print(f.tell())
    print(f.seek(0))
    print(f.tell())


with open('C:/Users/dhchaluv/Learning/PythonLearnings/data.txt','w') as f:
    f.write("This is pythin")
    #print(f.read())

f=open('C:/Users/dhchaluv/Learning/PythonLearnings/data.txt','r')
#data=f.read()
print(f.read())
f.close()

f=open('C:/Users/dhchaluv/Learning/PythonLearnings/data.txt','r')
print(f.read())


# mode of files

#'r' : "to read existing"
# w  : it opens file an write the content, if file does not exist , It will create the file and write the content
# a  : open file to append the at end of the file.
# t  : open file text mode
# b  : binary mode
# +  : open file both reading and writing.
















listoflines=f.readlines()
for i in listoflines:
    print(i,end=',')

print((f.readlines()))
print(type(f.readlines()))




