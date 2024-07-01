class human:
    def __init__(self,name,legs):
        self.name=name
        self.legs=legs

    def run(self):
        print("I am running with parent class")


class animal(human):

    def __init__(self,name,legs,jump):
        super().__init__(name,legs)
        self.jump=jump


    def jump(self):
        print("I am able to jump")

class mamals(human,animal):

    def __init__(self,name,legs,jump):
        super().__init__(name,legs,jump)



object=mamals('hhd',9,"jump")
object.run()

