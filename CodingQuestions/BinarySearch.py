require = 13
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]

# right=0
# left=len(list1)-1
# mid =  (right+left)//2
# print(list1[mid])
# if require==list1[mid]:
#     print(mid)
#
# elif require > list1[mid]:
#      mid=mid+1
#
# else:
#
#
# 2 -- target
#
# 1  2  3  4  5  6  7


def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # target value not found
