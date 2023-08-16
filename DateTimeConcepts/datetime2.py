from datetime import datetime

# current date and time
now = datetime.now()

print(type(now))

print(now.strftime("%H:%M:%S"))

t = now.strftime("%H:%M:%S")
print("Time:", t)
print(now.strftime("%d/%m/%Y"))

