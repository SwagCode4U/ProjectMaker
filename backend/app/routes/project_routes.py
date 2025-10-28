# app/project_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    return crud.create_project(db, project)

@router.get("/", response_model=list[schemas.ProjectResponse])
def list_projects(db: Session = Depends(database.get_db)):
    return crud.get_projects(db)
