def fun(x):
    return x[1]

dic1={'a':25,'b':21,'c':24,'d':21,'e':17}
ord={k:v for k,v in dic1.items() if v>17}
print(ord)
for i in dic1:
        print(i[0],i[1])
order_dict1=sorted(dic1.items(),key=fun ,reverse=True)
print(order_dict1)
ord={k:v for k,v in order_dict1.items() if v>17}
print(ord)
for i in order_dict1:
        print(i[0],i[1])



Tv = {'BreakingBad': 100, 'GameOfThrones': 1292, 'TMKUC': 88}

Keymax = sorted(Tv.items(), key=lambda x: x[1])
print(Keymax)