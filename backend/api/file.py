from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.response import SuccessResponse
from models.file import FileEditRequest, FileContentRequest, FileCreateRequest
from config import REPO_PATH, repo, json_schema
from services.file import edit_and_save_content, file_save, check_file_existence
from utils.git import validate_branch_name
from utils.file import validate_file_path, validate_folder_path
from git import GitCommandError
import json
import os

router = APIRouter()

@router.post("/file_edit", response_model=SuccessResponse)
async def file_edit(edit_req: FileEditRequest, background_tasks: BackgroundTasks):
    """
    Saved new content of a file from a specific branch in the repository.
    """
    try:
        valid_branch = validate_branch_name(edit_req.branch, REPO_PATH)
        valid_file_path = validate_file_path(edit_req.file_path, REPO_PATH)

        try:
            new_content = edit_and_save_content(repo, valid_branch, valid_file_path, edit_req.content, background_tasks)
        except GitCommandError:
            raise HTTPException(status_code=404, detail="File not found in the specified branch")
        
        return SuccessResponse(
            status="success",
            message="New file content updated successfully",
            data={
                "branch": valid_branch,
                "file_path": valid_file_path,
                "content": new_content
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file_content", response_model=SuccessResponse)
async def get_file_content(content_req: FileContentRequest):
    """
    Get the content of a file from a specific branch in the repository.
    """
    try:
        valid_branch = validate_branch_name(content_req.branch, REPO_PATH)
        valid_file_path = validate_file_path(content_req.file_path, REPO_PATH)

        try:
            file_content = repo.git.show(f"{valid_branch}:{valid_file_path}")
            parsed_content = json.loads(file_content)
        except GitCommandError:
            raise HTTPException(status_code=404, detail="File not found in the specified branch")
        
        return SuccessResponse(
            status="success",
            message="File content retrieved successfully",
            data={
                "branch": valid_branch,
                "file_path": valid_file_path,
                "content": parsed_content
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/file_create", response_model=SuccessResponse)
async def file_create(create_req: FileCreateRequest, background_tasks: BackgroundTasks):
    """
    Create a new file in a specific folder of a branch in the repository.
    """
    try:
        valid_branch = validate_branch_name(create_req.branch, REPO_PATH)
        valid_folder = validate_folder_path(create_req.folder, REPO_PATH)
        file_path = f"{valid_folder}/{create_req.file_name}"

         # Check existence in local and remote
        check_file_existence(repo, valid_branch, file_path, REPO_PATH)

        try:
            # File truly doesn't exist in local or remote → create it
            file_path = file_save(repo, valid_branch, file_path, background_tasks, json_schema, valid_folder)
        except GitCommandError as e:
            print(f"[ERROR] GitCommandError: {e}")
            raise HTTPException(status_code=400, detail="Failed to create file")
        
        return SuccessResponse(
            status="success",
            message="File created successfully",
            data={
                "branch": valid_branch,
                "file_path": file_path
            }
        )
    except Exception as e:  
        raise HTTPException(status_code=400, detail=str(e))