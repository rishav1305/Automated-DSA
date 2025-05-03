import os
import subprocess
from datetime import datetime

class GitHandler:
    def __init__(self, repo_path):
        self.repo_path = repo_path
    
    def _run_command(self, command):
        """Run a git command and return the output"""
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
            return self._run_command(["git", "init"])
        return "Git repository already initialized"
    
    def remote_exists(self, remote="origin"):
        """Check if the specified remote exists"""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", remote],
                cwd=self.repo_path,
                text=True,
                capture_output=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def add_files(self, files=None):
        """
        Adds files to git staging
        If files is None, adds all files
        """
        if files is None:
            return self._run_command(["git", "add", "."])
        else:
            return self._run_command(["git", "add"] + files)
    
    def commit_changes(self, message=None):
        """Commits staged changes with a message"""
        if message is None:
            # Default commit message
            message = f"Add solution for {datetime.now().strftime('%Y-%m-%d')}"
        
        return self._run_command(["git", "commit", "-m", message])
    
    def push_changes(self, remote="origin", branch="main"):
        """Pushes committed changes to the remote repository if it exists"""
        if not self.remote_exists(remote):
            print(f"Remote '{remote}' doesn't exist. Skipping push.")
            print("To push changes later, set up a remote with:")
            print(f"  git remote add {remote} <repository-url>")
            return "Remote not configured, commit succeeded locally"
        
        return self._run_command(["git", "push", remote, branch])
    
    def add_commit_push(self, files=None, message=None, remote="origin", branch="main"):
        """Combines add, commit, and push operations"""
        self.add_files(files)
        commit_result = self.commit_changes(message)
        if commit_result:
            if self.remote_exists(remote):
                return self.push_changes(remote, branch)
            else:
                print(f"Changes committed locally. Remote '{remote}' not configured.")
                return commit_result
        return None