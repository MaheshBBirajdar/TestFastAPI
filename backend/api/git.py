from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services.git import get_branches, commit_info, get_file_diff
from models.response import SuccessResponse
from models.git import GitCommitRequest, GitCompareRequest
from config import REPO_PATH, repo
from utils.git import validate_branch_name

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


@router.post("/git_commit", response_model=SuccessResponse)
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



@router.post("/git_compare", response_model=SuccessResponse)
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
    
