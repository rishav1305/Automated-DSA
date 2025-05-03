# Automated DSA Questions Tracker

This project helps you track your progress through the NeetCode 150 DSA problems. It automatically fetches questions from NeetCode, tracks your solutions, validates them, and helps you maintain a Git repository of your solutions.

## Features

- Fetch the NeetCode 150 DSA questions and save to CSV
- Organize solutions by category and difficulty
- Track completion status of each question
- Generate solution template files with problem descriptions
- Validate and test solutions
- Automatically commit and push changes to Git

## Project Structure

```
Automated-DSA/
├── questions/               # Solutions organized by category/difficulty
├── questions.csv           # CSV with all questions & tracking info
├── src/                    # Source code
│   ├── main.py             # Main script to run the workflow
│   ├── scrapers/           # Scripts to fetch questions 
│   ├── templates/          # Solution templates
│   └── utils/              # Utility functions
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Fetch Questions from NeetCode

```bash
python -m main --fetch
```

### Get a New Question to Solve

```bash
python -m main --new
```

Optionally filter by category or difficulty:

```bash
python -m main --new --category "Arrays & Hashing" --difficulty Easy
```

### Test a Solution

```bash
python -m main --test path/to/solution.py
```

### Commit and Push Changes to Git

```bash
python -m main --commit
```

## Workflow

1. Run `--fetch` to get the initial list of questions
2. Run `--new` to get a new question to solve
3. Open the generated solution file and implement your solution
4. Run `--test` to validate your solution
5. Run `--commit` to save your solution to Git

## License

See the [LICENSE](LICENSE) file for details.
