from sqlmodel import Session, select
from ..models import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentDatabase,
)
from fastapi import HTTPException, status


def create_department(department: DepartmentCreate, db: Session):
    """Creates a department"""
    department = department.model_dump()
    new_department = DepartmentDatabase(**department)

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


def get_all_departments(db: Session):
    """Returns all departments"""
    statement = select(DepartmentDatabase)
    return db.exec(statement).all()


def get_department(id: int, db: Session):
    """Get a department based on the department id"""
    statement = select(DepartmentDatabase).where(DepartmentDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not Found"
        )
    return result


def update_department(id: int, department: DepartmentUpdate, db: Session):
    """Update the department"""
    statement = select(DepartmentDatabase).where(DepartmentDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    department = department.model_dump()
    for key, value in department.items():
        setattr(result, key, value)
    db.commit()

    return department


def delete_department(id: int, db: Session):
    """Deletes a department"""
    statement = select(DepartmentDatabase).where(DepartmentDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    db.delete(result)
    db.commit()
    return {"message": "Deleted successfully"}
