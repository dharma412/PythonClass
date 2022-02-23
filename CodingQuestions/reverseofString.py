#reverse of string
name="madam"
print(name[::-1])


#reverse of words in sentense
str1="geeks quiz practice code"
liststr=str1.split(" ")
liststr=liststr[::-1]
reversestring=' '.join(liststr)
print(reversestring)

#reverse of individual strings in sentence
str1="geeks quiz practice code"
words=str1.split(" ")
newwords=[word[::-1] for word in words]
newwords=" ".join(newwords)
print(newwords)
