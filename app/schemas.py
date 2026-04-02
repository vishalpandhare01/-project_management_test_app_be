from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr


class IssueStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class IssuePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    created_by: int


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class IssueBase(BaseModel):
    title: str
    description: str | None = None
    project_id: int
    assigned_to: int | None = None
    status: IssueStatus = IssueStatus.OPEN
    priority: IssuePriority = IssuePriority.MEDIUM


class IssueCreate(IssueBase):
    pass


class IssueStatusUpdate(BaseModel):
    status: IssueStatus


class IssueAssign(BaseModel):
    assigned_to: int


class Issue(IssueBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    message: str


class CommentCreate(CommentBase):
    user_id: int


class Comment(CommentBase):
    id: int
    issue_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
