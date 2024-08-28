from config.database import get_db
from ..crud.position import (
    create_position,
    get_all_positions,
    get_position,
    update_position,
    delete_position,
)

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from ..models import (
    PositionCreate,
    PositionReturnDetail,
    PositionReturnList,
    PositionUpdate,
    PositionDeletion,
)

router = APIRouter(tags=["Position"], prefix="/api/v1")


@router.post(
    "/positions",
    response_model=PositionReturnDetail,
    status_code=201,
)
def add_positions(position: PositionCreate, db: Session = Depends(get_db)):
    """Creates a new user"""
    response_data = PositionReturnDetail(
        status=201,
        success=True,
        message="Position Created Successfully",
        data=create_position(position=position, db=db),
    )
    return response_data


@router.get("/positions", response_model=PositionReturnList)
def retrieve_positions(
    db: Session = Depends(get_db),
    limit: int = 0,
    offset: int = 50,
):
    """This gets all positions"""
    get_all_positions(db=db)
    response_data = PositionReturnList(
        status=200,
        success=True,
        message="positions retrieved successfully",
        data=get_all_positions(db=db, limit=limit, offset=offset),
    )
    return response_data


@router.get("/positions/{id}", response_model=PositionReturnDetail)
def retrieve_position(id: int, db: Session = Depends(get_db)):
    """Retrieves an position based on its id"""
    response_data = PositionReturnDetail(
        status=200,
        success=True,
        message="Position Retrieved Successfully",
        data=get_position(id=id, db=db),
    )
    return response_data


@router.put("/positions/{id}", response_model=PositionReturnDetail)
def edit_position(
    id: int,
    position: PositionUpdate,
    db: Session = Depends(get_db),
):
    """Updates an position"""
    response_data = PositionReturnDetail(
        status=200,
        success=True,
        message="Position Updated Successfully",
        data=update_position(id=id, position=position, db=db),
    )
    return response_data


@router.delete("/positions/{id}", response_model=PositionDeletion)
def remove_position(id: int, db: Session = Depends(get_db)):
    """Deletes an position"""
    delete_position(id=id, db=db)
    response_data = PositionDeletion(
        status=200, success=True, message="Position Deleted Successfully"
    )
    return response_data
