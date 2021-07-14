# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it
#conversion of character to numbers is called encoding , and the reverse process is decoding.
#ASCII and unicode or the popular encodings used.

str1='hello'
print(str1)

str2="hello"
print(str2)

str3="""string can be write in multipe
    lines using the 
    triple quotes 
    bgyftfyhb """
print(str3)

# we can access the elements of string in using the index
# index must be integer can not use floate or other type which leads to typeError.

# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it.
mystring='This is python'
print(mystring[:8])
print(id(mystring))
#mystring='u'
#mystring=[1,2,4,56]

#python string operators
# string operations

mystr1='This'
mystr2=' is python'
print(mystr1+mystr2)

n=1
print("hello"+str(n))

#iteration Through a string

itestring='hello ramya'
count=0
for letter in itestring:
    if letter=='a':
        count=count+1
print(count)

itestring1="this is india"
for letter in itestring1:
    print(letter, end=',')

def sumofdigit(n):
    sum=0
    while n>0:
        r=n%10  #7 #9 #8
        sum=sum+r # 7 #16 # 24
        n=n//10 #89 #8 #0
    return sum

res=sumofdigit(8975456)
if res>10:
    print(sumofdigit(res))
else:
    print(res)

def palindormer():
    str222='madam'
    print(str222[::-1])

str='This is python'
print(list(enumerate(str)))

#use triple quotes to print double and single quotes in string.

print('''He said, "What's there?"''')
print('He said, "What\'s there?\"')