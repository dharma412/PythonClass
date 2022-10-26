# data frame is is a two-dimensional size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns).
# A Data frame is a two-dimensional data structure, i.e., data is aligned in a tabular fashion in rows and columns.
# PandasAndNumPy DataFrame consists of three principal components, the data, rows, and columns.

#In the real world, a PandasAndNumPy DataFrame will be created by loading the datasets from existing storage, storage can be SQL Database, CSV file, an Excel file.
#PandasAndNumPy DataFrame can be created from the lists, dictionary, and from a list of dictionaries, etc.
import os


# create lits using the list
import pandas as pd

lst = ['Geeks', 'For', 'Geeks', 'is',
			'portal', 'for', 'Geeks']

# Calling DataFrame constructor on list
df = pd.DataFrame(lst)
print(df)

# Python code demonstrate creating
# DataFrame from dict narray / lists
# By default addresses.

import pandas as pd
data = {'Name': ['Tom', 'nick', 'krish', 'jack'],
        'Age': [20, 21, 19, 18]}

df = pd.DataFrame(data)

print(df['Name'])


import pandas as pd
data = pd.read_csv(r"/PandasAndNumPy\nba.csv", index_col ="Name")
#first = data["Age"]
first = data.loc["Avery Bradley"]
second = data.loc["R.J. Hunter"]
print(second)
print(first)

# import pandas as pd
# data = pd.read_csv(r"C:\Users\EACHHDA\Desktop\p\PythonClass\PandasAndNumPy\nba.csv", index_col ="Name")
# #first = data["Age"]
# first = data.iloc[6]
# print(first)

import pandas as pd
data = pd.read_csv(r"/PandasAndNumPy\nba.csv")
#print(data)
#first = data.iloc[7]
first= data.loc[7,["Team", "Number", "Position"]]
print(first)

import pandas as pd
data = pd.read_csv(r"/PandasAndNumPy\nba.csv", index_col='Name')
# selectign single column
# print(data['Age'])
#multiple columsn
#first = data[["Age", "College", "Salary"]]
#select two rows and columns
# first = data.loc[["Avery Bradley", "R.J. Hunter"],
#                    ["Team", "Number", "Position"]]
#selecting all rows and 3 columns
# first = data.loc[:, ["Team", "Number", "Position"]]
# print(first)
#selecting rows by .iloc[]:
# print(data.iloc[3] )
#print(data.iloc [[3, 5, 7],[0,1]])
#print(data.iloc[:,:])
