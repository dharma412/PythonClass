# # Input: s = "abcabcbb"
# # Output: 3
# # Explanation: The answer is "abc", with the length of 3.
#
# def lengthOfLongestSubstring(s):
#     # Base condition
#     if s == "":
#         return 0
#     # Starting index of window
#     start = 0
#     # Ending index of window
#     end = 0
#     # Maximum length of substring without repeating characters
#     maxLength = 0
#     # Set to store unique characters
#     unique_characters = set()
#     # Loop for each character in the string
#     while end < len(s):
#         if s[end] not in unique_characters:
#             print(end)
#
#             unique_characters.add(s[end])
#             print(unique_characters)
#             end += 1
#             maxLength = max(maxLength, len(unique_characters))
#
#         else:
#             unique_characters.remove(s[start])
#             start += 1
#     return maxLength

# print(lengthOfLongestSubstring("abcabcbb"))


def lengthOfLongestSubstring(s: str) -> int:
    result = 0
    cache = {}

    for i in s:
        if i in cache:
            #print(i)
            result = max(result, len(cache))
            while i in cache:
                del cache[list(cache.keys())[0]]

        cache[i] = 0
    # print(len(cache))
    # print(result)
    return max(result, len(cache))

print(lengthOfLongestSubstring("abcabcbb"))