import os

#def count(fname):
num_word=0
num_char=0
num_lines=0
num_spaces=0
file=open('textfike',"r")
for line in file:
    line=line.strip('\n')
    words=line.split(' ')
    num_word=num_word+len(words)
    num_lines+=1
    num_word+=len(words)
    num_char+=len(line)

    print(num_char,num_word,num_lines)
file.close()



