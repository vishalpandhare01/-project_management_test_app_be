from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=project.created_by,
        created_at=datetime.utcnow(),
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def create_issue(db: Session, issue: schemas.IssueCreate):
    db_issue = models.Issue(
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        project_id=issue.project_id,
        assigned_to=issue.assigned_to,
        created_at=datetime.utcnow(),
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_project_issues(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Issue)
        .filter(models.Issue.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def update_issue_status(db: Session, issue_id: int, status: schemas.IssueStatus):
    issue = get_issue(db, issue_id)
    if issue is None:
        return None
    issue.status = status
    db.commit()
    db.refresh(issue)
    return issue


def assign_issue(db: Session, issue_id: int, assigned_to: int):
    issue = get_issue(db, issue_id)
    if issue is None:
        return None
    issue.assigned_to = assigned_to
    db.commit()
    db.refresh(issue)
    return issue


def create_comment(db: Session, issue_id: int, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        issue_id=issue_id,
        user_id=comment.user_id,
        message=comment.message,
        created_at=datetime.utcnow(),
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_issue_comments(db: Session, issue_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Comment)
        .filter(models.Comment.issue_id == issue_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
