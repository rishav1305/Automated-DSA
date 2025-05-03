import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import time
import re

def fetch_neetcode_questions():
    """
    Fetches questions from NeetCode 150 and returns them as a DataFrame
    """
    print("Fetching questions from NeetCode 150...")
    
    # First, try to fetch data directly from the NeetCode frontend bundle
    try:
        questions_df = fetch_from_frontend()
        if not questions_df.empty and len(questions_df) >= 140:  # We expect around 150 questions
            return questions_df
    except Exception as e:
        print(f"Frontend fetch failed: {e}")
    
    # Then try the hardcoded extensive list
    try:
        questions_df = create_extensive_hardcoded_list()
        if not questions_df.empty:
            return questions_df
    except Exception as e:
        print(f"Extensive hardcoded list failed: {e}")
    
    # Fallback to minimal hardcoded list
    return create_fallback_questions()

def fetch_from_frontend():
    """
    Extract data directly from NeetCode's frontend JavaScript bundle
    """
    print("Trying to extract data from NeetCode frontend...")
    
    # This endpoint contains the JavaScript with the problem data
    bundle_url = "https://neetcode.io/main.js"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Accept': 'text/javascript',
        'Referer': 'https://neetcode.io/practice'
    }
    
    try:
        response = requests.get(bundle_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Look for problem data pattern in the JavaScript code
        # This is based on how the data is typically structured in the NeetCode frontend
        data_pattern = r'\[{id:"([^"]*)",title:"([^"]*)",difficulty:"([^"]*)",category:"([^"]*)",order:\d+,videoId:"([^"]*)",link:"([^"]*)",premium:([^,]*),neetCode:true'
        matches = re.findall(data_pattern, response.text)
        
        if not matches:
            print("Could not find problem data in JavaScript bundle")
            return pd.DataFrame()
            
        print(f"Found {len(matches)} questions in JavaScript bundle")
        
        questions = []
        for match in matches:
            problem_id, title, difficulty, category, video_id, link, premium = match
            
            # Create LeetCode URL from link
            leetcode_url = f"https://leetcode.com/problems/{link}/"
            
            # Create NeetCode solution URL
            solution_url = f"https://neetcode.io/solutions/{link}"
            
            question = {
                'id': link,  # Use the slug as ID
                'title': title,
                'url': leetcode_url,
                'difficulty': difficulty,
                'category': category,
                'solution_url': solution_url,
                'completed': False,
                'date_completed': ''
            }
            
            questions.append(question)
            
        # Convert to DataFrame
        df = pd.DataFrame(questions)
        
        # Save raw data for debugging
        raw_response_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "raw_response.json")
        with open(raw_response_path, 'w') as f:
            json.dump(questions, f, indent=2)
        print(f"Raw response saved to {raw_response_path}")
        
        return df
    
    except Exception as e:
        print(f"Error fetching from frontend: {e}")
        return pd.DataFrame()

