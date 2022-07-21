import re
str1="This is india !!"
#str1=re.subn('[^A-Za-z0-9]+', ' ', str1)  # return the number of substitutions and replaced sub string


str1=re.subn('[^A-Za-z0-9]+', ' ', str1)
print(str1)
# str1="".join(e for e in str1 if e.isalnum())

