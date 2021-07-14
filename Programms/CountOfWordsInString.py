with open('Files/Files.txt', "r") as file:
    d=dict()
    for line in file:
        line=line.strip().lower().split(" ") # remove spaces at edges
        for word in line:
            if word in d.keys():
                d[word]=d[word]+1
            else:
                d[word]=1
print(d)