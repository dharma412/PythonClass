#****  02/05/202  KPMG  ***

import re
str1='abc@123'

patter='\d+|\w+|.'

result=re.findall(patter,str1)
print(result)