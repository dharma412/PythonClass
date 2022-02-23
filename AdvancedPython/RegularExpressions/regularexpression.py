import re

#    [] . ^ $ * + ? {} () \ |

# sepcial sq  \A,\B,\b,\d,\D,\S,\s,\W,\w,\Z



#\b --pending

# Program to remove all whitespaces


# multiline string
string1 = 'abc \$ 12 \n 23  f45 6'
print(type(string1))

#formaula='^c...m$'
#formaula='..'
#formaula="\[]"
#formaula='(\d+) (\d+)'
formula=r'\n'
# replace="4"
res=re.search(formula,string1)
print(res)
# res=re.sub(formaula,replace,string)
# res1=re.subn(formaula,replace,string)

#res=re.match(formaula,str1)
# print(res1)
