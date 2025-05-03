"""
Problem: Two Sum
Difficulty: Easy
URL: https://leetcode.com/problems/two-sum/
Category: Arrays & Hashing

Description:
<p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>

<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>

<p>You can return the answer in any order.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,7,11,15], target = 9
<strong>Output:</strong> [0,1]
<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,2,4], target = 6
<strong>Output:</strong> [1,2]
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,3], target = 6
<strong>Output:</strong> [0,1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>
	<li><strong>Only one valid answer exists.</strong></li>
</ul>

<p>&nbsp;</p>
<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face="monospace">&nbsp;</font>time complexity?

Examples:
[2,7,11,15]
9
[3,2,4]
6
[3,3]
6
"""

class Solution:
    def twoSum(self, nums, target):
        """
        Given an array of integers nums and an integer target, return indices of the two 
        numbers such that they add up to target.
        
        Time Complexity: O(n) - We traverse the list once
        Space Complexity: O(n) - We use a hash map to store values
        """
        # Create a hash map to store value -> index
        seen = {}
        
        # Traverse through the array
        for i, num in enumerate(nums):
            # Calculate the complement we need to find
            complement = target - num
            
            # Check if the complement exists in our hash map
            if complement in seen:
                # Return the indices of the two numbers
                return [seen[complement], i]
            
            # Store current value and its index
            seen[num] = i
        
        # No solution found (should not reach here based on problem constraints)
        return []

    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            # Example test cases from the problem description
            (([2, 7, 11, 15], 9), [0, 1]),  # nums[0] + nums[1] = 2 + 7 = 9
            (([3, 2, 4], 6), [1, 2]),       # nums[1] + nums[2] = 2 + 4 = 6
            (([3, 3], 6), [0, 1]),          # nums[0] + nums[1] = 3 + 3 = 6
            
            # Additional test cases
            (([1, 2, 3, 4, 5], 9), [3, 4]), # nums[3] + nums[4] = 4 + 5 = 9
            (([5, 2, 7, 11, 15], 12), [0, 2]), # nums[0] + nums[2] = 5 + 7 = 12
            (([1, 3, 5, 7, 9], 8), [1, 2])  # nums[1] + nums[2] = 3 + 5 = 8
        ]
        
# For testing
if __name__ == "__main__":
    sol = Solution()
    for i, (inputs, expected) in enumerate(sol.get_test_cases()):
        nums, target = inputs
        actual = sol.twoSum(nums, target)
        result = "✓" if actual == expected else "✗"
        print(f"Test {i+1}: {result}")
        if actual != expected:
            print(f"  Input: nums={nums}, target={target}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")