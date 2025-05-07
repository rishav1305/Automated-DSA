"""
Problem: Top K Frequent Elements
Difficulty: Medium
URL: https://leetcode.com/problems/top-k-frequent-elements/
Category: Arrays & Hashing

Description:
<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return <em>the</em> <code>k</code> <em>most frequent elements</em>. You may return the answer in <strong>any order</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> nums = [1,1,1,2,2,3], k = 2
<strong>Output:</strong> [1,2]
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> nums = [1], k = 1
<strong>Output:</strong> [1]
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>
	<li><code>-10<sup>4</sup> &lt;= nums[i] &lt;= 10<sup>4</sup></code></li>
	<li><code>k</code> is in the range <code>[1, the number of unique elements in the array]</code>.</li>
	<li>It is <strong>guaranteed</strong> that the answer is <strong>unique</strong>.</li>
</ul>

<p>&nbsp;</p>
<p><strong>Follow up:</strong> Your algorithm&#39;s time complexity must be better than <code>O(n log n)</code>, where n is the array&#39;s size.</p>


Examples:
[1,1,1,2,2,3]
2
[1]
1
"""

class Solution:
    def top_k_frequent(self, nums, k):
        """
        Find the k most frequent elements in the array.
        
        Args:
            nums: List of integers
            k: Number of most frequent elements to return
            
        Returns:
            List of the k most frequent elements
            
        Time Complexity: O(n log k) where n is the length of the input array
        Space Complexity: O(n) for storing the counter and heap
        """
        # Use Counter to count occurrences of each number
        from collections import Counter
        count = Counter(nums)
        
        # Use heap to get the k most frequent elements
        import heapq
        return heapq.nlargest(k, count.keys(), key=count.get)
    
    def solution_function(self, nums, k):
        return self.top_k_frequent(nums, k)
        
    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            # Example 1 from problem description
            (([1, 1, 1, 2, 2, 3], 2), [1, 2]),
            
            # Example 2 from problem description
            (([1], 1), [1]),
            
            # Additional test cases
            (([1, 2, 2, 3, 3, 3], 2), [3, 2]),
            
            # Edge cases
            (([5, 5, 5, 5, 5], 1), [5]),
            (([1, 2, 3, 4], 4), [1, 2, 3, 4]),  # All elements have the same frequency
            (([1, 2, 3, 1, 2, 1], 2), [1, 2]),  # Tie between elements
            (([3, 0, 1, 0], 1), [0])  # Single most frequent element
        ]

# Import necessary modules for CSV update functionality
import os
import csv
from datetime import datetime

def update_csv_status(problem_id, status=True):
    """
    Update the status of a problem in the questions.csv file.
    
    Args:
        problem_id (str): The ID of the problem to update.
        status (bool): Whether the problem is completed or not.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    csv_path = os.path.join(project_root, 'questions.csv')
    
    # Read the CSV file
    rows = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    
    # Update the status of the problem
    for row in rows:
        if row['id'] == problem_id:
            row['completed'] = str(status)
            if status:
                row['date_completed'] = datetime.now().strftime('%Y-%m-%d')
    
    # Write back to the CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Updated status of '{problem_id}' to {'completed' if status else 'incomplete'}")

# For testing
if __name__ == "__main__":
    sol = Solution()
    test_cases = sol.get_test_cases()
    passed = 0
    total = len(test_cases)
    
    if not test_cases:
        print("No test cases defined! Please implement get_test_cases() method.")
    else:
        for i, (inputs, expected) in enumerate(test_cases):
            # Handle different input types
            if isinstance(inputs, tuple):
                actual = sol.solution_function(*inputs)
            else:
                actual = sol.solution_function(inputs)
                
            # For this problem, the order doesn't matter
            if isinstance(expected, list) and isinstance(actual, list):
                result = "✓" if sorted(actual) == sorted(expected) else "✗"
            else:
                result = "✓" if actual == expected else "✗"
            
            if result == "✓":
                passed += 1
            
            print(f"Test {i+1}: {result}")
            if result == "✗":
                print(f"  Input: {inputs}")
                print(f"  Expected: {expected}")
                print(f"  Actual: {actual}")
        
        print(f"\nPassed {passed}/{total} tests")
        
        # Update CSV if all test cases pass
        if passed == total:
            update_csv_status("top-k-frequent-elements", True)