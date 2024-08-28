from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class DepartmentBase(SQLModel):
    """The Base of the Department"""

    name: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Engineering",
            }
        }


class DepartmentCreate(DepartmentBase):
    """Creates  a department"""

    pass


class DepartmentUpdate(DepartmentCreate):
    """updates the departments"""

    pass


class Department(DepartmentBase, table=False):
    """Department class"""

    id: int | None = Field(default=None, primary_key=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Engineering",
            }
        }


class DepartmentReturnList(BaseModel):
    """Return statement"""

    status: int
    success: bool
    message: str
    data: List["DepartmentDatabase"]

    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "success": True,
                "message": "Departments retrieved successfully",
                "data": [
                    {
                        "id": 1,
                        "name": "Engineering",
                    }
                ],
            }
        }


class DepartmentReturnDetail(BaseModel):
    """Return details"""

    status: int
    success: bool
    message: str
    data: "DepartmentDatabase"


class DepartmentDeletion(BaseModel):
    """Deletion Return Type"""

    status: int
    success: bool
    message: str


class DepartmentDatabase(Department, table=True):
    """Stores the data in the database"""

    __tablename__ = "departments"
    employees: list["EmployeeDatabase"] = Relationship(
        back_populates="department",
    )
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: datetime | None = Field(default=None, nullable=True)


class EmployeeBase(SQLModel):
    """Base Class"""

    name: str = Field(default=None)
    phone: str | None = Field(default=None)
    address: str | None = Field(default=None)
    email: str | None = Field(default=None)
    hire_date: datetime | None = Field(default_factory=datetime.today)
    department_id: int | None = Field(
        default=None,
        foreign_key="departments.id",
    )
    position_id: int | None = Field(default=None, foreign_key="positions.id")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "1234567890",
                "address": "123 Main St",
                "email": "tiwi@gmail.com",
                "hire_date": "2021-08-01",
                "department_id": 1,
                "position_id": 1,
            }
        }


class EmployeeCreate(EmployeeBase):
    """Create an employee"""

    pass


class EmployeeUpdate(EmployeeCreate):
    """Update an employee"""

    is_active: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "1234567890",
                "address": "123 Main St",
                "email": "update@example.com",
                "hire_date": "2021-08-01",
                "department_id": 1,
                "position_id": 1,
                "is_active": False,
                "date_updated": "2021-08-01",
                "date_created": "2021-08-01",
            },
        }


class EmployeeDatabase(EmployeeBase, table=True):
    """The Employee class"""

    __tablename__ = "employees"
    id: int = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    position: Optional["PositionDatabase"] = Relationship(
        back_populates="employees",
    )
    department: DepartmentDatabase | None = Relationship(
        back_populates="employees",
    )
    performance_reviews: list["PerformanceReviewDatabase"] = Relationship(
        back_populates="employee"
    )
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: datetime | None = Field(default=None, nullable=True)

    class Config:
        from_attributes = True


class EmployeePaginationLinks(BaseModel):
    """Pagination links"""

    first: str
    last: str
    self: str
    next: str
    prev: str


class EmployeePagination(BaseModel):
    """Pagination"""

    page_num: int
    num_of_employees: int
    total_pages: int
    total_employees: int


class EmployeeReturnList(BaseModel):
    """Return statement"""

    status: int
    success: bool
    message: str
    data: List[EmployeeDatabase]


class EmployeeDeletion(BaseModel):
    """Deletion Return Type"""

    status: int
    success: bool
    message: str


class EmployeeReturnDetail(BaseModel):
    """Return details"""

    status: int
    success: bool
    message: str
    data: EmployeeDatabase


class PerformanceReviewBase(SQLModel):
    """Performance review base"""

    review_date: datetime = Field(default_factory=datetime.now)
    coments: Optional[str] = Field(nullable=True)
    rating: int = Field(default=0)
    employee_id: int = Field(foreign_key="employees.id", nullable=False)


class PerformanceReviewCreate(PerformanceReviewBase):
    """Create a performance review"""

    pass


class PerformanceReviewUpdate(PerformanceReviewCreate):
    """Update a performance review"""

    pass


class PerformanceReview(PerformanceReviewBase):
    """The PerformanceReview Class"""

    id: int = Field(default=None, primary_key=True)


class PerformanceReviewReturnList(BaseModel):
    """Return statement"""

    status: int
    success: bool
    message: str
    data: List["PerformanceReviewDatabase"]


class PerformanceReviewReturnDetail(BaseModel):
    """Return details"""

    status: int
    success: bool
    message: str
    data: "PerformanceReviewDatabase"


class PerformanceReviewDeletion(BaseModel):
    """Deletion Return Type"""

    status: int
    success: bool
    message: str


class PerformanceReviewDatabase(PerformanceReview, table=True):
    """Store the performance review"""

    __tablename__ = "performance_reviews"
    employee: EmployeeDatabase | None = Relationship(
        back_populates="performance_reviews",
    )
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: Optional[datetime] = Field(default=None, nullable=True)


class PositionBase(SQLModel):
    """Position Base"""

    name: str = Field(nullable=False)


class PositionCreate(PositionBase):
    """Creates a position"""

    pass


class PositionUpdate(PositionBase):
    """Updates a position"""

    pass


class PositionReturnList(BaseModel):
    """Return statement"""

    status: int
    success: bool
    message: str
    data: List["PositionDatabase"]


class PositionReturnDetail(BaseModel):
    """Return details"""

    status: int
    success: bool
    message: str
    data: "PositionDatabase"


class PositionDeletion(BaseModel):
    """Deletion Return Type"""

    status: int
    success: bool
    message: str


class Position(PositionBase):
    """The position class"""

    id: int = Field(default=None, primary_key=True)


class PositionDatabase(Position, table=True):
    """Stores the position in the database"""

    __tablename__ = "positions"
    date_created: datetime = Field(default_factory=datetime.now)
    date_updated: Optional[datetime] = Field(default=None, nullable=True)
    employees: list[EmployeeDatabase] = Relationship(back_populates="position")
