"""
Problem: {title}
Difficulty: {difficulty}
URL: {url}
Category: {category}

Description:
{description}

Examples:
{examples}
"""

class Solution:
    def solution_function(self):
        """
        Replace this with the actual solution function
        
        Time Complexity: O(?)
        Space Complexity: O(?)
        """
        pass

    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            # Add test cases here
            # Example: ([1, 2, 3], 6)
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