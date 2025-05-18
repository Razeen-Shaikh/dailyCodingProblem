
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
    n = len(arr)

    for i in range(n):
        while 1 <= arr[i] <= n and arr[arr[i] - 1] != arr[i]:
            correct_idx = arr[i] - 1
            arr[i], arr[correct_idx] = arr[correct_idx], arr[i]

    return next((i + 1 for i in range(n) if arr[i] != i + 1), n + 1)

arr = [3, 4, -1, 1]
print(firstMissingPositive(arr))

arr = [1, 2, 0]
print(firstMissingPositive(arr))
