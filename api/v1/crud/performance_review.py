from sqlmodel import Session, select
from ..models import (
    PerformanceReviewCreate,
    PerformanceReview,
    PerformanceReviewUpdate,
    PerformanceReviewDatabase,
    EmployeeDatabase,
)
from fastapi import HTTPException, status
from datetime import datetime


def create_performance_review(
    performance_review: PerformanceReviewCreate, db: Session
) -> PerformanceReview:
    """Creates a performance_review"""
    performance_review = performance_review.model_dump()
    if performance_review.get("employee_id"):
        employee = db.exec(
            select(EmployeeDatabase).where(
                EmployeeDatabase.id == performance_review.get("employee_id")
            )
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found. Please enter a valid employee id.",
            )
    new_performance_review = PerformanceReviewDatabase(**performance_review)

    db.add(new_performance_review)
    db.commit()
    db.refresh(new_performance_review)

    return new_performance_review


def get_all_performance_reviews(db: Session):
    """Returns all performance_reviews"""
    statement = select(PerformanceReviewDatabase)
    return db.exec(statement).all()


def get_performance_review(id: int, db: Session):
    """Get a performance_review based on the performance_review id"""
    statement = select(PerformanceReviewDatabase).where(
        PerformanceReviewDatabase.id == id
    )
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="performance_review not Found",
        )
    return result


def update_performance_review(
    id: int, performance_review: PerformanceReviewUpdate, db: Session
):
    """Update the performance_review"""
    statement = select(PerformanceReviewDatabase).where(
        PerformanceReviewDatabase.id == id
    )
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="performance_review not found",
        )
    performance_review = performance_review.model_dump()
    if (
        performance_review.get("employee_id")
        or performance_review.get("employee_id") == 0
    ):
        employee = db.exec(
            select(EmployeeDatabase).where(
                EmployeeDatabase.id == performance_review.get("employee_id")
            )
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found. Please enter a valid employee id.",
            )
    for key, value in performance_review.items():
        setattr(result, key, value)
    result.date_updated = datetime.now()
    db.commit()
    db.refresh(result)
    return result


def delete_performance_review(id: int, db: Session):
    """Deletes a performance_review"""
    statement = select(PerformanceReviewDatabase).where(
        PerformanceReviewDatabase.id == id
    )
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="performance_review not found",
        )
    db.delete(result)
    db.commit()
    return {"message": "Deleted successfully"}
