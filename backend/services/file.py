import os
import json
from config import REPO_PATH
from fastapi import HTTPException
from git.exc import GitCommandError
from datetime import datetime
from utils.git import _push_changes
import logging

# Setup logger
logger = logging.getLogger("file")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def edit_and_save_content(repo, branch, file_path, new_content, background_tasks):
    """
    Save new content to a file in a specific branch without checking out the branch.
    The old content is replaced entirely.
    """
    repo_relative_path = file_path  # Keep as repo-relative
    abs_file_path = os.path.join(REPO_PATH, repo_relative_path)

    logger.info(f"Opening repository: {repo.working_tree_dir}")
    logger.info(f"Getting reference for branch: {branch}")

    branch_ref = repo.refs[branch]
    commit = branch_ref.commit
    logger.info(f"Current commit on '{branch}': {commit.hexsha}")

    # Step 1: Write content directly to repo file
    logger.info(f"Writing new content directly to: {abs_file_path}")
    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    with open(abs_file_path, "w", encoding="utf-8") as f:
        if isinstance(new_content, (dict, list)):
            f.write(json.dumps(new_content, indent=4))
        else:
            f.write(str(new_content))

    # Step 2: Reset index to branch tree
    logger.info("Resetting index to branch tree...")
    repo.index.reset(commit=commit, working_tree=False)

    # Step 3: Stage the file
    logger.info(f"Adding '{repo_relative_path}' to index...")
    repo.index.add([repo_relative_path])

    # Step 4: Commit changes
    logger.info("Committing changes...")
    commit_message = "Updated file content"
    new_commit = repo.index.commit(commit_message, parent_commits=[commit])
    logger.info(f"New commit created: {new_commit.hexsha}")

    # Step 5: Update branch reference
    logger.info(f"Updating branch '{branch}' to point to new commit...")
    branch_ref.set_commit(new_commit)

    # Step 6: Schedule push in background
    logger.info(f"Scheduling push to remote branch '{branch}' in background...")
    background_tasks.add_task(_push_changes, repo, branch)
    
    logger.info("SUCCESS: File updated and pushed successfully!")

    return new_content


def file_save(repo, valid_branch, file_path, background_tasks, json_schema, valid_folder):

    # Create empty schema: set 'category' to valid_folder, rest empty
    empty_schema = {
        key: (valid_folder if key == "category" else "")
        for key in json_schema
    }
    empty_schema["timestamp"] = datetime.now().isoformat()

    # Ensure the branch is checked out
    logger.info(f"Checking out branch: {valid_branch}")
    repo.git.checkout(valid_branch)
    
    # Create the file path if it doesn't exist
    logger.info(f"Ensuring directory exists for file: {REPO_PATH}/{file_path}")
    os.makedirs(os.path.dirname(f"{REPO_PATH}/{file_path}"), exist_ok=True)
    
    # Create the new file with an empty JSON object
    logger.info(f"Creating new file at: {REPO_PATH}/{file_path}")
    with open(f"{REPO_PATH}/{file_path}", 'w') as new_file:
        json.dump(empty_schema, new_file, indent=2)  # Initialize with empty JSON object
    
    # Stage the new file
    logger.info(f"Adding new file '{file_path}' to the repository...") 
    repo.git.add(file_path)
    
    # Commit the new file creation
    logger.info(f"Committing new file '{file_path}' in branch '{valid_branch}'...")
    repo.git.commit(m=f"Created new file {file_path}")

    logger.info(f"Scheduling push file to remote branch '{valid_branch}' in background...")
    background_tasks.add_task(_push_changes, repo, valid_branch)
    
    logger.info(f"SUCCESS: File '{file_path}' created and pushed successfully!")
    return file_path    


def check_file_existence(repo, branch: str, file_path: str, repo_path: str):
    """
    Checks whether a file exists locally, remotely, or both.
    - If file exists locally and remotely -> raise error
    - If file exists remotely but missing locally -> fetch & raise error
    - If file exists locally but not remotely -> raise error
    - Returns (file_in_local, file_in_remote) if no error
    """
    local_full_path = f"{repo_path}/{file_path}"

    # Ensure branch is up to date
    repo.git.fetch("origin", branch)

    # Check if file exists in remote branch
    try:
        remote_file_list = repo.git.ls_tree("-r", f"origin/{branch}", "--name-only").splitlines()
    except GitCommandError as e:
        raise HTTPException(status_code=400, detail=f"Error checking remote files: {e}")

    file_in_remote = file_path in remote_file_list
    file_in_local = os.path.exists(local_full_path)

    # Handle cases
    if file_in_local or file_in_remote:
        # Exists in both local & remote
        if file_in_local and file_in_remote:
            raise HTTPException(status_code=400, detail=f"File '{file_path}' already exists in branch '{branch}'")

        # Exists in remote but missing locally
        if not file_in_local and file_in_remote:
            repo.git.checkout(branch)
            repo.git.pull("origin", branch)
            raise HTTPException(status_code=400, detail=f"File '{file_path}' exists in remote but was missing locally. Fetched from remote.")

        # Exists locally but not in remote
        if file_in_local and not file_in_remote:
            raise HTTPException(status_code=400, detail=f"File '{file_path}' exists locally but not in remote. Please sync first.")

    return file_in_local, file_in_remote
