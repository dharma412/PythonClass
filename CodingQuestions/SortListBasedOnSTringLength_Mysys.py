# Problem Statement
# Sort based on length of string and do not use inbuilt methods
# if string has same length go with alaphates
input_function = ["goa", "Mysure", "mysure", "Mumbai", "Bangalore", "mumbai", "BANGALORE", "Pune"]

def custom_sort(lst):
    n = len(lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if len(lst[j]) > len(lst[j + 1]):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

custom_sort(input_function)

print(input_function)
