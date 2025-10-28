from sqlalchemy.orm import Session
from app import models, schemas

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session):
    return db.query(models.Project).all()
