import re
import json
import ast

class TestCaseGenerator:
    """
    Utility class to automatically generate test cases from problem descriptions
    """
    
    @staticmethod
    def extract_examples_from_description(description):
        """
        Extract examples from a problem description
        
        Args:
            description (str): The problem description containing examples
            
        Returns:
            list: List of examples with inputs and outputs
        """
        examples = []
        
        # Look for input/output patterns in the description
        input_pattern = r"<strong>Input:</strong>.*?</strong>"
        output_pattern = r"<strong>Output:</strong>.*?</strong>"
        
        # Alternative patterns
        alt_input_pattern = r"Input:.*?\n"
        alt_output_pattern = r"Output:.*?\n"
        
        # Try to find matches using regex patterns
        input_matches = re.findall(input_pattern, description) or re.findall(alt_input_pattern, description)
        output_matches = re.findall(output_pattern, description) or re.findall(alt_output_pattern, description)
        
        # Extract input and output values
        for i, (input_match, output_match) in enumerate(zip(input_matches, output_matches)):
            try:
                # Extract the input values
                input_text = input_match.split("Input:")[1].strip()
                
                # Extract the output values
                output_text = output_match.split("Output:")[1].strip()
                
                # Clean up the values (remove HTML tags)
                input_text = re.sub(r"<.*?>", "", input_text).strip()
                output_text = re.sub(r"<.*?>", "", output_text).strip()
                
                # Convert to Python literals safely
                examples.append({
                    'input': input_text,
                    'output': output_text
                })
            except Exception as e:
                print(f"Error parsing example {i+1}: {e}")
        
        return examples
    
    @staticmethod
    def parse_input_string(input_str):
        """
        Parse an input string into Python objects
        
        Args:
            input_str (str): The input string to parse
            
        Returns:
            tuple: The parsed input values
        """
        try:
            # Try to identify array or numeric patterns
            # Look for array pattern [x,y,z]
            array_match = re.search(r'\[.*?\]', input_str)
            
            # Look for multiple inputs separated by commas
            if ',' in input_str:
                # Split by commas outside of brackets
                parts = []
                current_part = ""
                bracket_count = 0
                
                for char in input_str:
                    if char == '[':
                        bracket_count += 1
                        current_part += char
                    elif char == ']':
                        bracket_count -= 1
                        current_part += char
                    elif char == ',' and bracket_count == 0:
                        parts.append(current_part.strip())
                        current_part = ""
                    else:
                        current_part += char
                
                if current_part:
                    parts.append(current_part.strip())
                
                # Parse each part
                parsed_parts = []
                for part in parts:
                    # Check if it looks like a variable assignment
                    if '=' in part:
                        var_name, var_value = part.split('=', 1)
                        parsed_value = TestCaseGenerator.parse_single_value(var_value.strip())
                        parsed_parts.append(parsed_value)
                    else:
                        parsed_parts.append(TestCaseGenerator.parse_single_value(part))
                
                return tuple(parsed_parts)
            else:
                # Single input
                return TestCaseGenerator.parse_single_value(input_str)
        except Exception as e:
            print(f"Error parsing input: {e}")
            return input_str
    
    @staticmethod
    def parse_single_value(value_str):
        """
        Parse a single value string into a Python object
        
        Args:
            value_str (str): The value string to parse
            
        Returns:
            object: The parsed value
        """
        try:
            # Try to use ast.literal_eval for safe parsing
            parsed = ast.literal_eval(value_str)
            return parsed
        except (SyntaxError, ValueError):
            # If literal_eval fails, return the string as is
            return value_str.strip()
    
    @staticmethod
    def parse_output_string(output_str):
        """
        Parse an output string into Python objects
        
        Args:
            output_str (str): The output string to parse
            
        Returns:
            object: The parsed output value
        """
        return TestCaseGenerator.parse_single_value(output_str)
    
    @staticmethod
    def generate_test_cases_from_description(description):
        """
        Generate test cases from a problem description
        
        Args:
            description (str): The problem description
            
        Returns:
            list: List of test cases in the format [(inputs, expected_output), ...]
        """
        examples = TestCaseGenerator.extract_examples_from_description(description)
        test_cases = []
        
        for example in examples:
            try:
                inputs = TestCaseGenerator.parse_input_string(example['input'])
                expected = TestCaseGenerator.parse_output_string(example['output'])
                test_cases.append((inputs, expected))
            except Exception as e:
                print(f"Error generating test case: {e}")
        
        return test_cases
    
    @staticmethod
    def add_edge_cases(test_cases, problem_type):
        """
        Add common edge cases based on the problem type
        
        Args:
            test_cases (list): Existing test cases
            problem_type (str): Type of problem (e.g., 'array', 'string', 'tree')
            
        Returns:
            list: Enhanced test cases with edge cases
        """
        if problem_type == 'array':
            # Add empty array and single element array cases
            test_cases.append(([], None))  # Expected output needs to be determined by the user
            test_cases.append(([1], None)) # Expected output needs to be determined by the user
        elif problem_type == 'string':
            # Add empty string and single character cases
            test_cases.append(("", None))
            test_cases.append(("a", None))
        
        return test_cases

if __name__ == "__main__":
    # Example usage
    description = """
    <p><strong class="example">Example 1:</strong></p>
    <pre>
    <strong>Input:</strong> nums = [2,7,11,15], target = 9
    <strong>Output:</strong> [0,1]
    </pre>
    """
    
    test_cases = TestCaseGenerator.generate_test_cases_from_description(description)
    print(f"Generated test cases: {test_cases}")