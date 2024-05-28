class student:
    def __init__(self,fee,id_card,uniform):
        self.money=fee
        self.id=id_card
        self.cloths=uniform

    def study(self):
        return "students will be studying" + self.money

    def play(self):
        print("students will play",self.id)

    def eat(self):
        print("students will eat",self.cloths)

    def clothe(self):
        print("students will wear")


stu=student("books","games","food")
result=stu.study()
print(result)

# result1=stu.play()
# print(result1)
#
# result2=stu.eat()
# print(result2)