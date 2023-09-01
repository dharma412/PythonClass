# list1=[1,2,3,4,5]
# list2=['a','b','c','d','e']
#
# dic1={}
# count=0
# for i in list1:
#     dic1[i]=list2[count]
#     count=count+1
# print(dic1)
# result={key1:value1 for key1 in list1 for value1 in list2}
# print(result)

# def reverstring(string1="madam"):
#     return  string1
#
# reverstring("python")

# class laptop:
#
#     def __init__(self,ram,price):
#         print("I am creating object now ")
#         self.ram=ram
#         self.price=price
#
#     def  reverse(self):
#         return self.ram
#
# obj=laptop('8gb',4444)
# print(obj.reverse())
#
# with open('newfile.txt','w') as f1:
#     f1.write("Hello world")


class IceCreamMachine:

    def __init__(self, ingredients, toppings):
        self.ingredients = ingredients
        self.toppings = toppings

    def scoops(self):
        self.toppings.insert(0, self.ingredients[1])
        self.ingredients[1]= self.toppings[1]

        return [self.ingredients,self.toppings]


if __name__ == "__main__":
    machine = IceCreamMachine(["vanilla", "chocolate"], ["chocolate sauce"])
    print(machine.scoops())

#
# Expected output:
# print[['vanilla', 'chocolate #sauce'],['chocolate', 'chocolate sauce']]

date="today"













