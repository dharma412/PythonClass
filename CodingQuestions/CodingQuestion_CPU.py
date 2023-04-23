with open('cpu') as f1:
    text=f1.read()
    text2=text.replace('-','')
    result = text2.splitlines()
    result = [i for i in result if i]
    ls= []
    for i in result:
        if 'CPU' not in i:
            ls.append(i)
    list_of_cpu=[]
    for i in ls:
        res=[j for j in (i.split(' ')) if j]
        res=[float(i) for i in res]
        res=[int(i) for i in res]
        if res[1]>=50:
            print("The Usage of CPU id "+str(res[0]) +" is "+ str(res[1]))

    # for i in ls:
    #     for i in ls:
    #         =i.split(' ')
    #     res=[i.split(' ') for i in ls]
    #     res1=[i for i in res if i]
    #     print(res1)