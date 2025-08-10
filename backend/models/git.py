from pydantic import BaseModel
from typing import List

class GitCommitRequest(BaseModel):
    branch: str

class GitCompareRequest(BaseModel):
    branch1: str
    branch2: str