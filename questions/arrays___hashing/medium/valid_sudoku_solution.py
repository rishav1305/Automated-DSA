"""
Problem: Valid Sudoku
Difficulty: Medium
URL: https://leetcode.com/problems/valid-sudoku/
Category: Arrays & Hashing

Description:
<p>Determine if a&nbsp;<code>9 x 9</code> Sudoku board&nbsp;is valid.&nbsp;Only the filled cells need to be validated&nbsp;<strong>according to the following rules</strong>:</p>

<ol>
	<li>Each row&nbsp;must contain the&nbsp;digits&nbsp;<code>1-9</code> without repetition.</li>
	<li>Each column must contain the digits&nbsp;<code>1-9</code>&nbsp;without repetition.</li>
	<li>Each of the nine&nbsp;<code>3 x 3</code> sub-boxes of the grid must contain the digits&nbsp;<code>1-9</code>&nbsp;without repetition.</li>
</ol>

<p><strong>Note:</strong></p>

<ul>
	<li>A Sudoku board (partially filled) could be valid but is not necessarily solvable.</li>
	<li>Only the filled cells need to be validated according to the mentioned&nbsp;rules.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Sudoku-by-L2G-20050714.svg/250px-Sudoku-by-L2G-20050714.svg.png" style="height:250px; width:250px" />
<pre>
<strong>Input:</strong> board = 
[[&quot;5&quot;,&quot;3&quot;,&quot;.&quot;,&quot;.&quot;,&quot;7&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;]
,[&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;1&quot;,&quot;9&quot;,&quot;5&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;]
,[&quot;.&quot;,&quot;9&quot;,&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;,&quot;.&quot;]
,[&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;3&quot;]
,[&quot;4&quot;,&quot;.&quot;,&quot;.&quot;,&quot;8&quot;,&quot;.&quot;,&quot;3&quot;,&quot;.&quot;,&quot;.&quot;,&quot;1&quot;]
,[&quot;7&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;2&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;]
,[&quot;.&quot;,&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;2&quot;,&quot;8&quot;,&quot;.&quot;]
,[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;4&quot;,&quot;1&quot;,&quot;9&quot;,&quot;.&quot;,&quot;.&quot;,&quot;5&quot;]
,[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;7&quot;,&quot;9&quot;]]
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> board = 
[[&quot;8&quot;,&quot;3&quot;,&quot;.&quot;,&quot;.&quot;,&quot;7&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;]
,[&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;1&quot;,&quot;9&quot;,&quot;5&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;]
,[&quot;.&quot;,&quot;9&quot;,&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;,&quot;.&quot;]
,[&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;3&quot;]
,[&quot;4&quot;,&quot;.&quot;,&quot;.&quot;,&quot;8&quot;,&quot;.&quot;,&quot;3&quot;,&quot;.&quot;,&quot;.&quot;,&quot;1&quot;]
,[&quot;7&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;2&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;6&quot;]
,[&quot;.&quot;,&quot;6&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;2&quot;,&quot;8&quot;,&quot;.&quot;]
,[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;4&quot;,&quot;1&quot;,&quot;9&quot;,&quot;.&quot;,&quot;.&quot;,&quot;5&quot;]
,[&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;.&quot;,&quot;8&quot;,&quot;.&quot;,&quot;.&quot;,&quot;7&quot;,&quot;9&quot;]]
<strong>Output:</strong> false
<strong>Explanation:</strong> Same as Example 1, except with the <strong>5</strong> in the top left corner being modified to <strong>8</strong>. Since there are two 8&#39;s in the top left 3x3 sub-box, it is invalid.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>board.length == 9</code></li>
	<li><code>board[i].length == 9</code></li>
	<li><code>board[i][j]</code> is a digit <code>1-9</code> or <code>&#39;.&#39;</code>.</li>
</ul>


Examples:
[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
"""

class Solution:
    def solution_function(self, board):
        """
        Determine if a 9x9 Sudoku board is valid by checking:
        1. Each row has unique digits 1-9 (no duplicates)
        2. Each column has unique digits 1-9 (no duplicates)
        3. Each 3x3 sub-box has unique digits 1-9 (no duplicates)
        
        Time Complexity: O(1) since board size is fixed at 9x9
        Space Complexity: O(1) since we use fixed-size sets
        """
        # Initialize sets to track digits in rows, columns, and 3x3 boxes
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        
        # Check each cell in the board
        for i in range(9):
            for j in range(9):
                # Skip empty cells
                if board[i][j] == '.':
                    continue
                
                # Get the current value
                val = board[i][j]
                
                # Calculate box index (0-8) for the current cell
                box_idx = (i // 3) * 3 + (j // 3)
                
                # Check if value already exists in row, column, or box
                if (val in rows[i] or 
                    val in cols[j] or 
                    val in boxes[box_idx]):
                    return False
                
                # Add value to the respective sets
                rows[i].add(val)
                cols[j].add(val)
                boxes[box_idx].add(val)
                
        # If no duplicates were found, the board is valid
        return True
        
    def get_test_cases(self):
        """
        Return a list of test cases in the format:
        [
            (inputs, expected_output),
            ...
        ]
        """
        return [
            # Example 1: Valid Sudoku
            ([
                ["5","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]
            ], True),
            
            # Example 2: Invalid Sudoku (duplicate 8 in top-left box)
            ([
                ["8","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]
            ], False),
            
            # Additional test case: Empty board (all cells are '.')
            ([
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ]
            ], True),
            
            # Additional test case: Invalid row (duplicate 1)
            ([
                ["1","1",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ]
            ], False),
            
            # Additional test case: Invalid column (duplicate 2)
            ([
                ["2",".",".",".",".",".",".",".","."],
                ["2",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ]
            ], False),
            
            # Additional test case: Invalid 3x3 box (duplicate 3)
            ([
                ["3",".",".",".",".",".",".",".","." ],
                [".","3",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ],
                [".",".",".",".",".",".",".",".","." ]
            ], False)
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