str1="amadeus is onboarding brilliant minds"

result=" "
space=True
for i in range(len(str1)):
    if str1[i]==' ':
        space= True
    elif (str1[i]!=' ' and space==True):
        result+=(str1[i])
        space=False
print(result.upper())