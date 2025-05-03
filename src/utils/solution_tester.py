import os
import importlib.util
import sys
import traceback

class SolutionTester:
    def __init__(self, solution_file_path):
        self.solution_file_path = solution_file_path
        self.solution_module = None
        self.solution_instance = None
        self._load_solution()
        
    def _load_solution(self):
        """Dynamically load the solution module"""
        try:
            # Get the module name from the file path
            module_name = os.path.basename(self.solution_file_path).replace(".py", "")
            
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(module_name, self.solution_file_path)
            solution_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = solution_module
            spec.loader.exec_module(solution_module)
            
            self.solution_module = solution_module
            
            # Create an instance of the Solution class
            if hasattr(solution_module, "Solution"):
                self.solution_instance = solution_module.Solution()
            else:
                raise AttributeError("Solution class not found in the module")
                
        except Exception as e:
            print(f"Error loading solution: {e}")
            traceback.print_exc()
    
    def run_tests(self):
        """Run the tests from the solution module"""
        if not self.solution_instance:
            print("No solution instance available")
            return False
            
        if not hasattr(self.solution_instance, "get_test_cases"):
            print("Solution instance does not have get_test_cases method")
            return False
            
        test_cases = self.solution_instance.get_test_cases()
        if not test_cases:
            print("No test cases provided")
            return False
            
        # Get the solution function
        # Try to automatically detect the solution function
        solution_functions = [attr for attr in dir(self.solution_instance) 
                             if callable(getattr(self.solution_instance, attr)) and 
                             not attr.startswith('_') and 
                             attr != 'get_test_cases']
        
        if not solution_functions:
            print("No solution function found")
            return False
            
        solution_function_name = solution_functions[0]
        solution_function = getattr(self.solution_instance, solution_function_name)
        
        # Run the tests
        passed = 0
        failed = 0
        
        print(f"\nRunning tests for {os.path.basename(self.solution_file_path)}...")
        for i, (inputs, expected) in enumerate(test_cases):
            try:
                # Handle different types of inputs (single value or list of values)
                if isinstance(inputs, tuple):
                    actual = solution_function(*inputs)
                elif isinstance(inputs, list) and all(isinstance(x, dict) for x in inputs):
                    # Special case for LeetCode-style list of objects
                    actual = solution_function(inputs)
                else:
                    actual = solution_function(inputs)
                
                if actual == expected:
                    print(f"Test {i+1}: ✓")
                    passed += 1
                else:
                    print(f"Test {i+1}: ✗")
                    print(f"  Input: {inputs}")
                    print(f"  Expected: {expected}")
                    print(f"  Actual: {actual}")
                    failed += 1
            except Exception as e:
                print(f"Test {i+1}: Error - {e}")
                traceback.print_exc()
                failed += 1
                
        print(f"\nTest Results: {passed} passed, {failed} failed")
        return failed == 0