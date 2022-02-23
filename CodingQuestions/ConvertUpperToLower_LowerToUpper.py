def upper(data):
    data=ord(data)-32
    return chr(data)
result=upper('a')
print(result)
str3=[]
str1="unITed STATES of amEriCa"
valuestring=(str1.lower())
values=valuestring.split(' ')
for word in values:
    word=upper(word[0])+word[1:]
    str3.append(word)
print(' '.join(str3))
