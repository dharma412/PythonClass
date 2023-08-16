from datetime import datetime
dic1={'P1' : '3/09/2023' ,'P2' : '6/01/2023' ,'P3' : '1/09/2023' ,'P4' : '2/09/2023','P5' : '28/08/2023'}
#dic1={'P1' : 3 ,'P2' : 6 ,'P3' : 1 ,'P4' : 2,'P5' : 28}

# result=sorted(dic1.values())
# print(result)
result=sorted(dic1.items(),key=lambda x:datetime.strftime(x[1],'%d/%b/%Y'),reverse=True)
print(result)
for i in result:
    print((i[0]))