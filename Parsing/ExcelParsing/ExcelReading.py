import xlrd
sheet=xlrd.open_workbook('sampleData_Excel_Data.xlsx')
sheet.sheet_by_index(0)