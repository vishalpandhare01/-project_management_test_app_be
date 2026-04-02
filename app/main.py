from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + SQLAlchemy + SQLite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# user 
@app.post("/users/", response_model=schemas.User)
@app.post("/api/v1/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
@app.get("/api/v1/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
@app.get("/api/v1/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
@app.put("/api/v1/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User)
@app.delete("/api/v1/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/projects/", response_model=schemas.Project)
@app.post("/api/v1/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Optionally verify creator exists
    creator = crud.get_user(db, project.created_by)
    if creator is None:
        raise HTTPException(status_code=400, detail="creator user_id not found")
    return crud.create_project(db=db, project=project)


@app.get("/projects/", response_model=list[schemas.Project])
@app.get("/api/v1/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)


@app.get("/projects/{project_id}", response_model=schemas.Project)
@app.get("/api/v1/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/issues/", response_model=schemas.Issue)
@app.post("/api/v1/issues/", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    # Validate project exists
    project = crud.get_project(db, issue.project_id)
    if project is None:
        raise HTTPException(status_code=400, detail="project_id not found")

    # Optional: validate assigned user (if provided)
    if issue.assigned_to is not None and crud.get_user(db, issue.assigned_to) is None:
        raise HTTPException(status_code=400, detail="assigned_to user_id not found")

    return crud.create_issue(db=db, issue=issue)


@app.get("/projects/{project_id}/issues", response_model=list[schemas.Issue])
@app.get("/api/v1/projects/{project_id}/issues", response_model=list[schemas.Issue])
def read_project_issues(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Ensure project exists
    if crud.get_project(db, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_project_issues(db=db, project_id=project_id, skip=skip, limit=limit)


@app.put("/issues/{issue_id}/status", response_model=schemas.Issue)
@app.put("/api/v1/issues/{issue_id}/status", response_model=schemas.Issue)
def update_issue_status(issue_id: int, status_payload: schemas.IssueStatusUpdate, db: Session = Depends(get_db)):
    issue = crud.update_issue_status(db=db, issue_id=issue_id, status=status_payload.status)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@app.put("/issues/{issue_id}/assign", response_model=schemas.Issue)
@app.put("/api/v1/issues/{issue_id}/assign", response_model=schemas.Issue)
def assign_issue(issue_id: int, assign_payload: schemas.IssueAssign, db: Session = Depends(get_db)):
    if crud.get_user(db, assign_payload.assigned_to) is None:
        raise HTTPException(status_code=400, detail="assigned_to user_id not found")
    issue = crud.assign_issue(db=db, issue_id=issue_id, assigned_to=assign_payload.assigned_to)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@app.get("/issues/{issue_id}", response_model=schemas.Issue)
@app.get("/api/v1/issues/{issue_id}", response_model=schemas.Issue)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = crud.get_issue(db=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@app.post("/issues/{issue_id}/comments", response_model=schemas.Comment)
@app.post("/api/v1/issues/{issue_id}/comments", response_model=schemas.Comment)
def add_issue_comment(issue_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    issue = crud.get_issue(db=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    if crud.get_user(db, comment.user_id) is None:
        raise HTTPException(status_code=400, detail="user_id not found")
    return crud.create_comment(db=db, issue_id=issue_id, comment=comment)


@app.get("/issues/{issue_id}/comments", response_model=list[schemas.Comment])
@app.get("/api/v1/issues/{issue_id}/comments", response_model=list[schemas.Comment])
def get_issue_comments(issue_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if crud.get_issue(db=db, issue_id=issue_id) is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return crud.get_issue_comments(db=db, issue_id=issue_id, skip=skip, limit=limit)

