import os
import subprocess
import difflib
import git
import logging
from utils.git import _push_changes


# Setup logger
logger = logging.getLogger("git")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_branches(repo_path):
    """
    Retrieve a list of all git branches in the repository.
    """
    logger.info(f"Getting branches for repo: {repo_path}")
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        logger.error(f"Repository path does not exist: {repo_path}")
        raise Exception(f"Repository path does not exist: {repo_path}")

    git_dir = os.path.join(repo_path, ".git")
    if not os.path.exists(git_dir) or not os.path.isdir(git_dir):
        logger.error(f"Not a valid Git repository: {repo_path}")
        raise Exception(f"Not a valid Git repository: {repo_path}")

    try:
        result = subprocess.run(
            ["git", "branch", "--list"],
            cwd=repo_path,
            check=True,
            text=True,
            capture_output=True
        )
        branches = result.stdout.strip().split('\n')
        branch_list = [branch.strip().lstrip("* ").strip() for branch in branches if branch]
        logger.info(f"Branches found: {branch_list}")
        return branch_list
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving branches: {e.stderr.strip()}")
        raise Exception(f"Error retrieving branches: {e.stderr.strip()}") from e


def commit_info(branch: str, repo_path: str) -> list[dict]:
    """
    Get full commit history for the specified branch.
    """
    logger.info(f"Getting commit info for branch: {branch} in repo: {repo_path}")
    try:
        result = subprocess.run(
            ["git", "log", branch, "--pretty=format:%H|%an|%ad|%s", "--date=iso"],
            cwd=repo_path,
            text=True,
            check=True,
            capture_output=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split("|", 3)
            if len(parts) == 4:
                commit_hash, author, date, message = parts
                commits.append({
                    "hash": commit_hash,
                    "author": author,
                    "date": date,
                    "message": message
                })
        logger.info(f"Found {len(commits)} commits for branch {branch}")
        return commits

    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving commit history: {e.stderr.strip()}")
        raise Exception(f"Error retrieving commit history: {e.stderr.strip()}") from e


def get_file_diff(branch1, branch2, repo_path):
    logger.info(f"Comparing branches: {branch1} vs {branch2} in repo: {repo_path}")
    repo = git.Repo(repo_path)
    diff_index = repo.git.diff('--name-only', f'{branch1}..{branch2}').splitlines()
    logger.info(f"Changed files: {diff_index}")
    changes = []
    for file_path in diff_index:
        logger.info(f"Diff for file: {file_path}")
        old_blob = repo.git.show(f'{branch1}:{file_path}')
        new_blob = repo.git.show(f'{branch2}:{file_path}')
        old_lines = old_blob.splitlines()
        new_lines = new_blob.splitlines()
        diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=''))
        added = [i+1 for i, line in enumerate(diff) if line.startswith('+') and not line.startswith('+++')]
        removed = [i+1 for i, line in enumerate(diff) if line.startswith('-') and not line.startswith('---')]
        changes.append({
            "file_path": file_path,
            "old_text": old_blob,
            "new_text": new_blob,
            "added_lines": added,
            "removed_lines": removed
        })
    logger.info(f"Total changed files: {len(changes)}")
    return changes


def create_and_push_branch(repo, new_branch, source_branch, background_tasks):
    logger.info(f"Creating new branch '{new_branch}' from source branch '{source_branch}'")
    
    logger.info(f"Checking out source branch: {source_branch}")
    repo.git.checkout(source_branch)
    
    logger.info(f"Creating new branch: {new_branch}")
    new_branch_ref = repo.create_head(new_branch)
    
    logger.info(f"Checking out new branch: {new_branch}")
    new_branch_ref.checkout()
    
    # Schedule git push in the background
    background_tasks.add_task(_push_changes, repo, new_branch)
    
    logger.info(f"Branch '{new_branch}' created locally; push scheduled in background.")

    return new_branch, source_branch
