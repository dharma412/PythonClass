# AND, OR , NOT
# AND - return true if all conditions return True else return False
# OR  -return true if any one condition return True

3+5

#AND
x=34
if x>=15 or x<=20:
    print("Number is between 15 and 20")
else:
    print("Number is not between 15 and 20")

# OR
x=5
print(x>3 or x<4)

#not
x=15
print(not(x>3 and x<10))


x=[10,23,56,4,64,564,2]
var1=19
#check 19 is in list
#check 19 shoud no be in list

if var1 not in x:
    print("Pass")