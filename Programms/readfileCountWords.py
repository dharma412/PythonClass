count=0
with open(r'/data.txt', 'r') as f:
        data=f.read()
        print(type(data))
        print(data.count("Raghu"))