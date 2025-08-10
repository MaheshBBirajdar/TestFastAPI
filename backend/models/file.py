from pydantic import BaseModel

class FileEditRequest(BaseModel):
    branch: str
    file_path: str
    content: dict = {}

class FileContentRequest(BaseModel):
    branch: str
    file_path: str

class FileCreateRequest(BaseModel):
    branch: str
    folder: str
    file_name: str

