def inter(str1):
    repea= {}
    for i in str1:
        if i in repea:
            repea[i]+=1
        else:
            repea[i]=1
    return repea

dummy=inter('ggoogle')
result=max(dummy,key=dummy.get)
print(str(result))