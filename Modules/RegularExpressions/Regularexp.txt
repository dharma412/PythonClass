import re

re.compile() #convert given string into patter.
re.match() # it will look for patter at the begining of string and return None if it is not found.
#re.match() it will return
re.search()# it will look for patter at any position in the string.

#Metacharecter
# '.'- matches any single character except the newline.
# '*' - zero or more occurrence of the patter left to it.
# '+' -one or more occureance of the patter left to it.
# '?'- zero or one occurreence of patter left to it.
#'()' - is used to group sub patters ex: (a
#'^' - is used to check if a string start with a certain character.
# '$' - is used to check if a string ends with a certain character.
#'\'- escape character is used to escape various characters including all metacharacters.
#{} - This means at least n , and at most m repetitions of the pattern left to it. Ex: [0-9]{2,5}

import re

sentence = 'we are humans'
matched = re.match(r'(.*)', sentence)
print(matched.groups(1))

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


