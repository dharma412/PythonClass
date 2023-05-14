def reverse1(m):
    x = 0
    n = m
    if m < 0 :
      n *= -1
    while n > 0 :
        x *= 10
        x += n % 10
        n /= 10
    if m < 0:
      #concatenate a - sign at the end
      return  "-"+ 'x'
    return x

#print(reverse_int(1234))
print(reverse1(-1234))