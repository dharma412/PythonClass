class Car:
    def __int__(self,color,model,engine,cost):  # intialisation
        self.color3=color            #instant variables
        self.model2=model
        self.engine2=engine
        self.cost2=cost

    def drive(self):
        print("I can dirver")

    def reverse(self):
        print("I can dirver reverse")

    @staticmethod
    def sum1(a,b):
        print(a+b)




class Car1(Car):
    def __int__(self,color,model,engine,cost):  # intialisation
        self.color3=color            #instant variables
        self.model2=model
        self.engine2=engine
        self.cost2=cost

    def drive(self):
        print("I can dirver")

    def reverse(self):
        print("I can dirver reverse")

    @staticmethod
    def sum1(a, b,c):
        print(a + b+c)
#
# car1=Car('black','1iro','nenf',788)

# varible
# private
# public and protected variables.




