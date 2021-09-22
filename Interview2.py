n=4

for i in range(0,n):
	for j in range(0,i+1):
		print ("1",end='')
	print('\r')



def sumofdig(n):
	sum = 0
	while n>0:
		sum=sum+n%10
		n=n//10
	return sum
n=1234569999
sumofdigit=sumofdig(n)
print(sumofdigit)

if sumofdigit>9:
	sumofdigit=sumofdig(sumofdigit)
	print(sumofdigit)



def compare(str1,str2):

	if len(str1)>len(str2):
		str1=str1.split(" ")
		if str2 in str1:
			print("Yes")



str2 = "ravi"
str3 = "ruvi"
compare(str1,str2)

str1 = "ravi kumar"
print(str1[::-1])
words=str1.split(" ")

reverse=" ".join(word[::-1] for word in words)

print(reverse)




