
# class laptopn:
#     def __init__(self,price,color,ram):
#         self.price=price
#         self.color=color
#         self.ram=ram
#
#     def ram1(self):
#         print("ram is ",self.ram())
#
#     def price_display(self):
#         print("price is ",self.price)
#
# class Dell(laptopn):
#
#     def __init__(self,price,color,ram,model):
#         #super().__init__(color,price,ram)
#         self.mode=model
#         self.price=price
#         self.ram=ram
#         self.color=color
#
#     def ram1(self):
#         print("dell ram is ",self.mode)
#
#     @staticmethod
#     def utilmethod():
#         print("i am static")
#
#
# ob=Dell(85984,'black','5','i5')
# ob.ram1()
# ob.price_display()
# # ob1=Dell(85984,'black','5','i7')
# #
# # Dell.utilmethod()
#


#output: a 4"

def repeating(str1):
    n=len(str1)
    max_count=0
    present_count=1
    cur_char=str1[0]
    for i in range(1,n):
        if str1[i]==str1[i-1]:
            present_count=present_count+1
        else:
            if present_count>max_count:
                max_count=present_count
                cur_char=str1[i-1]
            present_count=1

    if present_count>max_count:
        max_count=present_count
        cur_char=str1[n-1]

    print(max_count)
    return  cur_char

str1="ccabcdefghijklmnopqaaaaxxxxxxxxrstuvwxyzaaccccccc"
print(repeating(str1))