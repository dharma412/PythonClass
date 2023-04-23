# l1 = [12, 45, 78, 98, 57, 76]
#
# for i in range(0,len(l1),2):
#     for j in range(0,len(l2),):
#     print(l1[i])
#
#
# l2 = [10, 20, 30, 40, 50]






# for i in range(len(l1)):
#     for j in range(i,len(l1)):
#         if l1[i]>l1[j]:
#             len[i],len[j]=len[j],len[i]
#
# print(l1)
#
#
# # l2=[]
# # while l1:
# #     min1=l1[0]
# #     for item in l1:
# #         if item<min1:
# #             min1=item
# #     l2.append(min1)
# #     l1.remove(min1)
# # print(l2[-1])


# Python program for implementation of Bubble Sort


# def bubbleSort(arr):
# 	n = len(arr)
#
# 	# Traverse through all array elements
# 	for i in range(n):
# 		# Last i elements are already in place
# 		for j in range(0, n-i-1):
#
# 			# traverse the array from 0 to n-i-1
# 			# Swap if the element found is greater
# 			# than the next element
# 			if arr[j] > arr[j+1]:
# 				arr[j], arr[j+1] = arr[j+1], arr[j]
#
#
# # Driver code to test above
# if __name__ == "__main__":
#     arr = [5, 1, 4, 8, 2]
#            1 5 4 8 2
#            1 4 5 8 2
#            1 4 5 2 8
#
# bubbleSort(arr)


arr=[5,2,1,8,7]
#
# for i in range(len(arr)-1,0,-1):
#     for j in range(i):
#         if arr[j]>arr[j+i]:
#             tem=arr[j]
#             arr[j]=arr[j+1]
#             arr[j+1]=tem
#
#
# print(arr)

n=len(arr)
for i in range(len(arr)):

    for j in range(n-i-1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]

print(arr)