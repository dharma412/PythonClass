# open()


################# Read Mode ##################
# file1=open('sample.txt','r')
# result=file1.read()
# print(file1.tell())
# print((result))
# file1.close()
# file1=open('sample.txt','r')
# print(file1.tell())
#
with open('sample.txt', 'w+') as fi:
    print(fi.truncate(5))
    # print(fi.())
    # print(fi.tell())
    # print(fi.seek(0))
    # print(fi.tell())
    # fi.truncate(2)



##################### write mode ####################

# with open("sample.txt",'a') as fileobject:
#     fileobject.write("this is python\n")
#     fileobject.write("this is python class\n")
#     fileobject.write("this is python learing\n")
#     # fileobject.write("this is python learing new version\n")



##################### Binaryh file mode ####################


