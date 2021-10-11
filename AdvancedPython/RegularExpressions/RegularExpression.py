import re



re.compile() #convert given string into patter.
re.match() # it will look for patter at the begining of string and return None if it is not found.
#re.match() it will return
re.search()# it will look for patter at any position in the string.

#Metacharecter
# '.' period- matches any single character except the newline.
# '*' - zero or more occurrence of the patter left to it.
# '+' -one or more occureance of the patter left to it.
# '?'- zero or one occurreence of patter left to it.

# '[]' - set of characters you wish to match.
#'()' - is used to group sub patters ex: (a
#'^' -caret-is used to check if a string start with a certain character.
# '$' - dollar-is used to check if a string ends with a certain character.
#'\'- escape character is used to escape various characters including all metacharacters.
#{} - This means at least n , and at most m repetitions of the pattern left to it. Ex: [0-9]{2,5}


#example: []
import re
var='****%$&$%122456DzZaddefdsABGDUEHFUccdedhf'
patter='[a-zA-Z]+'
matched=re.search(patter,var)
#matched=re.match(patter,var)  # will return NONe
print(matched)
#print(matched.group())

#example: ()-group
#pattern=(a|b|c)xy
import re
patter='(a|b|c)xy'
string1='dxy'
print(re.search(patter,string1))

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
print(matched.group())

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

# special Sequences
# \A - matches if specified characters are at the start of the string.
# \b - matches if specified characters are at the begining or end of the string.
# \B - matches if specified characters are not at the begining or end of the string.
# \d  - matches any decimal digit .Equiwalent to [0-9]
# \D  - matches any non-decimal digit .Equiwalent to [^0-9]
# \s  - matches where a string has whitespace. equivalent to [ \t\n\r\f\v].
# \S  - matches where a string has non-whitespace character. equivalent to [ \t\n\r\f\v].
# \w  - matches alphanumeric character . equivalent to [a-zA-Z0-9_] , underscore is also consider as alphanumeric character.
# \W  - matches non-alphanumeric character. equialent to [^a-zA-Z0-9]

pattern='^a...s$'  # any five letter word starting with a and ends with s
str1="anils"
print(re.match(pattern,str1))






# regular expression methods.
re.findall()
import re
str1='hello 12 hi 89. Howdy 34'
pat='\d+'
print(re.findall(pat,str1))

re.split()

import re
string = 'Twelve 12 Eighty nine 89.'
pattern = '\d+'
result = re.split(pattern, string)
print(result)

re.sub() # returns string where matched occurrence are replaced with the content of replace variable.
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




def fact(n):

    if n <0:
        return 0
    elif n==0 or n==1:
        return 1
    else:
        fac=1
        while n>1:
            fac=fac*n
            n=n-1
        return fac
#print(fact(5))
def postivecase(n):
    assert fact(n) == 121
postivecase(5)


def negavtivetest(n):
    assert fact(n)==0

def postivecasewithzero(n):
    assert fact(n)==1
















