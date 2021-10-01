with open('Interviewfile.txt') as f1:
    lines=(f1.readlines())
    memorylist = []
    PIDList    = []
    for line in lines:
        linelist=line.split(' ')
        memorylist.append((linelist[9]))
        PIDList.append(linelist[0])
memorylist=memorylist[1:]
PIDList =PIDList[1:]
#print(memorylist)
memorylistfload = []
for i in memorylist:
    memorylistfload.append(float(i))
maxvalue=max(memorylistfload)
indexvalue=(memorylistfload.index(maxvalue))
print("The maxmiun utilisation of memeory is "+str(maxvalue)+ " and the PID value is",PIDList[indexvalue])