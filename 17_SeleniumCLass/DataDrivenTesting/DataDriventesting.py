import openPyxl
import xlrd

workbook=xlrd.open_workbook()
sheet=workbook.get_sheet("emp")

print(sheet.row())

