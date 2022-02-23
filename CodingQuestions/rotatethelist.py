def rotate(my_list, num_rotations):
    if num_rotations==0:
        return my_list
    else:
        length=len(my_list)-1
        for i in range(num_rotations):
            print(length)
            res1=my_list.pop(my_list[length])
            print(my_list)
            my_list.insert(i,res1)
            length=length-1

    return my_list
re=rotate([1,2,34,53,4],2)
print(re)

num_rotations = 3
letters = ['a', 'b', 'c', 'd', 'e']
print(letters[-2])
print(letters[-num_rotations:])
print(letters[:-num_rotations])
# to create ['c', 'd', 'e', 'a', 'b']
# we can use the slice operator...

a=letters[-num_rotations:]
b=letters[:-num_rotations]

# ['a', 'b']
print(a+b)




