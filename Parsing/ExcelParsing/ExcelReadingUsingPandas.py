import pandas as a



# converting cell data to other forms

def change_year(cell):
    if cell==2020:
        return 2022
    return cell

df=a.read_excel('sampleData_Excel_Data.xlsx','sampleData',converters = {'Year':change_year})
print(df)