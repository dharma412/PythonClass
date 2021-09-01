import sys

import pandas as pd

#df=pd.read_csv('sampleData.csv',skiprows=0)  #skiprows skip the row of given value

#df=pd.read_csv('sampleData.csv',header=1)  # header index start from zero so it will consider the header is start from argument value.
#df=pd.read_csv('sampleData.csv',header=None,names=["name1","name2","name3","name4","name5"]) # when head is none and we can give header names here

#df=pd.read_csv('sampleData.csv',nrows=4) # to read limited rows

#df=pd.read_csv('sampleData.csv',na_values=["not available","2020"],nrows=10) # to replace data cell values
# here we are replacing 2020 with NaN usually we apply for not available data


# if we want to replace different colums with differnt data we can pass dictionary to na_values

df=pd.read_csv('sampleData.csv',na_values={'Year':["not available","2020"],'Variable_code':['Rupees','Dollars (millions)']},nrows=10)

print((df))
sys.exit()