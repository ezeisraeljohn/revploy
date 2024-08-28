from sqlmodel import Session, select
from ..models import (
    PerformanceReviewCreate,
    PerformanceReview,
    PerformanceReviewUpdate,
    PerformanceReviewDatabase,
)
from fastapi import HTTPException, status


def create_performance_review(
    performance_review: PerformanceReviewCreate, db: Session
) -> PerformanceReview:
    """Creates a performance_review"""
    performance_review = performance_review.model_dump()
    new_performance_review = PerformanceReviewDatabase(**performance_review)

    db.add(new_performance_review)
    db.commit()
    db.refresh(new_performance_review)

    return new_performance_review


def get_all_performance_reviews(db: Session, limit: int, offset: int):
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
            details="performance_review not Found",
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
    for key, value in performance_review.items():
        setattr(result, key, value)
    db.commit()

    return performance_review


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
