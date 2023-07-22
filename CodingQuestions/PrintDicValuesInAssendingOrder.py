dic1={'a':25,'b':21,'c':24,'d':21,'e':17}
order_dict1=sorted(dic1.items(),key=lambda x:x[1],reverse=True)
print(order_dict1)
for i in order_dict1:
    print(i[0],i[1])