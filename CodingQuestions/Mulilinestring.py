s='''name    model    status
-----------------------------
abc    2800    online'''
d={}
s1=s.split('\n')

s2=[x for x in s1 if '-' not in x]

keys=s2[0].split()
values=s2[1].split()

for i in range(len(keys)):
    d[keys[i]]=values[i]

print(d)
# for i in values:
#     d=d.fromkeys(keys,i)
# print(d)
# for i in range(len(keys)):
#     d=d.fromkeys(keys,values[i])
# print(d)
