import pandas as pd

df=pd.read_csv("List of Notable Events.csv")
list1=['critical','high','medium','low']
for i in list1:
    list2 = [len((df.loc[df['severity'] == i]).index) for i in list1]
    #Sevirity_score=len((df.loc[df['severity']==i]).index)
print(list2)

dictionary = dict(zip(list1,list2 ))
print((dictionary))