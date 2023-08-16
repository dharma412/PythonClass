def optimalSolution(string):

    size = len(string)
    head = 0
    tail = 0
    # Substrings are not explicitly stored but is kept by this head and tail pointer
    chars = dict()      # HashMap in Python

    max_len = 1
    s = 0       # Starting index of the resultant substring
    e = 0       # Ending Index of the resultant substring
    # Both inclusive

    for tail in range(size):
        if string[tail] in chars:
            # Current tail character already present inside HashMap
            if chars[string[tail]] >= head:
                # All characters between head and tail is inside current substring
                # If the character inside HashMap is after head index, then it is inside this current substring
                # Hence, the current tail is a duplicate character, reduce the substring
                head = chars[string[tail]] + 1

        chars[string[tail]] = max(chars.get(string[tail], 0), tail)

        if max_len < (tail - head + 1):
            s = head
            e = tail
            max_len = e - s + 1

    result_string = string[s : e+1]
    return result_string

print(optimalSolution("ahbhduuneud"))