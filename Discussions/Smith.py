# def reverse(str1):
#
#     str2=""
#     for i in str1:
#         str2=i+str2
#     return str2
#
# print(reverse("python"))
# str1="python"
# print(str1[::-1])



def frequency(str2):
    b={}
    try :
        if not str2.isalpha():
            print("Enter the proper string contains alphabetes")
        else:
            for i in str2:
                if i!=' ' and i.isalpha():
                    if i in b.keys():
                        b[i]=b[i]+1
                    else:
                        b[i]=1

        return b,set(list(b.keys()))
    except AttributeError:
        print()

result,result2=frequency(5445)
print(result,result2)

# Special characters and spaces should be excluded.  input 1: "%7bhfuhd#1" input 2: "&&&&&&" input 3 = "       " 4="yuyu     " 5="       yyyyyy"
# Verify that function takes "alphanumeric" , numberic,data types
# verify that functionn can handle list type of input.
# Verify that function should not accept int, float values (based on current state of function, later )
#     0   1
# |city|state|
# |hyder|telnaga|
# |jaiput|rajastam|
# |mumbai|maharasta|
# |delhi |delhi|
# city="hyder"
# n=4
# driver.findeleme(f'//tbody//tr//childs[@span={city}]'//td[div]).txt