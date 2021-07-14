import os
f=open("Files.txt",'a')

f=open("Files.txt",'w') # it will overwrite the data

f=open("Files.txt",'t')

f=open("Files.txt",'+')

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

