from fastapi import APIRouter, Depends, HTTPException
from services.git import get_branches, commit_info, get_file_diff, create_and_push_branch
from models.response import SuccessResponse
from models.git import GitCommitRequest, GitCompareRequest, GitBranchCreateRequest
from config import REPO_PATH, repo
from utils.git import validate_branch_name, branch_exists_local, branch_exists_remote
from fastapi import BackgroundTasks

router = APIRouter()

@router.get("/git_branches", response_model=SuccessResponse)
async def get_all_branches():
    try:
        branches = get_branches(REPO_PATH)
        if not branches:
            raise HTTPException(status_code=404, detail="No branches found in the repository")
        
        return SuccessResponse(
            status="success",
            message="Branches retrieved successfully",
            data = {
                "branches": branches
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/git_branch_commit", response_model=SuccessResponse)
async def get_commit_info(branch_req: GitCommitRequest):
    try:
        validate_branch = validate_branch_name(branch_req.branch, REPO_PATH)
        commits = commit_info(validate_branch, REPO_PATH)
        
        if not commits:
            raise HTTPException(status_code=404, detail="No commits found for the specified branch")
        
        return SuccessResponse(
            status="success",
            message="Commit hash retrieved successfully",
            data={
                "commit_hash": commits
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")



@router.post("/git_branch_compare", response_model=SuccessResponse)
async def compare_branches(branch_req: GitCompareRequest):
    try:
        # Validate branches
        b1 = validate_branch_name(branch_req.branch1, REPO_PATH)
        b2 = validate_branch_name(branch_req.branch2, REPO_PATH)

        # Get changed files and their diffs (implement get_file_diff)
        changes = get_file_diff(b1, b2, REPO_PATH)
        if not changes:
            raise ValueError("No changes found between the specified branches")

        return SuccessResponse(
            status="success",
            message="Branches compared successfully",
            data={
                "changed_files_count": len(changes),
                "files": changes
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    

@router.post("/git_create_branch", response_model=SuccessResponse)
def create_branch(request: GitBranchCreateRequest, background_tasks: BackgroundTasks):
    try:
        new_branch = f"v_/{request.new_branch}"
        source_branch = validate_branch_name(request.source_branch, REPO_PATH)

        # Check if source branch exists locally or remotely
        if not branch_exists_local(repo, source_branch):
            if branch_exists_remote(repo, source_branch):
                repo.git.fetch("origin", source_branch)
            else:
                raise Exception(f"Source branch '{source_branch}' not found locally or remotely.")

        # Check if new branch already exists locally or remotely
        if branch_exists_local(repo, new_branch) or branch_exists_remote(repo, new_branch):
            raise Exception(f"Branch '{new_branch}' already exists locally or remotely.")
            
        # Create and push new branch
        try:
            new_branch, source_branch = create_and_push_branch(repo, new_branch, source_branch, background_tasks)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating branch: {str(e)}")

        return SuccessResponse (
            status="success",
            message="Branch created successfully",
            data={
                "new_branch": new_branch,
                "source_branch": source_branch
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")