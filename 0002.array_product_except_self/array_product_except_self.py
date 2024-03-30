def array_product_except_self(nums):
    """
    Given an array of integers, return a new array such that each element at index i of the new array
    is the product of all the numbers in the original array except the one at i.

    For example, if our input was [1, 2, 3, 4, 5], the expected output would be [120, 60, 40, 30, 24].
    If our input was [3, 2, 1], the expected output would be [2, 3, 6].

    Follow-up: what if you can't use division?

    Args:
        nums (List[int]): The input array of integers.

    Returns:
        List[int]: The product of all the numbers in the original array except the one at i.
    """
    for i, _ in enumerate(nums):
        product = 1
        for j, num in enumerate(nums):
            if i != j:
                product *= num
        nums[i] = product
    return nums
