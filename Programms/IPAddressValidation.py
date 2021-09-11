import re
ip="25.25.45.67"

op=re.match('(\d+).(\d+).(\d+).(\d+)',ip)

print(type(op.group()))

if ((int(op.group(1))<=255) and (int(op.group(2))<=255) and int(op.group(3))<=255) and (int(op.group(4))<=255):

    print("valid ip")
else:
    print("Not valid")