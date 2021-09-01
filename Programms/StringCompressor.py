def compressor(s):
    count=0
    for i in range(len(s)):
        if s[i]==s[i-1]:
            count+=1
            print(s[i]+str(count))

compressor("tejajaj")
