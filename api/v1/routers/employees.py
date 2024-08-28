from config.database import get_db
from ..crud.employee import (
    create_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee,
)

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from ..models import (
    EmployeeCreate,
    EmployeeReturnDetail,
    EmployeeReturnList,
    EmployeeUpdate,
    EmployeeDeletion,
)

router = APIRouter(tags=["Employee"], prefix="/api/v1")


@router.post(
    "/employees",
    response_model=EmployeeReturnDetail,
    status_code=201,
)
def add_employees(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Creates a new user"""
    response_data = EmployeeReturnDetail(
        status=201,
        success=True,
        message="Employee Created Successfully",
        data=create_employee(employee=employee, db=db),
    )
    return response_data


@router.get("/employees", response_model=EmployeeReturnList)
def retrieve_employees(
    db: Session = Depends(get_db),
):
    """This gets all employees"""
    get_all_employees(
        db=db,
    )
    response_data = EmployeeReturnList(
        status=200,
        success=True,
        message="Employees retrieved successfully",
        data=get_all_employees(
            db=db,
        ),
    )
    return response_data


@router.get("/employees/{id}", response_model=EmployeeReturnDetail)
def retrieve_employee(id: int, db: Session = Depends(get_db)):
    """Retrieves an employee based on its id"""
    response_data = EmployeeReturnDetail(
        status=200,
        success=True,
        message="Employee Retrieved Successfully",
        data=get_employee(id=id, db=db),
    )
    return response_data


@router.put("/employees/{id}", response_model=EmployeeReturnDetail)
def edit_employee(
    id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    """Updates an Employee"""
    response_data = EmployeeReturnDetail(
        status=200,
        success=True,
        message="Employee Updated Successfully",
        data=update_employee(id=id, employee=employee, db=db),
    )
    return response_data


@router.delete("/employees/{id}", response_model=EmployeeDeletion)
def remove_employee(id: int, db: Session = Depends(get_db)):
    """Deletes an employee"""
    delete_employee(id=id, db=db)
    response_data = EmployeeDeletion(
        status=200, success=True, message="Employee Deleted Successfully"
    )
    return response_data
