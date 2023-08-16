

a = "dharmateja"
b=[i for i in a]
current=None
count=0

for i in b:
    if i!=current:
        b[count]=i
        count=count+1
        current=i

print(b[:count])