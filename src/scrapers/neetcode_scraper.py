import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import time

def fetch_neetcode_questions():
    """
    Fetches questions from NeetCode 150 and returns them as a DataFrame
    """
    print("Fetching questions from NeetCode 150...")
    
    # The URL uses JavaScript to load data, so we can't directly scrape it
    # Instead, NeetCode loads data from this API endpoint
    api_url = "https://neetcode.io/api/problems/list"
    
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://neetcode.io/practice'
        }
        
        # Make the request with headers and a timeout
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Print response info for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type', 'Unknown')}")
        
        # Check if the response is empty
        if not response.text.strip():
            print("Received empty response from API")
            return create_fallback_questions()
        
        # Save the raw response for debugging if needed
        raw_response_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "raw_response.json")
        with open(raw_response_path, 'w') as f:
            f.write(response.text)
        print(f"Raw response saved to {raw_response_path}")
        
        # Try to parse the JSON response
        try:
            all_problems = response.json()
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return create_fallback_questions()
        
        # Filter for NeetCode 150 problems (they have a neetCode tag)
        neetcode150 = [problem for problem in all_problems if problem.get('neetCode', False)]
        
        # If no NeetCode 150 problems found, use the fallback
        if not neetcode150:
            print("No NeetCode 150 problems found in API response. Using fallback data.")
            return create_fallback_questions()
        
        # Extract needed fields
        questions = []
        for problem in neetcode150:
            questions.append({
                'id': problem.get('id'),
                'title': problem.get('title'),
                'url': f"https://leetcode.com/problems/{problem.get('slug')}/",
                'difficulty': problem.get('difficulty'),
                'category': problem.get('category'),
                'pattern': problem.get('pattern', ''),
                'completed': False,
                'date_completed': ''
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(questions)
        print(f"Successfully parsed {len(df)} questions from API")
        return df
    
    except Exception as e:
        print(f"Error fetching questions: {e}")
        return create_fallback_questions()

def create_fallback_questions():
    """
    Creates a fallback list of NeetCode 150 problems
    """
    print("Using fallback list of NeetCode 150 problems...")
    
    questions = [
        # Arrays & Hashing
        {'id': 1, 'title': 'Two Sum', 'url': 'https://leetcode.com/problems/two-sum/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing'},
        {'id': 49, 'title': 'Group Anagrams', 'url': 'https://leetcode.com/problems/group-anagrams/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing'},
        {'id': 217, 'title': 'Contains Duplicate', 'url': 'https://leetcode.com/problems/contains-duplicate/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing'},
        {'id': 238, 'title': 'Product of Array Except Self', 'url': 'https://leetcode.com/problems/product-of-array-except-self/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing'},
        {'id': 242, 'title': 'Valid Anagram', 'url': 'https://leetcode.com/problems/valid-anagram/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing'},
        {'id': 347, 'title': 'Top K Frequent Elements', 'url': 'https://leetcode.com/problems/top-k-frequent-elements/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing'},
        {'id': 271, 'title': 'Encode and Decode Strings', 'url': 'https://leetcode.com/problems/encode-and-decode-strings/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing'},
        
        # Two Pointers
        {'id': 125, 'title': 'Valid Palindrome', 'url': 'https://leetcode.com/problems/valid-palindrome/', 'difficulty': 'Easy', 'category': 'Two Pointers'},
        {'id': 15, 'title': '3Sum', 'url': 'https://leetcode.com/problems/3sum/', 'difficulty': 'Medium', 'category': 'Two Pointers'},
        {'id': 11, 'title': 'Container With Most Water', 'url': 'https://leetcode.com/problems/container-with-most-water/', 'difficulty': 'Medium', 'category': 'Two Pointers'},
        
        # Sliding Window
        {'id': 121, 'title': 'Best Time to Buy and Sell Stock', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/', 'difficulty': 'Easy', 'category': 'Sliding Window'},
        {'id': 3, 'title': 'Longest Substring Without Repeating Characters', 'url': 'https://leetcode.com/problems/longest-substring-without-repeating-characters/', 'difficulty': 'Medium', 'category': 'Sliding Window'},
        {'id': 424, 'title': 'Longest Repeating Character Replacement', 'url': 'https://leetcode.com/problems/longest-repeating-character-replacement/', 'difficulty': 'Medium', 'category': 'Sliding Window'},
        
        # Stack
        {'id': 20, 'title': 'Valid Parentheses', 'url': 'https://leetcode.com/problems/valid-parentheses/', 'difficulty': 'Easy', 'category': 'Stack'},
        {'id': 155, 'title': 'Min Stack', 'url': 'https://leetcode.com/problems/min-stack/', 'difficulty': 'Easy', 'category': 'Stack'},
        {'id': 84, 'title': 'Largest Rectangle in Histogram', 'url': 'https://leetcode.com/problems/largest-rectangle-in-histogram/', 'difficulty': 'Hard', 'category': 'Stack'},
        
        # Binary Search
        {'id': 704, 'title': 'Binary Search', 'url': 'https://leetcode.com/problems/binary-search/', 'difficulty': 'Easy', 'category': 'Binary Search'},
        {'id': 74, 'title': 'Search a 2D Matrix', 'url': 'https://leetcode.com/problems/search-a-2d-matrix/', 'difficulty': 'Medium', 'category': 'Binary Search'},
        {'id': 33, 'title': 'Search in Rotated Sorted Array', 'url': 'https://leetcode.com/problems/search-in-rotated-sorted-array/', 'difficulty': 'Medium', 'category': 'Binary Search'},
        
        # Linked List
        {'id': 206, 'title': 'Reverse Linked List', 'url': 'https://leetcode.com/problems/reverse-linked-list/', 'difficulty': 'Easy', 'category': 'Linked List'},
        {'id': 21, 'title': 'Merge Two Sorted Lists', 'url': 'https://leetcode.com/problems/merge-two-sorted-lists/', 'difficulty': 'Easy', 'category': 'Linked List'},
        {'id': 23, 'title': 'Merge k Sorted Lists', 'url': 'https://leetcode.com/problems/merge-k-sorted-lists/', 'difficulty': 'Hard', 'category': 'Linked List'},
        
        # Trees
        {'id': 104, 'title': 'Maximum Depth of Binary Tree', 'url': 'https://leetcode.com/problems/maximum-depth-of-binary-tree/', 'difficulty': 'Easy', 'category': 'Trees'},
        {'id': 100, 'title': 'Same Tree', 'url': 'https://leetcode.com/problems/same-tree/', 'difficulty': 'Easy', 'category': 'Trees'},
        {'id': 124, 'title': 'Binary Tree Maximum Path Sum', 'url': 'https://leetcode.com/problems/binary-tree-maximum-path-sum/', 'difficulty': 'Hard', 'category': 'Trees'},
        
        # Heap / Priority Queue
        {'id': 703, 'title': 'Kth Largest Element in a Stream', 'url': 'https://leetcode.com/problems/kth-largest-element-in-a-stream/', 'difficulty': 'Easy', 'category': 'Heap / Priority Queue'},
        {'id': 1046, 'title': 'Last Stone Weight', 'url': 'https://leetcode.com/problems/last-stone-weight/', 'difficulty': 'Easy', 'category': 'Heap / Priority Queue'},
        {'id': 295, 'title': 'Find Median from Data Stream', 'url': 'https://leetcode.com/problems/find-median-from-data-stream/', 'difficulty': 'Hard', 'category': 'Heap / Priority Queue'},
        
        # Backtracking
        {'id': 78, 'title': 'Subsets', 'url': 'https://leetcode.com/problems/subsets/', 'difficulty': 'Medium', 'category': 'Backtracking'},
        {'id': 39, 'title': 'Combination Sum', 'url': 'https://leetcode.com/problems/combination-sum/', 'difficulty': 'Medium', 'category': 'Backtracking'},
        {'id': 51, 'title': 'N-Queens', 'url': 'https://leetcode.com/problems/n-queens/', 'difficulty': 'Hard', 'category': 'Backtracking'},
        
        # Graphs
        {'id': 200, 'title': 'Number of Islands', 'url': 'https://leetcode.com/problems/number-of-islands/', 'difficulty': 'Medium', 'category': 'Graphs'},
        {'id': 133, 'title': 'Clone Graph', 'url': 'https://leetcode.com/problems/clone-graph/', 'difficulty': 'Medium', 'category': 'Graphs'},
        {'id': 417, 'title': 'Pacific Atlantic Water Flow', 'url': 'https://leetcode.com/problems/pacific-atlantic-water-flow/', 'difficulty': 'Medium', 'category': 'Graphs'},
        
        # Dynamic Programming
        {'id': 70, 'title': 'Climbing Stairs', 'url': 'https://leetcode.com/problems/climbing-stairs/', 'difficulty': 'Easy', 'category': 'Dynamic Programming'},
        {'id': 198, 'title': 'House Robber', 'url': 'https://leetcode.com/problems/house-robber/', 'difficulty': 'Medium', 'category': 'Dynamic Programming'},
        {'id': 91, 'title': 'Decode Ways', 'url': 'https://leetcode.com/problems/decode-ways/', 'difficulty': 'Medium', 'category': 'Dynamic Programming'},
        {'id': 10, 'title': 'Regular Expression Matching', 'url': 'https://leetcode.com/problems/regular-expression-matching/', 'difficulty': 'Hard', 'category': 'Dynamic Programming'},
    ]
    
    # Add pattern and completion status
    for q in questions:
        q['pattern'] = q.get('pattern', '')
        q['completed'] = False
        q['date_completed'] = ''
    
    df = pd.DataFrame(questions)
    print(f"Created fallback list with {len(df)} questions")
    return df

if __name__ == "__main__":
    questions_df = fetch_neetcode_questions()
    if not questions_df.empty:
        print(f"Successfully fetched {len(questions_df)} questions")
        print(questions_df.head())
    else:
        print("Failed to fetch questions")