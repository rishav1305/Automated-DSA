"""
Problem: Contains Duplicate
Difficulty: Easy
URL: https://leetcode.com/problems/contains-duplicate/
Category: Arrays & Hashing

Description:
<p>Given an integer array <code>nums</code>, return <code>true</code> if any value appears <strong>at least twice</strong> in the array, and return <code>false</code> if every element is distinct.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,3,1]</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>

<p><strong>Explanation:</strong></p>

<p>The element 1 occurs at the indices 0 and 3.</p>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,2,3,4]</span></p>

<p><strong>Output:</strong> <span class="example-io">false</span></p>

<p><strong>Explanation:</strong></p>

<p>All elements are distinct.</p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">nums = [1,1,1,3,3,4,3,2,4,2]</span></p>

<p><strong>Output:</strong> <span class="example-io">true</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
</ul>


Examples:
[1,2,3,1]
[1,2,3,4]
[1,1,1,3,3,4,3,2,4,2]
"""

class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        """
        Check if the input list contains any duplicates
        
        Time Complexity: O(n) - We iterate through the list once
        Space Complexity: O(n) - In worst case, we store all elements in the set
        """
        # Use a set to track seen elements
        seen = set()
        
        # Iterate through each number in the array
        for num in nums:
            # If we've seen this number before, return True
            if num in seen:
                return True
            # Otherwise, add it to our set of seen numbers
            seen.add(num)
            
        # If we get through the entire array without finding a duplicate, return False
        return False
    
    # Aliasing solution_function to containsDuplicate for compatibility
    solution_function = containsDuplicate

    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            ([1, 2, 3, 1], True),
            ([1, 2, 3, 4], False),
            ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
            ([], False),  # Edge case: empty array
            ([5], False),  # Edge case: single element
        ]
        
# For testing
if __name__ == "__main__":
    sol = Solution()
    for i, (inputs, expected) in enumerate(sol.get_test_cases()):
        actual = sol.solution_function(inputs)
        result = "✓" if actual == expected else "✗"
        print(f"Test {i+1}: {result}")
        if actual != expected:
            print(f"  Input: {inputs}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")