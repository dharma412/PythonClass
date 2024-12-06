import re


re.compile() #convert given string into patter.
re.match() # it will look for patter at the begining of string and return None if it is not found.
#re.match() it will return
re.search()# it will look for patter at any position in the string.

#example: []
import re
var='fgfgfr****%$&$%122456DzZaddefdsABGDUEHFUccdedhf&&&&&hthftgf'
patter='[a-zA-Z]+'
#matched=re.search(patter,var)
matched=re.match(patter,var)# will return NONe
values=re.findall(patter,var)
print(values)
# print(type(matched))
# print(matched.group())

#example: ()-group
#pattern=(a|b|c)xy
import re
patter='((a|b|c)xy)'
string1='axy56565654654bxy'
print(re.findall(patter,string1))

#eample: ^ and $
import re
patter='^a...s$'
str1='anals'
matched=re.match(patter,str1)
print(matched)
print(matched.group())

#example Braces: {}
import re
sentence = 'his ias python'
patter='a{2,7}'
#matched=re.match(patter,sentence)
matched=re.search(patter,sentence)
print(matched)

#example Alternation: |
import re
sentence = 'his iabs python'
patter='a|b'
#matched=re.match(patter,sentence)
matched=re.search(patter,sentence)
print(matched.group())


# Special Sequence
#example: \A- matches if specified characters are at the start of a string
import re
str1="the sun"
pattern='^the'
patter='\Athe'
print(re.match(patter,str1))

# example : \b
import re
str1="football"
pa1='foo\B'
print(re.search(pa1,str1))

# example : \d -matches any charcter between [0-9]
import re
str1="12abcd233"
pa1='\d*'
print(re.search(pa1,str1))

# example : \D - does not matches any charcter between [0-9]
import re
str1="12abcd233"
pa1='\D+'
print(re.search(pa1,str1))

# \w-  it is eqaul to [a-zA-Z0-9_]
import re
str1="_1y73573683#@#"
pa1='\w+'
print(re.search(pa1,str1))
print(re.findall(pa1,str1))
print(re.split(pa1,str1))

# \W-  it does not match any char in ^[a-zA-Z0-9_]
import re
str1="_12abcd%$233"
pa1='\W+'
print(re.search(pa1,str1))
print(re.findall(pa1,str1))

import re
var="12356836"
match=re.match(r'.*',var)
print(match.group())

matched = re.match(r'(.*)', sentence)
print(matched.groups())

import re
str1="teja dharma"
patter=re.compile('(.*)')
matchobj=re.match(patter,str1)
print(matchobj.re)
print(matchobj.string)
if matchobj:
    print(matchobj.groups())

pattern='^a...s$'  # any five letter word starting with a and ends with s
str1="anils"
print(re.match(pattern,str1))

# regular expression methods.
#re.findall()
import re
str1='hello 12 hi 89. Howdy 34'
pat='\d+'
print(re.findall(pat,str1))

#re.split()

import re
string = 'Twelve 12 Eighty nine 89.'
pattern = '\d+'
result = re.split(pattern, string)
print(result)

#re.sub() # returns string where matched occurrence are replaced with the content of replace variable.
# Program to remove all whitespaces
import re

# multiline string
string = 'abc 12\
de 23 \n f45 6'

# matches all whitespace characters
pattern = '\s+'

# empty string
replace = ''

new_string = re.sub(pattern, replace, string)
print(new_string)


#re.subn()
#re.subn() is similar to re.sub() expect it returns a tuple of 2 items containing the new string and the number of substitutions made.

# Program to remove all whitespaces
import re
# multiline string
string = 'abc 12\
de 23 \n f45 6'
# matches all whitespace characters
pattern = '\s+'
# empty string
replace = ''
new_string = re.subn(pattern, replace, string)
print(new_string)

# Output: ('abc12de23f456', 4)

#note other methods are


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