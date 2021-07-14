count=0
with open(r'C:\Users\dhchaluv\Learning\PythonLearnings\data.txt','r') as f:
        data=f.read()

        print(type(data))
        print(data.count("Raghu"))