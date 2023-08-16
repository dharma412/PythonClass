from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta
from datetime import time

print(time(11, 34, 56))

now=dt.now()
print(dt.today())
today = (d.today())
print(today.year)
print(today.month)
print(today.day)

print(d.fromtimestamp(1326244364))
print(dt.fromtimestamp(1326244364))

