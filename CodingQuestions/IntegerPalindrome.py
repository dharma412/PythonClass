x=int(12321)
temp=x
re=0
while x>0:
    reminder=x%10
    re=re*10+reminder
    x=x//10

if temp==re:
    print("pass")