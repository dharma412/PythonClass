# import re
# with open('ipconfig.txt','r') as f1:
#     lines=f1.readlines()
#     for  line in lines:
#
#         if 'Subnet Mask' in line:
#             pattern='\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'
#             result=re.findall(pattern,line)
#             print(result)