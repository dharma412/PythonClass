# Problem statement
#input [1,2,3,4]  input 5

# output  [[1,4],[2,3]]

def find_combinations_recursive(target, numbers, current_sum, start, combination, result):
    if current_sum == target:
        result.append(combination[:])
        return

    for i in range(start, len(numbers)):
        if current_sum + numbers[i] > target:
            continue

        combination.append(numbers[i])
        find_combinations_recursive(target, numbers, current_sum + numbers[i], i, combination, result)
        combination.pop()


def find_combinations(target, numbers):
    result = []
    find_combinations_recursive(target, numbers, 0, 0, [], result)
    return result


input_list = [1, 2, 3, 4]
target_sum = 5
combinations = find_combinations(target_sum, input_list)
print(combinations)
