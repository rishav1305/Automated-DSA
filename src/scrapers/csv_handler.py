import pandas as pd
import os
from datetime import datetime

class CSVHandler:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self):
        """Creates the CSV file if it doesn't exist"""
        if not os.path.exists(os.path.dirname(self.csv_path)):
            os.makedirs(os.path.dirname(self.csv_path))
            
        if not os.path.exists(self.csv_path):
            # Create an empty DataFrame with the required columns
            empty_df = pd.DataFrame(columns=[
                'id', 'title', 'url', 'difficulty', 
                'category', 'pattern', 'completed', 'date_completed'
            ])
            empty_df.to_csv(self.csv_path, index=False)
            print(f"Created new tracking file at {self.csv_path}")
    
    def read_questions(self):
        """Reads the questions from the CSV file"""
        try:
            return pd.read_csv(self.csv_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return pd.DataFrame()
    
    def save_questions(self, questions_df):
        """Saves the questions DataFrame to the CSV file"""
        try:
            questions_df.to_csv(self.csv_path, index=False)
            print(f"Successfully saved {len(questions_df)} questions to {self.csv_path}")
            return True
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False
    
    def update_question_status(self, question_id, completed=True):
        """Marks a question as completed"""
        df = self.read_questions()
        if question_id in df['id'].values:
            idx = df.index[df['id'] == question_id].tolist()[0]
            df.at[idx, 'completed'] = completed
            df.at[idx, 'date_completed'] = datetime.now().strftime('%Y-%m-%d') if completed else ''
            return self.save_questions(df)
        else:
            print(f"Question ID {question_id} not found")
            return False
    
    def get_next_question(self, category=None, difficulty=None):
        """
        Gets the next uncompleted question, optionally filtered by category and difficulty
        Returns a pandas Series with the question details or None if no questions match
        """
        df = self.read_questions()
        
        # Filter for uncompleted questions
        uncompleted = df[df['completed'] == False]
        
        # Apply additional filters if provided
        if category:
            uncompleted = uncompleted[uncompleted['category'] == category]
        if difficulty:
            uncompleted = uncompleted[uncompleted['difficulty'] == difficulty]
        
        if uncompleted.empty:
            return None
        
        # Return the first uncompleted question
        return uncompleted.iloc[0]