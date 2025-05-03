#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import string
import re
import requests
import importlib

# Ensure correct paths - use absolute path to the current script's directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_root = script_dir  # Set project_root to the current directory

# Add project_root to system path
sys.path.append(project_root)

# Import modules from correct paths
from src.scrapers.neetcode_scraper import fetch_neetcode_questions
from src.scrapers.csv_handler import CSVHandler
from src.scrapers.git_handler import GitHandler
from src.utils.solution_tester import SolutionTester

# Constants
CSV_PATH = os.path.join(project_root, "questions.csv")
SOLUTIONS_DIR = os.path.join(project_root, "questions")
TEMPLATE_PATH = os.path.join(project_root, "src", "templates", "solution_template.py")


def sanitize_filename(filename):
    """Convert a string to a valid filename"""
    # Replace spaces and special characters
    valid_chars = "-_" + string.ascii_letters + string.digits
    filename = ''.join(c if c in valid_chars else '_' for c in filename)
    return filename.lower()


def fetch_problem_description(url):
    """Try to fetch a problem description from LeetCode URL"""
    # This is a simplified implementation and may not work for all problems
    # LeetCode has anti-scraping measures
    try:
        problem_slug = url.strip('/').split('/')[-1]
        leetcode_api = f"https://leetcode.com/graphql"
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
                exampleTestcases
                difficulty
            }
        }
        """
        response = requests.post(leetcode_api, json={
            'query': query,
            'variables': {'titleSlug': problem_slug}
        })
        data = response.json()
        question_data = data.get('data', {}).get('question', {})
        
        # Process examples to ensure they don't contain format strings
        examples = question_data.get('exampleTestcases', '')
        # Escape any curly braces to prevent format string issues
        examples = examples.replace('{', '{{').replace('}', '}}')
        
        return {
            'title': question_data.get('title', ''),
            'description': question_data.get('content', '').replace('{', '{{').replace('}', '}}'),
            'examples': examples,
            'difficulty': question_data.get('difficulty', '')
        }
    except Exception as e:
        print(f"Failed to fetch problem description: {e}")
        return {
            'title': '',
            'description': 'Unable to fetch problem description automatically.',
            'examples': 'Please add examples manually.',
            'difficulty': ''
        }


def create_solution_file(question, template_path, solutions_dir):
    """Create a solution file from template"""
    # Create directory structure
    category_dir = os.path.join(solutions_dir, sanitize_filename(question['category']))
    difficulty_dir = os.path.join(category_dir, question['difficulty'].lower())
    
    os.makedirs(difficulty_dir, exist_ok=True)
    
    # Generate filename
    filename = f"{sanitize_filename(question['title'])}_solution.py"
    solution_path = os.path.join(difficulty_dir, filename)
    
    # Check if file already exists
    if os.path.exists(solution_path):
        print(f"Solution file already exists at {solution_path}")
        return solution_path
    
    # Create a default description if LeetCode API fails
    description = f"Solve the {question['title']} problem from LeetCode.\nPlease visit the URL for full description: {question['url']}"
    examples = "Please refer to LeetCode for examples."
    
    try:
        # Try to fetch problem details, but don't fail if it doesn't work
        problem_details = fetch_problem_description(question['url'])
        if problem_details.get('description') and problem_details['description'] != 'Unable to fetch problem description automatically.':
            description = problem_details['description']
        if problem_details.get('examples') and problem_details['examples'] != 'Please add examples manually.':
            examples = problem_details['examples']
    except Exception as e:
        print(f"Error fetching problem details: {e}")
        # Continue with default values
    
    # Read template
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Replace template placeholders manually to avoid format string issues
    solution_content = template
    replacements = {
        '{title}': question['title'],
        '{difficulty}': question['difficulty'],
        '{url}': question['url'],
        '{category}': question['category'],
        '{description}': description,
        '{examples}': examples
    }
    
    for placeholder, value in replacements.items():
        solution_content = solution_content.replace(placeholder, str(value))
    
    # Write solution file
    with open(solution_path, 'w') as file:
        file.write(solution_content)
    
    print(f"Created solution file at {solution_path}")
    return solution_path


def main():
    parser = argparse.ArgumentParser(description='NeetCode 150 DSA Tracker')
    parser.add_argument('--fetch', action='store_true', help='Fetch questions from NeetCode')
    parser.add_argument('--new', action='store_true', help='Get a new question to solve')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--difficulty', type=str, choices=['Easy', 'Medium', 'Hard'], 
                        help='Filter by difficulty')
    parser.add_argument('--test', type=str, help='Test a specific solution file')
    parser.add_argument('--commit', action='store_true', help='Commit and push changes to git')
    
    args = parser.parse_args()
    
    csv_handler = CSVHandler(CSV_PATH)
    git_handler = GitHandler(project_root)
    
    # Ensure git is initialized
    git_handler.ensure_git_initialized()
    
    # Fetch questions from NeetCode
    if args.fetch:
        questions_df = fetch_neetcode_questions()
        if not questions_df.empty:
            # Merge with existing data to preserve completion status
            existing_df = csv_handler.read_questions()
            if not existing_df.empty:
                # Keep track of completed questions
                completed_dict = {row['id']: (row['completed'], row['date_completed']) 
                                 for _, row in existing_df.iterrows() if row['completed']}
                
                # Update completion status in new dataframe
                for idx, row in questions_df.iterrows():
                    if row['id'] in completed_dict:
                        questions_df.at[idx, 'completed'] = completed_dict[row['id']][0]
                        questions_df.at[idx, 'date_completed'] = completed_dict[row['id']][1]
            
            csv_handler.save_questions(questions_df)
    
    # Get a new question
    if args.new:
        question = csv_handler.get_next_question(args.category, args.difficulty)
        if question is not None:
            print(f"\nNext question: {question['title']}")
            print(f"Difficulty: {question['difficulty']}")
            print(f"Category: {question['category']}")
            print(f"URL: {question['url']}")
            
            # Create solution file
            solution_path = create_solution_file(question, TEMPLATE_PATH, SOLUTIONS_DIR)
            print(f"\nPlease open {solution_path} to start coding your solution.")
        else:
            print("No matching uncompleted questions found.")
    
    # Test a solution
    if args.test:
        solution_path = args.test
        if not os.path.exists(solution_path):
            print(f"Solution file not found: {solution_path}")
            return
        
        tester = SolutionTester(solution_path)
        tests_passed = tester.run_tests()
        
        if tests_passed:
            print("All tests passed!")
            
            # Extract question ID from file path to update status
            filename = os.path.basename(solution_path)
            questions_df = csv_handler.read_questions()
            
            # Try to find matching question based on filename
            for idx, row in questions_df.iterrows():
                sanitized_title = sanitize_filename(row['title'])
                if sanitized_title in filename:
                    csv_handler.update_question_status(row['id'], completed=True)
                    break
    
    # Commit and push changes
    if args.commit:
        print("Committing and pushing changes to git...")
        message = f"Add solution for {datetime.now().strftime('%Y-%m-%d')}"
        result = git_handler.add_commit_push(message=message)
        if result:
            print("Changes successfully committed and pushed.")
        else:
            print("Failed to commit and push changes.")


if __name__ == "__main__":
    main()