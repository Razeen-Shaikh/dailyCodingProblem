def has_pair_with_sum(nums, k):
    """
    Check if there is a pair of numbers in the given list that sum up to the target sum.

    Args:
        nums (List[int]): The list of numbers.
        k (int): The target sum.

    Returns:
        bool: True if a pair of numbers sum up to the target sum, False otherwise.
    """
    seen = set()
    for num in nums:
        complement = k - num
        if complement in seen:
            return True
        seen.add(num)
    return False

numbers = [10, 15, 3, 7]
target_sum = 17
result = has_pair_with_sum(numbers, target_sum)
print(result)
