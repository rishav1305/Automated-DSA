"""
Problem: Group Anagrams
Difficulty: Medium
URL: https://leetcode.com/problems/group-anagrams/
Category: Arrays & Hashing

Description:
<p>Given an array of strings <code>strs</code>, group the <span data-keyword="anagram">anagrams</span> together. You can return the answer in <strong>any order</strong>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">strs = [&quot;eat&quot;,&quot;tea&quot;,&quot;tan&quot;,&quot;ate&quot;,&quot;nat&quot;,&quot;bat&quot;]</span></p>

<p><strong>Output:</strong> <span class="example-io">[[&quot;bat&quot;],[&quot;nat&quot;,&quot;tan&quot;],[&quot;ate&quot;,&quot;eat&quot;,&quot;tea&quot;]]</span></p>

<p><strong>Explanation:</strong></p>

<ul>
	<li>There is no string in strs that can be rearranged to form <code>&quot;bat&quot;</code>.</li>
	<li>The strings <code>&quot;nat&quot;</code> and <code>&quot;tan&quot;</code> are anagrams as they can be rearranged to form each other.</li>
	<li>The strings <code>&quot;ate&quot;</code>, <code>&quot;eat&quot;</code>, and <code>&quot;tea&quot;</code> are anagrams as they can be rearranged to form each other.</li>
</ul>
</div>

<p><strong class="example">Example 2:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">strs = [&quot;&quot;]</span></p>

<p><strong>Output:</strong> <span class="example-io">[[&quot;&quot;]]</span></p>
</div>

<p><strong class="example">Example 3:</strong></p>

<div class="example-block">
<p><strong>Input:</strong> <span class="example-io">strs = [&quot;a&quot;]</span></p>

<p><strong>Output:</strong> <span class="example-io">[[&quot;a&quot;]]</span></p>
</div>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= strs.length &lt;= 10<sup>4</sup></code></li>
	<li><code>0 &lt;= strs[i].length &lt;= 100</code></li>
	<li><code>strs[i]</code> consists of lowercase English letters.</li>
</ul>


Examples:
["eat","tea","tan","ate","nat","bat"]
[""]
["a"]
"""

from collections import defaultdict
import os
import csv
from datetime import datetime

class Solution:
    def group_anagrams(self, strs):
        """
        Group anagrams together.
        
        Args:
            strs: List of strings to be grouped
            
        Returns:
            List of lists, where each inner list contains strings that are anagrams of each other
            
        Time Complexity: O(n * k) where n is the number of strings and k is the maximum length of a string
        Space Complexity: O(n * k) for storing the result and the hash map
        """
        # Use a defaultdict to group anagrams
        anagram_groups = defaultdict(list)
        
        for s in strs:
            # Sort each string to use as a key for grouping anagrams
            # Strings that are anagrams of each other will have the same sorted representation
            sorted_str = ''.join(sorted(s))
            anagram_groups[sorted_str].append(s)
        
        # Return the values (groups of anagrams) as a list of lists
        return list(anagram_groups.values())
    
    # Alias for the solution function to match the expected interface
    def solution_function(self, strs):
        return self.group_anagrams(strs)
        
    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            # Example 1: Main example from the problem
            (["eat", "tea", "tan", "ate", "nat", "bat"], 
             [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
            
            # Example 2: Single empty string
            ([""], [[""]]),
            
            # Example 3: Single character
            (["a"], [["a"]]),
            
            # Additional test cases
            (["ab", "ba", "abc", "cba", "bca"], [["ab", "ba"], ["abc", "cba", "bca"]]),
            
            # Edge case: All strings are different (no anagrams)
            (["a", "b", "c", "d"], [["a"], ["b"], ["c"], ["d"]]),
            
            # Edge case: All strings are the same
            (["a", "a", "a"], [["a", "a", "a"]]),
            
            # Edge case: Mix of empty strings and non-empty strings
            (["", "", "a", "b"], [["", ""], ["a"], ["b"]])
        ]

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
            # Get the actual result
            actual = sol.solution_function(inputs)
            
            # Sort both expected and actual results for comparison
            # Since the order of groups doesn't matter
            sorted_expected = sorted([sorted(group) for group in expected])
            sorted_actual = sorted([sorted(group) for group in actual])
            
            result = "✓" if sorted_actual == sorted_expected else "✗"
            
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
            update_csv_status("group-anagrams", True)