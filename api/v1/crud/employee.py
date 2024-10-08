from sqlmodel import Session, select
from ..models import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeDatabase,
    DepartmentDatabase,
    PositionDatabase,
)
from fastapi import HTTPException, status
from datetime import datetime


def create_employee(employee: EmployeeCreate, db: Session):
    """Creates an employee"""
    employee_dict = employee.model_dump()
    if employee_dict.get("department_id"):
        department = db.exec(
            select(DepartmentDatabase).where(
                DepartmentDatabase.id == employee_dict.get("department_id")
            )
        ).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found. Please enter a valid department id.",
            )

    # Check if position_id is provided
    if employee_dict.get("position_id"):
        position = db.exec(
            select(PositionDatabase).where(
                PositionDatabase.id == employee_dict.get("position_id")
            )
        ).first()
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found. Please enter a valid position id.",
            )

    new_employee = EmployeeDatabase(**employee_dict)

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the employee: {str(e)}",
        )

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
    employee_dict = employee.model_dump()
    if employee_dict.get("department_id") or employee_dict.get("department_id") == 0:
        department = db.exec(
            select(DepartmentDatabase).where(
                DepartmentDatabase.id == employee_dict.get("department_id")
            )
        ).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found. Please enter a valid department id.",
            )
    if employee_dict.get("position_id") or employee_dict.get("position_id") == 0:
        position = db.exec(
            select(PositionDatabase).where(
                PositionDatabase.id == employee_dict.get("position_id")
            )
        ).first()
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found. Please enter a valid position id.",
            )
    for key, value in employee_dict.items():
        setattr(result, key, value)
    result.date_updated = datetime.now()
    db.commit()
    db.refresh(result)

    return result


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
