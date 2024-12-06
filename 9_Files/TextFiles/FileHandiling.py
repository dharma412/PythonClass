################# Read Mode ##################
file1=open('ContentFile.txt', 'r')
result=file1.read()
print((result))
print(file1.tell())
file1.close()