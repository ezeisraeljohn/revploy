from sqlmodel import Session, select
from ..models import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeDatabase,
)
from fastapi import HTTPException, status


def create_employee(employee: EmployeeCreate, db: Session):
    """Creates an employee"""
    employee = employee.model_dump()
    new_employee = EmployeeDatabase(**employee)

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def get_all_employees(db: Session):
    """Returns all employees"""
    statement = select(EmployeeDatabase)
    return db.exec(statement).all()


def get_employee(id: int, db: Session):
    """Get an employee based on the employee id"""
    statement = select(EmployeeDatabase).where(EmployeeDatabase.id == id)
    result = db.scalars(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not Found"
        )
    return result


def update_employee(id: int, employee: EmployeeUpdate, db: Session):
    """Update the employee"""
    statement = select(EmployeeDatabase).where(EmployeeDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found"
        )
    employee = employee.model_dump()
    for key, value in employee.items():
        setattr(result, key, value)
    db.commit()

    return employee


def delete_employee(id: int, db: Session):
    """Deletes an employee"""
    statement = select(EmployeeDatabase).where(EmployeeDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )
    db.delete(result)
    db.commit()
