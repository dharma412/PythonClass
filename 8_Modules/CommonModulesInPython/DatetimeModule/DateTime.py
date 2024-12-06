#Commonly used classes in the datetime module are:

#date Class
#time Class
#datetime Class
#timedelta Class


from datetime import  datetime as dt

from datetime import  date
print(dt.today())
print(date.today())



import datetime
#print(datetime.date.today())
time=datetime.datetime.now()
print(time)


# from datetime import datetime as dt
# today=dt.today()
# print("current year:",today.year)
# print("current month:",today.month)
# print("cuurent day:",today.day)

# import datetime
# d=datetime.date(2020,5,12)
# print(d)
# print(datetime.date.today())
import datetime
print(datetime.date.fromtimestamp(1691414715))
#
# print(datetime.datetime.now())
# print(datetime.date.today())
#
# print(dir(datetime))

#
# from datetime import datetime
#
# # current dateTime
# now = datetime.now()
# print(now)
# #convert to string
# date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
# print('DateTime String:', date_time_str)

str1="Generally the pythons are better than anything else at killing."

print(str1[::-1])


from datetime import datetime
#print(datetime.date.today())
time=datetime.today()
time1=datetime.now()
print(time)
print(time1)





today=datetime.date.today()

import datetime
today=datetime.date.today()
print("current year:",today.year)
print("current month:",today.month)
print("cuurent day:",today.day)

import datetime
d=datetime.date(2020,5,12)
print(d)
print(datetime.date.today())
print(datetime.date.fromtimestamp(1456289364))

print(datetime.datetime.now())
print(datetime.date.today())

print(dir(datetime))

