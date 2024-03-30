def has_pair_with_sum(nums, k):
    """
    Given a list of numbers and a number `k`, return whether any two numbers from the list add up to `k`.
    For example, given $[10, 15, 3, 7]$ and `k` of $17$, return true since $10 + 7$ is $17$.

    Args:
        nums (List[int]): The input list of numbers.
        k (int): The target sum.

    Returns:
        bool: True if any two numbers from the list add up to `k`, False otherwise.
    """
    seen = set()
    for num in nums:
        complement = k - num
        if complement in seen:
            return True
        seen.add(num)
    return False
