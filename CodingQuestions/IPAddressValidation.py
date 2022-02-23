import re

def checkIp(ip):
    op=re.match('(\d+).(\d+).(\d+).(\d+)',ip)
    if op==None:
        return ip
ip6=[]
iplist=['44.82.54.207', '48.82.54.207', '213.82.54.207']
for i in iplist:
    ip6.append(checkIp(i))
print(ip6)




