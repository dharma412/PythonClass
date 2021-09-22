#https://www.geeksforgeeks.org/python-program-to-interchange-first-and-last-elements-in-a-list/
list=[1,2,45,3,5,6,3,64,54,5]

temp=list[1:len(list)-1]
temp.append(list[0])
temp.insert(0,list[len(list)-1])
print(temp)


