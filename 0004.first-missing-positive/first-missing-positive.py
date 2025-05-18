
def firstMissingPositive(arr):
    """
    Given an array of integers, find the first missing positive integer in linear time and constant space.
    In other words, find the lowest positive integer that does not exist in the array.
    The array can contain duplicates and negative numbers as well.

    For example, the input[3, 4, -1, 1] should give 2. The input[1, 2, 0] should give 3.

    Args:
        arr (list): A list of integers.

    Returns:
        int: The first missing positive integer in the array.

    """
    return next((i for i in range(1, len(arr)) if i not in arr), len(arr))

arr = [3, 4, -1, 1]
print(firstMissingPositive(arr))

arr = [1, 2, 0]
print(firstMissingPositive(arr))
