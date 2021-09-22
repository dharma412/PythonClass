import os
with open('file123.txt') as f1:
    #print(f1.readlines())
    listoflines=[]
    f1=f1.readlines()
    for i in f1:
        lines=i.rstrip()
        listoflines.append(lines)
    listoflines=[i for i in listoflines if i]
    print(listoflines)

wordsstring=' '.join(listoflines)
listofwords=wordsstring.split(' ')
print(listofwords)
dic1={}
for i in listofwords:
    if i in dic1.keys():
        dic1[i] = dic1[i] + 1
    else:
        dic1[i] = 1

print(dic1)