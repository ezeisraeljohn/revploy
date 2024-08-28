from config.database import get_db
from ..crud.department import (
    create_department,
    get_all_departments,
    get_department,
    update_department,
    delete_department,
)

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from ..models import (
    DepartmentCreate,
    DepartmentReturnDetail,
    DepartmentReturnList,
    DepartmentUpdate,
    DepartmentDeletion,
)

router = APIRouter(tags=["Department"], prefix="/api/v1")


@router.post(
    "/departments",
    response_model=DepartmentReturnDetail,
    status_code=201,
)
def add_departments(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Creates a new user"""
    response_data = DepartmentReturnDetail(
        status=201,
        success=True,
        message="Department Created Successfully",
        data=create_department(department=department, db=db),
    )
    return response_data


@router.get("/departments", response_model=DepartmentReturnList)
def retrieve_departments(
    db: Session = Depends(get_db),
):
    """This gets all departments"""
    get_all_departments(db=db)
    response_data = DepartmentReturnList(
        status=200,
        success=True,
        message="Departments retrieved successfully",
        data=get_all_departments(db=db),
    )
    return response_data


@router.get("/departments/{id}", response_model=DepartmentReturnDetail)
def retrieve_department(id: int, db: Session = Depends(get_db)):
    """Retrieves an department based on its id"""
    response_data = DepartmentReturnDetail(
        status=200,
        success=True,
        message="Department Retrieved Successfully",
        data=get_department(id=id, db=db),
    )
    return response_data


@router.put("/departments/{id}", response_model=DepartmentReturnDetail)
def edit_department(
    id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
):
    """Updates an department"""
    response_data = DepartmentReturnDetail(
        status=200,
        success=True,
        message="department Updated Successfully",
        data=update_department(id=id, department=department, db=db),
    )
    return response_data


@router.delete("/departments/{id}", response_model=DepartmentDeletion)
def remove_department(id: int, db: Session = Depends(get_db)):
    """Deletes an department"""
    delete_department(id=id, db=db)
    response_data = DepartmentDeletion(
        status=200, success=True, message="department Deleted Successfully"
    )
    return response_data
