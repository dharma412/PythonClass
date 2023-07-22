
# Python3 code to Check for
# balanced parentheses in an expression
def check(my_string):
	brackets = ['()', '{}', '[]']
	while any(x in my_string for x in brackets):
		for br in brackets:
			my_string = my_string.replace(br, '')
			print(my_string)
	return not my_string

# Driver code
string = "[{}]"
result=check(string)
print(string, "-", "Balanced"
	if check(string) else "Unbalanced")


ip_str = "wipro's 1st round completed"
#
# #print(ip_str.replace('i','a'))
#
# for i in


# upper_lower=(ip_str[0:len(ip_str)//2].upper()+(ip_str[(len(ip_str)//2):].lower()))
# print(upper_lower)
# out=[x for x in upper_lower]
# for i in range(len(out)):
# 	if out[i]=="I"
# l=upper_lower.split()
# for i in l:
# 	if "I" or "i" in i:


# Given a string str, print reverse all words except the first and last words
# Examples:
Input="Given a string str, print reverse"
words=Input.split(" ")
output=words[0]+" "+" ".join(word[::-1] for word in words[1:-1])+" "+words[-1]
print(output)





#Output : Hi woh era uoy buddy













# str2=""
# list1=[]
# for j in range(len(upper_lower)):
# 	if upper_lower[j]=="I":
# 		list1.append(j)
# print(list1)
# new="a"
# for k in list1:
# 	if k<len(ip_str)//2:
# 		new="A"
# for i in list1:
# 	upper_lower1=upper_lower[0:list1[0]]+new+upper_lower[7:11]+new+upper_lower[12:]
# 	print(upper_lower1)

