"""
Problem: Product of Array Except Self
Difficulty: Medium
URL: https://leetcode.com/problems/product-of-array-except-self/
Category: Arrays & Hashing

Description:
<p>Given an integer array <code>nums</code>, return <em>an array</em> <code>answer</code> <em>such that</em> <code>answer[i]</code> <em>is equal to the product of all the elements of</em> <code>nums</code> <em>except</em> <code>nums[i]</code>.</p>

<p>The product of any prefix or suffix of <code>nums</code> is <strong>guaranteed</strong> to fit in a <strong>32-bit</strong> integer.</p>

<p>You must write an algorithm that runs in&nbsp;<code>O(n)</code>&nbsp;time and without using the division operation.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> nums = [1,2,3,4]
<strong>Output:</strong> [24,12,8,6]
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> nums = [-1,1,0,-3,3]
<strong>Output:</strong> [0,0,9,0,0]
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-30 &lt;= nums[i] &lt;= 30</code></li>
	<li>The input is generated such that <code>answer[i]</code> is <strong>guaranteed</strong> to fit in a <strong>32-bit</strong> integer.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong>&nbsp;Can you solve the problem in <code>O(1)</code>&nbsp;extra&nbsp;space complexity? (The output array <strong>does not</strong> count as extra space for space complexity analysis.)</p>


Examples:
[1,2,3,4]
[-1,1,0,-3,3]
"""

class Solution:
    def solution_function(self, nums):
        """
        For each position i, compute product of all elements except nums[i].
        We accomplish this in two passes:
        1. First pass: Calculate running product of all elements to the left
        2. Second pass: Calculate running product of all elements to the right
           and multiply it with the prefix product
        
        Time Complexity: O(n) - Two passes through the array
        Space Complexity: O(1) - Only output array, which doesn't count as extra space
        """
        n = len(nums)
        result = [1] * n  # Initialize output array
        
        # First pass: Calculate prefix products (product of all elements to the left)
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        
        # Second pass: Calculate suffix products and multiply with prefix products
        suffix = 1
        for i in range(n-1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        
        return result
        
    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        
        Note: The format of inputs depends on the problem:
        - For a single input like an array: ([1,2,3], expected_output)
        - For multiple inputs: ((nums, target), expected_output)
        """
        return [
            # Example test cases from the problem description
            ([1, 2, 3, 4], [24, 12, 8, 6]),
            ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
            
            # Additional test cases
            ([2, 3, 4, 5], [60, 40, 30, 24]),  # All positive
            ([-2, -3, -4], [12, 8, 6]),        # All negative
            ([0, 0, 9, 0], [0, 0, 0, 0]),      # Multiple zeros
            ([7], [1]),                        # Single element (edge case)
            ([1, 1, 1, 1], [1, 1, 1, 1])       # All ones
        ]

# Code to parse examples from description (optional implementation)
def parse_examples_from_description():
    # This function would parse the examples from the problem description
    # and convert them into test cases automatically
    pass
        
# For testing
if __name__ == "__main__":
    sol = Solution()
    test_cases = sol.get_test_cases()
    if not test_cases:
        print("No test cases defined! Please implement get_test_cases() method.")
    else:
        for i, (inputs, expected) in enumerate(test_cases):
            # Handle different input types
            if isinstance(inputs, tuple):
                actual = sol.solution_function(*inputs)
            else:
                actual = sol.solution_function(inputs)
                
            # Compare results - handle different output types as needed
            if isinstance(expected, list) and isinstance(actual, list):
                # For problems that can return results in any order (like two sum)
                result = "✓" if sorted(actual) == sorted(expected) else "✗"
            else:
                result = "✓" if actual == expected else "✗"
                
            print(f"Test {i+1}: {result}")
            if result == "✗":
                if isinstance(inputs, tuple):
                    print(f"  Input: {inputs}")
                else:
                    print(f"  Input: {inputs}")
                print(f"  Expected: {expected}")
                print(f"  Actual: {actual}")