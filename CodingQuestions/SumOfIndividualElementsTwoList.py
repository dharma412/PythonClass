


first = [1, 2, 3, 4, 5]
second = [6, 7, 8, 9, 10]
third = []

a = len(first)
b = int(0)
while True:
    x = first[b]
    y = second[b]
    ans = x + y
    third.append(ans)
    b = b + 1
    if b == a:
        break

print (third)
