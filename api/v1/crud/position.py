from sqlmodel import Session, select
from ..models import (
    PositionCreate,
    Position,
    PositionUpdate,
    PositionDatabase,
)
from fastapi import HTTPException, status
from datetime import datetime


def create_position(position: PositionCreate, db: Session):
    """Creates a position"""
    position = position.model_dump()
    new_position = PositionDatabase(**position)

    db.add(new_position)
    db.commit()
    db.refresh(new_position)

    return new_position


def get_all_positions(db: Session, limit: int, offset: int):
    """Returns all positions"""
    statement = select(PositionDatabase)
    return db.exec(statement).all()


def get_position(id: int, db: Session):
    """Get a position based on the position id"""
    statement = select(PositionDatabase).where(PositionDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="position not Found"
        )
    return result


def update_position(id: int, position: PositionUpdate, db: Session):
    """Update the position"""
    statement = select(PositionDatabase).where(PositionDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="position not found"
        )
    position = position.model_dump()
    for key, value in position.items():
        setattr(result, key, value)
    result.date_updated = datetime.now()
    db.commit()

    return position


def delete_position(id: int, db: Session):
    """Deletes a position"""
    statement = select(PositionDatabase).where(PositionDatabase.id == id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="position not found"
        )
    db.delete(result)
    db.commit()
    return {"message": "Deleted successfully"}
