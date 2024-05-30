#************ Methods in Re **************8
#findall method
import re
str1='hello 12585 hi 89. Howdy 34'
pat='\D+'
print(re.findall(pat,str1))

#re.match()
# import re
# str1='12585 hi 89. Howdy 34'
# pat='\D+'
# print(re.match(pat,str1))

# compile
# import re
# str1='12585hi89. Howdy 34'
# pat=re.compile(r'\w+')
#
# print(re.search(pat,str1))

# group
# import re
# str1="teja dharma"
# patter=re.compile('(.*)')
# matchobj=re.match(patter,str1)
# print(matchobj)
# # print(matchobj.re)
# # print(matchobj.string)
# if matchobj:
#     print(matchobj.groups())

# import re
# sentence = 'we are humans'
# matched = re.match(r'(.*)', sentence)
#
# print(len(matched.groups()))

#re.split()

import re
string = 'Twelve 12 Eighty nine 89.'
pattern = '\d+'
result = re.split(pattern, string)
print(result)

#re.sub()
#re.sub() # returns string where matched occurrence are replaced with the content of replace variable.
string = 'Twelve 12 Eighty nine 89.'
pattern = '\d+'
result = re.sub(pattern,'eight', string)
print(result)

#re.subn
#re.subn() is similar to re.sub() expect it returns a tuple of 2 items containing the new string and the number of substitutions made.
string = 'Twelve 12 Eighty nine 89 this 87.'
pattern = '\d+'
result = re.subn(pattern,'eight', string,2)
print(result)


# string='This is ++++ 4565 ++++'
# # pat='((\+{4}) (\d{4}) (\+{4}))'
# # #
# # result=re.findall(pat,string)
# # print(result)

string='343This is ++++ 4565 7 88 898_'
pat=r"[^a-zA-Z0-9_]"
#pat1='^T'
result=re.findall(pat,string)
print(result)