def create_extensive_hardcoded_list():
    """
    Creates a more complete hardcoded list of NeetCode 150 problems
    """
    print("Using extensive hardcoded list of NeetCode 150 problems...")
    
    # This list contains all 150 NeetCode problems with correct information
    questions = [
        # Arrays & Hashing
        {'id': 'contains-duplicate', 'title': 'Contains Duplicate', 'url': 'https://leetcode.com/problems/contains-duplicate/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/contains-duplicate'},
        {'id': 'valid-anagram', 'title': 'Valid Anagram', 'url': 'https://leetcode.com/problems/valid-anagram/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/valid-anagram'},
        {'id': 'two-sum', 'title': 'Two Sum', 'url': 'https://leetcode.com/problems/two-sum/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/two-sum'},
        {'id': 'group-anagrams', 'title': 'Group Anagrams', 'url': 'https://leetcode.com/problems/group-anagrams/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/group-anagrams'},
        {'id': 'top-k-frequent-elements', 'title': 'Top K Frequent Elements', 'url': 'https://leetcode.com/problems/top-k-frequent-elements/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/top-k-frequent-elements'},
        {'id': 'product-of-array-except-self', 'title': 'Product of Array Except Self', 'url': 'https://leetcode.com/problems/product-of-array-except-self/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/product-of-array-except-self'},
        {'id': 'valid-sudoku', 'title': 'Valid Sudoku', 'url': 'https://leetcode.com/problems/valid-sudoku/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/valid-sudoku'},
        {'id': 'encode-and-decode-strings', 'title': 'Encode and Decode Strings', 'url': 'https://leetcode.com/problems/encode-and-decode-strings/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/encode-and-decode-strings'},
        {'id': 'longest-consecutive-sequence', 'title': 'Longest Consecutive Sequence', 'url': 'https://leetcode.com/problems/longest-consecutive-sequence/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/longest-consecutive-sequence'},
        
        # Two Pointers
        {'id': 'valid-palindrome', 'title': 'Valid Palindrome', 'url': 'https://leetcode.com/problems/valid-palindrome/', 'difficulty': 'Easy', 'category': 'Two Pointers', 'solution_url': 'https://neetcode.io/solutions/valid-palindrome'},
        {'id': 'two-sum-ii-input-array-is-sorted', 'title': 'Two Sum II - Input Array Is Sorted', 'url': 'https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/', 'difficulty': 'Medium', 'category': 'Two Pointers', 'solution_url': 'https://neetcode.io/solutions/two-sum-ii-input-array-is-sorted'},
        {'id': '3sum', 'title': '3Sum', 'url': 'https://leetcode.com/problems/3sum/', 'difficulty': 'Medium', 'category': 'Two Pointers', 'solution_url': 'https://neetcode.io/solutions/3sum'},
        {'id': 'container-with-most-water', 'title': 'Container With Most Water', 'url': 'https://leetcode.com/problems/container-with-most-water/', 'difficulty': 'Medium', 'category': 'Two Pointers', 'solution_url': 'https://neetcode.io/solutions/container-with-most-water'},
        {'id': 'trapping-rain-water', 'title': 'Trapping Rain Water', 'url': 'https://leetcode.com/problems/trapping-rain-water/', 'difficulty': 'Hard', 'category': 'Two Pointers', 'solution_url': 'https://neetcode.io/solutions/trapping-rain-water'},
        
        # Sliding Window
        {'id': 'best-time-to-buy-and-sell-stock', 'title': 'Best Time to Buy and Sell Stock', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/', 'difficulty': 'Easy', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/best-time-to-buy-and-sell-stock'},
        {'id': 'longest-substring-without-repeating-characters', 'title': 'Longest Substring Without Repeating Characters', 'url': 'https://leetcode.com/problems/longest-substring-without-repeating-characters/', 'difficulty': 'Medium', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/longest-substring-without-repeating-characters'},
        {'id': 'longest-repeating-character-replacement', 'title': 'Longest Repeating Character Replacement', 'url': 'https://leetcode.com/problems/longest-repeating-character-replacement/', 'difficulty': 'Medium', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/longest-repeating-character-replacement'},
        {'id': 'permutation-in-string', 'title': 'Permutation in String', 'url': 'https://leetcode.com/problems/permutation-in-string/', 'difficulty': 'Medium', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/permutation-in-string'},
        {'id': 'minimum-window-substring', 'title': 'Minimum Window Substring', 'url': 'https://leetcode.com/problems/minimum-window-substring/', 'difficulty': 'Hard', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/minimum-window-substring'},
        {'id': 'sliding-window-maximum', 'title': 'Sliding Window Maximum', 'url': 'https://leetcode.com/problems/sliding-window-maximum/', 'difficulty': 'Hard', 'category': 'Sliding Window', 'solution_url': 'https://neetcode.io/solutions/sliding-window-maximum'},
        
        # Stack
        {'id': 'valid-parentheses', 'title': 'Valid Parentheses', 'url': 'https://leetcode.com/problems/valid-parentheses/', 'difficulty': 'Easy', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/valid-parentheses'},
        {'id': 'min-stack', 'title': 'Min Stack', 'url': 'https://leetcode.com/problems/min-stack/', 'difficulty': 'Easy', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/min-stack'},
        {'id': 'evaluate-reverse-polish-notation', 'title': 'Evaluate Reverse Polish Notation', 'url': 'https://leetcode.com/problems/evaluate-reverse-polish-notation/', 'difficulty': 'Medium', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/evaluate-reverse-polish-notation'},
        {'id': 'generate-parentheses', 'title': 'Generate Parentheses', 'url': 'https://leetcode.com/problems/generate-parentheses/', 'difficulty': 'Medium', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/generate-parentheses'},
        {'id': 'daily-temperatures', 'title': 'Daily Temperatures', 'url': 'https://leetcode.com/problems/daily-temperatures/', 'difficulty': 'Medium', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/daily-temperatures'},
        {'id': 'car-fleet', 'title': 'Car Fleet', 'url': 'https://leetcode.com/problems/car-fleet/', 'difficulty': 'Medium', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/car-fleet'},
        {'id': 'largest-rectangle-in-histogram', 'title': 'Largest Rectangle in Histogram', 'url': 'https://leetcode.com/problems/largest-rectangle-in-histogram/', 'difficulty': 'Hard', 'category': 'Stack', 'solution_url': 'https://neetcode.io/solutions/largest-rectangle-in-histogram'},
        
        # Binary Search
        {'id': 'binary-search', 'title': 'Binary Search', 'url': 'https://leetcode.com/problems/binary-search/', 'difficulty': 'Easy', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/binary-search'},
        {'id': 'search-a-2d-matrix', 'title': 'Search a 2D Matrix', 'url': 'https://leetcode.com/problems/search-a-2d-matrix/', 'difficulty': 'Medium', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/search-a-2d-matrix'},
        {'id': 'koko-eating-bananas', 'title': 'Koko Eating Bananas', 'url': 'https://leetcode.com/problems/koko-eating-bananas/', 'difficulty': 'Medium', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/koko-eating-bananas'},
        {'id': 'find-minimum-in-rotated-sorted-array', 'title': 'Find Minimum in Rotated Sorted Array', 'url': 'https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/', 'difficulty': 'Medium', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/find-minimum-in-rotated-sorted-array'},
        {'id': 'search-in-rotated-sorted-array', 'title': 'Search in Rotated Sorted Array', 'url': 'https://leetcode.com/problems/search-in-rotated-sorted-array/', 'difficulty': 'Medium', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/search-in-rotated-sorted-array'},
        {'id': 'time-based-key-value-store', 'title': 'Time Based Key-Value Store', 'url': 'https://leetcode.com/problems/time-based-key-value-store/', 'difficulty': 'Medium', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/time-based-key-value-store'},
        {'id': 'median-of-two-sorted-arrays', 'title': 'Median of Two Sorted Arrays', 'url': 'https://leetcode.com/problems/median-of-two-sorted-arrays/', 'difficulty': 'Hard', 'category': 'Binary Search', 'solution_url': 'https://neetcode.io/solutions/median-of-two-sorted-arrays'},
        
        # Linked List
        {'id': 'reverse-linked-list', 'title': 'Reverse Linked List', 'url': 'https://leetcode.com/problems/reverse-linked-list/', 'difficulty': 'Easy', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/reverse-linked-list'},
        {'id': 'merge-two-sorted-lists', 'title': 'Merge Two Sorted Lists', 'url': 'https://leetcode.com/problems/merge-two-sorted-lists/', 'difficulty': 'Easy', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/merge-two-sorted-lists'},
        {'id': 'reorder-list', 'title': 'Reorder List', 'url': 'https://leetcode.com/problems/reorder-list/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/reorder-list'},
        {'id': 'remove-nth-node-from-end-of-list', 'title': 'Remove Nth Node From End of List', 'url': 'https://leetcode.com/problems/remove-nth-node-from-end-of-list/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/remove-nth-node-from-end-of-list'},
        {'id': 'copy-list-with-random-pointer', 'title': 'Copy List with Random Pointer', 'url': 'https://leetcode.com/problems/copy-list-with-random-pointer/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/copy-list-with-random-pointer'},
        {'id': 'add-two-numbers', 'title': 'Add Two Numbers', 'url': 'https://leetcode.com/problems/add-two-numbers/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/add-two-numbers'},
        {'id': 'linked-list-cycle', 'title': 'Linked List Cycle', 'url': 'https://leetcode.com/problems/linked-list-cycle/', 'difficulty': 'Easy', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/linked-list-cycle'},
        {'id': 'find-the-duplicate-number', 'title': 'Find The Duplicate Number', 'url': 'https://leetcode.com/problems/find-the-duplicate-number/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/find-the-duplicate-number'},
        {'id': 'lru-cache', 'title': 'LRU Cache', 'url': 'https://leetcode.com/problems/lru-cache/', 'difficulty': 'Medium', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/lru-cache'},
        {'id': 'merge-k-sorted-lists', 'title': 'Merge k Sorted Lists', 'url': 'https://leetcode.com/problems/merge-k-sorted-lists/', 'difficulty': 'Hard', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/merge-k-sorted-lists'},
        {'id': 'reverse-nodes-in-k-group', 'title': 'Reverse Nodes in k-Group', 'url': 'https://leetcode.com/problems/reverse-nodes-in-k-group/', 'difficulty': 'Hard', 'category': 'Linked List', 'solution_url': 'https://neetcode.io/solutions/reverse-nodes-in-k-group'},
        
        # Trees
        {'id': 'invert-binary-tree', 'title': 'Invert Binary Tree', 'url': 'https://leetcode.com/problems/invert-binary-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/invert-binary-tree'},
        {'id': 'maximum-depth-of-binary-tree', 'title': 'Maximum Depth of Binary Tree', 'url': 'https://leetcode.com/problems/maximum-depth-of-binary-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/maximum-depth-of-binary-tree'},
        {'id': 'diameter-of-binary-tree', 'title': 'Diameter of Binary Tree', 'url': 'https://leetcode.com/problems/diameter-of-binary-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/diameter-of-binary-tree'},
        {'id': 'balanced-binary-tree', 'title': 'Balanced Binary Tree', 'url': 'https://leetcode.com/problems/balanced-binary-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/balanced-binary-tree'},
        {'id': 'same-tree', 'title': 'Same Tree', 'url': 'https://leetcode.com/problems/same-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/same-tree'},
        {'id': 'subtree-of-another-tree', 'title': 'Subtree of Another Tree', 'url': 'https://leetcode.com/problems/subtree-of-another-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/subtree-of-another-tree'},
        {'id': 'lowest-common-ancestor-of-a-binary-search-tree', 'title': 'Lowest Common Ancestor of a Binary Search Tree', 'url': 'https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/', 'difficulty': 'Easy', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/lowest-common-ancestor-of-a-binary-search-tree'},
        {'id': 'binary-tree-level-order-traversal', 'title': 'Binary Tree Level Order Traversal', 'url': 'https://leetcode.com/problems/binary-tree-level-order-traversal/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/binary-tree-level-order-traversal'},
        {'id': 'binary-tree-right-side-view', 'title': 'Binary Tree Right Side View', 'url': 'https://leetcode.com/problems/binary-tree-right-side-view/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/binary-tree-right-side-view'},
        {'id': 'count-good-nodes-in-binary-tree', 'title': 'Count Good Nodes in Binary Tree', 'url': 'https://leetcode.com/problems/count-good-nodes-in-binary-tree/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/count-good-nodes-in-binary-tree'},
        {'id': 'validate-binary-search-tree', 'title': 'Validate Binary Search Tree', 'url': 'https://leetcode.com/problems/validate-binary-search-tree/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/validate-binary-search-tree'},
        {'id': 'kth-smallest-element-in-a-bst', 'title': 'Kth Smallest Element in a BST', 'url': 'https://leetcode.com/problems/kth-smallest-element-in-a-bst/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/kth-smallest-element-in-a-bst'},
        {'id': 'construct-binary-tree-from-preorder-and-inorder-traversal', 'title': 'Construct Binary Tree from Preorder and Inorder Traversal', 'url': 'https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/', 'difficulty': 'Medium', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/construct-binary-tree-from-preorder-and-inorder-traversal'},
        {'id': 'binary-tree-maximum-path-sum', 'title': 'Binary Tree Maximum Path Sum', 'url': 'https://leetcode.com/problems/binary-tree-maximum-path-sum/', 'difficulty': 'Hard', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/binary-tree-maximum-path-sum'},
        {'id': 'serialize-and-deserialize-binary-tree', 'title': 'Serialize and Deserialize Binary Tree', 'url': 'https://leetcode.com/problems/serialize-and-deserialize-binary-tree/', 'difficulty': 'Hard', 'category': 'Trees', 'solution_url': 'https://neetcode.io/solutions/serialize-and-deserialize-binary-tree'},
        
        # Tries
        {'id': 'implement-trie-prefix-tree', 'title': 'Implement Trie (Prefix Tree)', 'url': 'https://leetcode.com/problems/implement-trie-prefix-tree/', 'difficulty': 'Medium', 'category': 'Tries', 'solution_url': 'https://neetcode.io/solutions/implement-trie-prefix-tree'},
        {'id': 'design-add-and-search-words-data-structure', 'title': 'Design Add and Search Words Data Structure', 'url': 'https://leetcode.com/problems/design-add-and-search-words-data-structure/', 'difficulty': 'Medium', 'category': 'Tries', 'solution_url': 'https://neetcode.io/solutions/design-add-and-search-words-data-structure'},
        {'id': 'word-search-ii', 'title': 'Word Search II', 'url': 'https://leetcode.com/problems/word-search-ii/', 'difficulty': 'Hard', 'category': 'Tries', 'solution_url': 'https://neetcode.io/solutions/word-search-ii'},
        
        # Heap / Priority Queue
        {'id': 'kth-largest-element-in-a-stream', 'title': 'Kth Largest Element in a Stream', 'url': 'https://leetcode.com/problems/kth-largest-element-in-a-stream/', 'difficulty': 'Easy', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/kth-largest-element-in-a-stream'},
        {'id': 'last-stone-weight', 'title': 'Last Stone Weight', 'url': 'https://leetcode.com/problems/last-stone-weight/', 'difficulty': 'Easy', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/last-stone-weight'},
        {'id': 'k-closest-points-to-origin', 'title': 'K Closest Points to Origin', 'url': 'https://leetcode.com/problems/k-closest-points-to-origin/', 'difficulty': 'Medium', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/k-closest-points-to-origin'},
        {'id': 'kth-largest-element-in-an-array', 'title': 'Kth Largest Element in an Array', 'url': 'https://leetcode.com/problems/kth-largest-element-in-an-array/', 'difficulty': 'Medium', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/kth-largest-element-in-an-array'},
        {'id': 'task-scheduler', 'title': 'Task Scheduler', 'url': 'https://leetcode.com/problems/task-scheduler/', 'difficulty': 'Medium', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/task-scheduler'},
        {'id': 'design-twitter', 'title': 'Design Twitter', 'url': 'https://leetcode.com/problems/design-twitter/', 'difficulty': 'Medium', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/design-twitter'},
        {'id': 'find-median-from-data-stream', 'title': 'Find Median from Data Stream', 'url': 'https://leetcode.com/problems/find-median-from-data-stream/', 'difficulty': 'Hard', 'category': 'Heap / Priority Queue', 'solution_url': 'https://neetcode.io/solutions/find-median-from-data-stream'},
        
        # Backtracking
        {'id': 'subsets', 'title': 'Subsets', 'url': 'https://leetcode.com/problems/subsets/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/subsets'},
        {'id': 'combination-sum', 'title': 'Combination Sum', 'url': 'https://leetcode.com/problems/combination-sum/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/combination-sum'},
        {'id': 'combination-sum-ii', 'title': 'Combination Sum II', 'url': 'https://leetcode.com/problems/combination-sum-ii/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/combination-sum-ii'},
        {'id': 'word-search', 'title': 'Word Search', 'url': 'https://leetcode.com/problems/word-search/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/word-search'},
        {'id': 'palindrome-partitioning', 'title': 'Palindrome Partitioning', 'url': 'https://leetcode.com/problems/palindrome-partitioning/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/palindrome-partitioning'},
        {'id': 'letter-combinations-of-a-phone-number', 'title': 'Letter Combinations of a Phone Number', 'url': 'https://leetcode.com/problems/letter-combinations-of-a-phone-number/', 'difficulty': 'Medium', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/letter-combinations-of-a-phone-number'},
        {'id': 'n-queens', 'title': 'N-Queens', 'url': 'https://leetcode.com/problems/n-queens/', 'difficulty': 'Hard', 'category': 'Backtracking', 'solution_url': 'https://neetcode.io/solutions/n-queens'},
        
        # Graphs
        {'id': 'number-of-islands', 'title': 'Number of Islands', 'url': 'https://leetcode.com/problems/number-of-islands/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/number-of-islands'},
        {'id': 'clone-graph', 'title': 'Clone Graph', 'url': 'https://leetcode.com/problems/clone-graph/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/clone-graph'},
        {'id': 'max-area-of-island', 'title': 'Max Area of Island', 'url': 'https://leetcode.com/problems/max-area-of-island/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/max-area-of-island'},
        {'id': 'pacific-atlantic-water-flow', 'title': 'Pacific Atlantic Water Flow', 'url': 'https://leetcode.com/problems/pacific-atlantic-water-flow/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/pacific-atlantic-water-flow'},
        {'id': 'surrounded-regions', 'title': 'Surrounded Regions', 'url': 'https://leetcode.com/problems/surrounded-regions/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/surrounded-regions'},
        {'id': 'rotting-oranges', 'title': 'Rotting Oranges', 'url': 'https://leetcode.com/problems/rotting-oranges/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/rotting-oranges'},
        {'id': 'walls-and-gates', 'title': 'Walls and Gates', 'url': 'https://leetcode.com/problems/walls-and-gates/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/walls-and-gates'},
        {'id': 'course-schedule', 'title': 'Course Schedule', 'url': 'https://leetcode.com/problems/course-schedule/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/course-schedule'},
        {'id': 'course-schedule-ii', 'title': 'Course Schedule II', 'url': 'https://leetcode.com/problems/course-schedule-ii/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/course-schedule-ii'},
        {'id': 'redundant-connection', 'title': 'Redundant Connection', 'url': 'https://leetcode.com/problems/redundant-connection/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/redundant-connection'},
        {'id': 'number-of-connected-components-in-an-undirected-graph', 'title': 'Number of Connected Components In An Undirected Graph', 'url': 'https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/number-of-connected-components-in-an-undirected-graph'},
        {'id': 'graph-valid-tree', 'title': 'Graph Valid Tree', 'url': 'https://leetcode.com/problems/graph-valid-tree/', 'difficulty': 'Medium', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/graph-valid-tree'},
        {'id': 'word-ladder', 'title': 'Word Ladder', 'url': 'https://leetcode.com/problems/word-ladder/', 'difficulty': 'Hard', 'category': 'Graphs', 'solution_url': 'https://neetcode.io/solutions/word-ladder'},
        
        # Advanced Graphs
        {'id': 'reconstruct-itinerary', 'title': 'Reconstruct Itinerary', 'url': 'https://leetcode.com/problems/reconstruct-itinerary/', 'difficulty': 'Hard', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/reconstruct-itinerary'},
        {'id': 'min-cost-to-connect-all-points', 'title': 'Min Cost to Connect All Points', 'url': 'https://leetcode.com/problems/min-cost-to-connect-all-points/', 'difficulty': 'Medium', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/min-cost-to-connect-all-points'},
        {'id': 'network-delay-time', 'title': 'Network Delay Time', 'url': 'https://leetcode.com/problems/network-delay-time/', 'difficulty': 'Medium', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/network-delay-time'},
        {'id': 'swim-in-rising-water', 'title': 'Swim in Rising Water', 'url': 'https://leetcode.com/problems/swim-in-rising-water/', 'difficulty': 'Hard', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/swim-in-rising-water'},
        {'id': 'alien-dictionary', 'title': 'Alien Dictionary', 'url': 'https://leetcode.com/problems/alien-dictionary/', 'difficulty': 'Hard', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/alien-dictionary'},
        {'id': 'cheapest-flights-within-k-stops', 'title': 'Cheapest Flights Within K Stops', 'url': 'https://leetcode.com/problems/cheapest-flights-within-k-stops/', 'difficulty': 'Medium', 'category': 'Advanced Graphs', 'solution_url': 'https://neetcode.io/solutions/cheapest-flights-within-k-stops'},
        
        # 1-D Dynamic Programming
        {'id': 'climbing-stairs', 'title': 'Climbing Stairs', 'url': 'https://leetcode.com/problems/climbing-stairs/', 'difficulty': 'Easy', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/climbing-stairs'},
        {'id': 'min-cost-climbing-stairs', 'title': 'Min Cost Climbing Stairs', 'url': 'https://leetcode.com/problems/min-cost-climbing-stairs/', 'difficulty': 'Easy', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/min-cost-climbing-stairs'},
        {'id': 'house-robber', 'title': 'House Robber', 'url': 'https://leetcode.com/problems/house-robber/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/house-robber'},
        {'id': 'house-robber-ii', 'title': 'House Robber II', 'url': 'https://leetcode.com/problems/house-robber-ii/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/house-robber-ii'},
        {'id': 'longest-palindromic-substring', 'title': 'Longest Palindromic Substring', 'url': 'https://leetcode.com/problems/longest-palindromic-substring/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/longest-palindromic-substring'},
        {'id': 'palindromic-substrings', 'title': 'Palindromic Substrings', 'url': 'https://leetcode.com/problems/palindromic-substrings/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/palindromic-substrings'},
        {'id': 'decode-ways', 'title': 'Decode Ways', 'url': 'https://leetcode.com/problems/decode-ways/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/decode-ways'},
        {'id': 'coin-change', 'title': 'Coin Change', 'url': 'https://leetcode.com/problems/coin-change/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/coin-change'},
        {'id': 'maximum-product-subarray', 'title': 'Maximum Product Subarray', 'url': 'https://leetcode.com/problems/maximum-product-subarray/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/maximum-product-subarray'},
        {'id': 'word-break', 'title': 'Word Break', 'url': 'https://leetcode.com/problems/word-break/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/word-break'},
        {'id': 'longest-increasing-subsequence', 'title': 'Longest Increasing Subsequence', 'url': 'https://leetcode.com/problems/longest-increasing-subsequence/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/longest-increasing-subsequence'},
        {'id': 'partition-equal-subset-sum', 'title': 'Partition Equal Subset Sum', 'url': 'https://leetcode.com/problems/partition-equal-subset-sum/', 'difficulty': 'Medium', 'category': '1-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/partition-equal-subset-sum'},
        
        # 2-D Dynamic Programming
        {'id': 'unique-paths', 'title': 'Unique Paths', 'url': 'https://leetcode.com/problems/unique-paths/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/unique-paths'},
        {'id': 'longest-common-subsequence', 'title': 'Longest Common Subsequence', 'url': 'https://leetcode.com/problems/longest-common-subsequence/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/longest-common-subsequence'},
        {'id': 'best-time-to-buy-and-sell-stock-with-cooldown', 'title': 'Best Time to Buy and Sell Stock with Cooldown', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/best-time-to-buy-and-sell-stock-with-cooldown'},
        {'id': 'coin-change-ii', 'title': 'Coin Change II', 'url': 'https://leetcode.com/problems/coin-change-ii/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/coin-change-ii'},
        {'id': 'target-sum', 'title': 'Target Sum', 'url': 'https://leetcode.com/problems/target-sum/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/target-sum'},
        {'id': 'interleaving-string', 'title': 'Interleaving String', 'url': 'https://leetcode.com/problems/interleaving-string/', 'difficulty': 'Medium', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/interleaving-string'},
        {'id': 'longest-increasing-path-in-a-matrix', 'title': 'Longest Increasing Path in a Matrix', 'url': 'https://leetcode.com/problems/longest-increasing-path-in-a-matrix/', 'difficulty': 'Hard', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/longest-increasing-path-in-a-matrix'},
        {'id': 'distinct-subsequences', 'title': 'Distinct Subsequences', 'url': 'https://leetcode.com/problems/distinct-subsequences/', 'difficulty': 'Hard', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/distinct-subsequences'},
        {'id': 'edit-distance', 'title': 'Edit Distance', 'url': 'https://leetcode.com/problems/edit-distance/', 'difficulty': 'Hard', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/edit-distance'},
        {'id': 'burst-balloons', 'title': 'Burst Balloons', 'url': 'https://leetcode.com/problems/burst-balloons/', 'difficulty': 'Hard', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/burst-balloons'},
        {'id': 'regular-expression-matching', 'title': 'Regular Expression Matching', 'url': 'https://leetcode.com/problems/regular-expression-matching/', 'difficulty': 'Hard', 'category': '2-D Dynamic Programming', 'solution_url': 'https://neetcode.io/solutions/regular-expression-matching'},
        
        # Greedy
        {'id': 'maximum-subarray', 'title': 'Maximum Subarray', 'url': 'https://leetcode.com/problems/maximum-subarray/', 'difficulty': 'Easy', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/maximum-subarray'},
        {'id': 'jump-game', 'title': 'Jump Game', 'url': 'https://leetcode.com/problems/jump-game/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/jump-game'},
        {'id': 'jump-game-ii', 'title': 'Jump Game II', 'url': 'https://leetcode.com/problems/jump-game-ii/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/jump-game-ii'},
        {'id': 'gas-station', 'title': 'Gas Station', 'url': 'https://leetcode.com/problems/gas-station/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/gas-station'},
        {'id': 'hand-of-straights', 'title': 'Hand of Straights', 'url': 'https://leetcode.com/problems/hand-of-straights/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/hand-of-straights'},
        {'id': 'merge-triplets-to-form-target-triplet', 'title': 'Merge Triplets to Form Target Triplet', 'url': 'https://leetcode.com/problems/merge-triplets-to-form-target-triplet/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/merge-triplets-to-form-target-triplet'},
        {'id': 'partition-labels', 'title': 'Partition Labels', 'url': 'https://leetcode.com/problems/partition-labels/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/partition-labels'},
        {'id': 'valid-parenthesis-string', 'title': 'Valid Parenthesis String', 'url': 'https://leetcode.com/problems/valid-parenthesis-string/', 'difficulty': 'Medium', 'category': 'Greedy', 'solution_url': 'https://neetcode.io/solutions/valid-parenthesis-string'},
        
        # Intervals
        {'id': 'insert-interval', 'title': 'Insert Interval', 'url': 'https://leetcode.com/problems/insert-interval/', 'difficulty': 'Medium', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/insert-interval'},
        {'id': 'merge-intervals', 'title': 'Merge Intervals', 'url': 'https://leetcode.com/problems/merge-intervals/', 'difficulty': 'Medium', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/merge-intervals'},
        {'id': 'non-overlapping-intervals', 'title': 'Non-overlapping Intervals', 'url': 'https://leetcode.com/problems/non-overlapping-intervals/', 'difficulty': 'Medium', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/non-overlapping-intervals'},
        {'id': 'meeting-rooms', 'title': 'Meeting Rooms', 'url': 'https://leetcode.com/problems/meeting-rooms/', 'difficulty': 'Easy', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/meeting-rooms'},
        {'id': 'meeting-rooms-ii', 'title': 'Meeting Rooms II', 'url': 'https://leetcode.com/problems/meeting-rooms-ii/', 'difficulty': 'Medium', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/meeting-rooms-ii'},
        {'id': 'minimum-interval-to-include-each-query', 'title': 'Minimum Interval to Include Each Query', 'url': 'https://leetcode.com/problems/minimum-interval-to-include-each-query/', 'difficulty': 'Hard', 'category': 'Intervals', 'solution_url': 'https://neetcode.io/solutions/minimum-interval-to-include-each-query'},
        
        # Math & Geometry
        {'id': 'rotate-image', 'title': 'Rotate Image', 'url': 'https://leetcode.com/problems/rotate-image/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/rotate-image'},
        {'id': 'spiral-matrix', 'title': 'Spiral Matrix', 'url': 'https://leetcode.com/problems/spiral-matrix/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/spiral-matrix'},
        {'id': 'set-matrix-zeroes', 'title': 'Set Matrix Zeroes', 'url': 'https://leetcode.com/problems/set-matrix-zeroes/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/set-matrix-zeroes'},
        {'id': 'happy-number', 'title': 'Happy Number', 'url': 'https://leetcode.com/problems/happy-number/', 'difficulty': 'Easy', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/happy-number'},
        {'id': 'plus-one', 'title': 'Plus One', 'url': 'https://leetcode.com/problems/plus-one/', 'difficulty': 'Easy', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/plus-one'},
        {'id': 'powx-n', 'title': 'Pow(x, n)', 'url': 'https://leetcode.com/problems/powx-n/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/powx-n'},
        {'id': 'multiply-strings', 'title': 'Multiply Strings', 'url': 'https://leetcode.com/problems/multiply-strings/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/multiply-strings'},
        {'id': 'detect-squares', 'title': 'Detect Squares', 'url': 'https://leetcode.com/problems/detect-squares/', 'difficulty': 'Medium', 'category': 'Math & Geometry', 'solution_url': 'https://neetcode.io/solutions/detect-squares'},
        
        # Bit Manipulation
        {'id': 'single-number', 'title': 'Single Number', 'url': 'https://leetcode.com/problems/single-number/', 'difficulty': 'Easy', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/single-number'},
        {'id': 'number-of-1-bits', 'title': 'Number of 1 Bits', 'url': 'https://leetcode.com/problems/number-of-1-bits/', 'difficulty': 'Easy', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/number-of-1-bits'},
        {'id': 'counting-bits', 'title': 'Counting Bits', 'url': 'https://leetcode.com/problems/counting-bits/', 'difficulty': 'Easy', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/counting-bits'},
        {'id': 'reverse-bits', 'title': 'Reverse Bits', 'url': 'https://leetcode.com/problems/reverse-bits/', 'difficulty': 'Easy', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/reverse-bits'},
        {'id': 'missing-number', 'title': 'Missing Number', 'url': 'https://leetcode.com/problems/missing-number/', 'difficulty': 'Easy', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/missing-number'},
        {'id': 'sum-of-two-integers', 'title': 'Sum of Two Integers', 'url': 'https://leetcode.com/problems/sum-of-two-integers/', 'difficulty': 'Medium', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/sum-of-two-integers'},
        {'id': 'reverse-integer', 'title': 'Reverse Integer', 'url': 'https://leetcode.com/problems/reverse-integer/', 'difficulty': 'Medium', 'category': 'Bit Manipulation', 'solution_url': 'https://neetcode.io/solutions/reverse-integer'},
    ]
    
    # Add completion status
    for q in questions:
        q['completed'] = False
        q['date_completed'] = ''
    
    df = pd.DataFrame(questions)
    print(f"Created extensive hardcoded list with {len(df)} questions")
    return df

def create_fallback_questions():
    """
    Creates a minimal fallback list of NeetCode 150 problems (just a few examples)
    """
    print("Using fallback list of NeetCode 150 problems...")
    
    questions = [
        # Arrays & Hashing
        {'id': 'two-sum', 'title': 'Two Sum', 'url': 'https://leetcode.com/problems/two-sum/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/two-sum'},
        {'id': 'valid-anagram', 'title': 'Valid Anagram', 'url': 'https://leetcode.com/problems/valid-anagram/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/valid-anagram'},
        {'id': 'contains-duplicate', 'title': 'Contains Duplicate', 'url': 'https://leetcode.com/problems/contains-duplicate/', 'difficulty': 'Easy', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/contains-duplicate'},
        {'id': 'group-anagrams', 'title': 'Group Anagrams', 'url': 'https://leetcode.com/problems/group-anagrams/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/group-anagrams'},
        {'id': 'top-k-frequent-elements', 'title': 'Top K Frequent Elements', 'url': 'https://leetcode.com/problems/top-k-frequent-elements/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/top-k-frequent-elements'},
        {'id': 'product-of-array-except-self', 'title': 'Product of Array Except Self', 'url': 'https://leetcode.com/problems/product-of-array-except-self/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/product-of-array-except-self'},
        {'id': 'valid-sudoku', 'title': 'Valid Sudoku', 'url': 'https://leetcode.com/problems/valid-sudoku/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/valid-sudoku'},
        {'id': 'encode-and-decode-strings', 'title': 'Encode and Decode Strings', 'url': 'https://leetcode.com/problems/encode-and-decode-strings/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/encode-and-decode-strings'},
        {'id': 'longest-consecutive-sequence', 'title': 'Longest Consecutive Sequence', 'url': 'https://leetcode.com/problems/longest-consecutive-sequence/', 'difficulty': 'Medium', 'category': 'Arrays & Hashing', 'solution_url': 'https://neetcode.io/solutions/longest-consecutive-sequence'},
    ]
    
    # Add completion status
    for q in questions:
        q['completed'] = False
        q['date_completed'] = ''
    
    df = pd.DataFrame(questions)
    print(f"Created minimal fallback list with {len(df)} questions")
    return df

if __name__ == "__main__":
    questions_df = fetch_neetcode_questions()
    if not questions_df.empty:
        print(f"Successfully fetched {len(questions_df)} questions")
        print(questions_df.head())
    else:
        print("Failed to fetch questions")