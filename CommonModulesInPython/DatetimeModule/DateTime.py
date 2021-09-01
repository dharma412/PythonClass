#Commonly used classes in the datetime module are:

#date Class
#time Class
#datetime Class
#timedelta Class

import datetime
#print(datetime.date.today())
time=datetime.datetime.now()
print(time)



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

