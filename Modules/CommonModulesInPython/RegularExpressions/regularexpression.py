# import re
#
#
# #    [] . ^ $ * + ? {} () \ |
#
# # sepcial sq  \A,\B,\b,\d,\D,\S,\s,\W,\w,\Z
#
#
#
# #\b --pending
#
# # Program to remove all whitespaces
#
#
# # multiline string
# string1 = 'abc \$ 12 \n 23  f45 6'
# print(type(string1))
#
# #formaula='^c...m$'
# #formaula='..'
# #formaula="\[]"
# #formaula='(\d+) (\d+)'
# formula=r'\n'
# # replace="4"
# res=re.search(formula,string1)
# print(res)
# # res=re.sub(formaula,replace,string)
# # res1=re.subn(formaula,replace,string)
#
# #res=re.match(formaula,str1)
# # print(res1)

#************ Methods in Re **************8
#findall method
# import re
# str1='hello 12585 hi 89. Howdy 34'
# pat='\D+'
# print(re.findall(pat,str1))

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

#re.subn