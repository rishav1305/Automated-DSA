import os
import subprocess
from datetime import datetime
import git  # Import GitPython

class GitHandler:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = None
    
    def _run_command(self, command):
        """Run a git command and return the output (fallback method)"""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                check=True,
                text=True,
                capture_output=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command {' '.join(command)}: {e}")
            print(f"Error output: {e.stderr}")
            return None
    
    def ensure_git_initialized(self):
        """Ensures the repository is initialized with git"""
        # Check if .git directory exists
        git_dir = os.path.join(self.repo_path, ".git")
        if not os.path.exists(git_dir):
            print(f"Initializing git repository in {self.repo_path}")
            self.repo = git.Repo.init(self.repo_path)
            return "Git repository initialized"
        else:
            try:
                self.repo = git.Repo(self.repo_path)
                return "Git repository already initialized"
            except git.InvalidGitRepositoryError:
                print(f"Invalid git repository at {self.repo_path}. Reinitializing...")
                self.repo = git.Repo.init(self.repo_path)
                return "Git repository reinitialized"
    
    def remote_exists(self, remote="origin"):
        """Check if the specified remote exists"""
        if self.repo is None:
            self.ensure_git_initialized()
            
        try:
            return remote in [r.name for r in self.repo.remotes]
        except Exception as e:
            print(f"Error checking remote: {e}")
            return False
    
    def add_files(self, files=None):
        """
        Adds files to git staging
        If files is None, adds all files
        """
        if self.repo is None:
            self.ensure_git_initialized()
            
        try:
            if files is None:
                self.repo.git.add(A=True)  # Add all files
            else:
                self.repo.git.add(files)
            return "Files added to staging"
        except Exception as e:
            print(f"Error adding files: {e}")
            # Fall back to subprocess if GitPython fails
            return self._run_command(["git", "add", "."] if files is None else ["git", "add"] + files)
    
    def commit_changes(self, message=None):
        """Commits staged changes with a message"""
        if self.repo is None:
            self.ensure_git_initialized()
            
        if message is None:
            # Default commit message
            message = f"Add solution for {datetime.now().strftime('%Y-%m-%d')}"
        
        try:
            self.repo.git.commit('-m', message)
            return f"Changes committed with message: {message}"
        except git.GitCommandError as e:
            if "nothing to commit" in str(e):
                print("No changes to commit")
                return "No changes to commit"
            else:
                print(f"Error committing changes: {e}")
                # Fall back to subprocess
                return self._run_command(["git", "commit", "-m", message])
    
    def push_changes(self, remote="origin", branch="main"):
        """Pushes committed changes to the remote repository if it exists"""
        if self.repo is None:
            self.ensure_git_initialized()
            
        if not self.remote_exists(remote):
            print(f"Remote '{remote}' doesn't exist. Skipping push.")
            print("To push changes later, set up a remote with:")
            print(f"  git remote add {remote} <repository-url>")
            return "Remote not configured, commit succeeded locally"
        
        try:
            self.repo.git.push(remote, branch)
            return f"Changes pushed to {remote}/{branch}"
        except git.GitCommandError as e:
            print(f"Error pushing changes: {e}")
            # Fall back to subprocess
            return self._run_command(["git", "push", remote, branch])
    
    def add_commit_push(self, files=None, message=None, remote="origin", branch="main"):
        """Combines add, commit, and push operations"""
        add_result = self.add_files(files)
        if "Error" in str(add_result):
            return add_result
            
        commit_result = self.commit_changes(message)
        if "No changes to commit" in str(commit_result):
            return commit_result
            
        if self.remote_exists(remote):
            return self.push_changes(remote, branch)
        else:
            print(f"Changes committed locally. Remote '{remote}' not configured.")
            return commit_result