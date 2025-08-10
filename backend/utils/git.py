import re
import subprocess
import os

def validate_branch_name(branch: str, repo_path: str) -> str:
    """
    Validate branch name format (X.Y or X.Y.Z) and check if v/branch or v_/branch exists.
    """
    if not re.fullmatch(r'\d+\.\d+(\.\d+)?', branch):
        raise ValueError("Branch format must be X.Y or X.Y.Z (e.g., 1.2 or 1.2.3)")

    possible_branches = [f"v/{branch}", f"v_/{branch}"]

    try:
        result = subprocess.run(
            ["git", "branch", "--list", "--all"],
            cwd=repo_path,
            text=True,
            check=True,
            capture_output=True
        )
        existing_branches = [
            b.strip().lstrip("* ").replace("remotes/origin/", "") 
            for b in result.stdout.strip().split('\n') if b.strip()
        ]

        for b in possible_branches:
            if b in existing_branches:
                return b

        raise ValueError(f"No matching branch found (checked: {possible_branches})")
    
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error retrieving branches: {e.stderr.strip()}") from e
