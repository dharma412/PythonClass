# & 	AND	Sets each bit to 1 if both bits are 1
# |	OR	Sets each bit to 1 if one of two bits is 1
#  ^	XOR	Sets each bit to 1 if only one of two bits is 1
# ~ 	NOT	Inverts all the bits
# <<	Zero fill left shift	Shift left by pushing zeros in from the right and let the leftmost bits fall off
# >>	Signed right shift	Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off

# &~
#
# 1 1  1 0  1   0
# 1 0  0  1 1   1
# 0 1  0  1 1   1
# 0 0  0  1 0   0
a=10  # 1010
b=4   # 0100

c=a&b
print(c)

a=10  # 1010
b=4   # 0100

c=a|b
print(c)


a=11  # 1011
b=11   # 1011

c=a^b
print(c)

a=10  # 1010+1
#1011=11

c=~a
print(c)


#right shift operator
a=10 #0000 0010


#1010 two bits are removed at end
print(a>>2)


#left shift operator
a=10 #0010 1000


#101000 two bits are added at end
print(a<<2)

print(15>>9)
# 0000 0000 0000 1111

# 4 8 16 32 65 128




#find the sum of digits of a number.
#ex: 768 = 21
