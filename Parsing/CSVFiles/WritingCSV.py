import pandas as pd

df=pd.read_csv('sampleData.csv',nrows=10)
print(df.columns) # display all columns
#df.to_csv('sampleDataWritin.csv') # by default it will write the index into it.
df.to_csv('sampleDataWritin.csv',index=False)

df.to_csv('sampleDataWritin.csv',index=False,columns=['Year', 'Industry_aggregation_NZSIOC', 'Industry_code_NZSIOC'])
# To mention onlt few columns


