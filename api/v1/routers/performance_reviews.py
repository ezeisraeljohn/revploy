from config.database import get_db
from ..crud.performance_review import (
    create_performance_review,
    get_all_performance_reviews,
    get_performance_review,
    update_performance_review,
    delete_performance_review,
)

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from ..models import (
    PerformanceReviewCreate,
    PerformanceReviewReturnDetail,
    PerformanceReviewReturnList,
    PerformanceReviewUpdate,
    PerformanceReviewDeletion,
)

router = APIRouter(tags=["Performance Review"], prefix="/api/v1")


@router.post(
    "/performance-reviews",
    response_model=PerformanceReviewReturnDetail,
    status_code=201,
)
def add_performance_reviews(
    performance_review: PerformanceReviewCreate, db: Session = Depends(get_db)
):
    """Creates a new user"""
    response_data = PerformanceReviewReturnDetail(
        status=201,
        success=True,
        message="Performance Review Created Successfully",
        data=create_performance_review(
            performance_review=performance_review,
            db=db,
        ),
    )
    return response_data


@router.get("/performance-reviews", response_model=PerformanceReviewReturnList)
def retrieve_performance_reviews(db: Session = Depends(get_db)):
    """This gets all Performance Reviews"""
    response_data = PerformanceReviewReturnList(
        status=200,
        success=True,
        message="Performance Reviews retrieved successfully",
        data=get_all_performance_reviews(db=db),
    )
    return response_data


@router.get(
    "/performance-reviews/{id}",
    response_model=PerformanceReviewReturnDetail,
)
def retrieve_performance_review(id: int, db: Session = Depends(get_db)):
    """Retrieves an performance_review based on its id"""
    response_data = PerformanceReviewReturnDetail(
        status=200,
        success=True,
        message="Performance Review Retrieved Successfully",
        data=get_performance_review(id=id, db=db),
    )
    return response_data


@router.put(
    "/performance-reviews/{id}",
    response_model=PerformanceReviewReturnDetail,
)
def edit_performance_review(
    id: int,
    performance_review: PerformanceReviewUpdate,
    db: Session = Depends(get_db),
):
    """Updates a Performance Review"""
    response_data = PerformanceReviewReturnDetail(
        status=200,
        success=True,
        message="Performance Review Updated Successfully",
        data=update_performance_review(
            id=id, performance_review=performance_review, db=db
        ),
    )
    return response_data


@router.delete(
    "/performance-reviews/{id}",
    response_model=PerformanceReviewDeletion,
)
def remove_performance_review(id: int, db: Session = Depends(get_db)):
    """Deletes a performance_review"""
    delete_performance_review(id=id, db=db)
    response_data = PerformanceReviewDeletion(
        status=200, success=True, message="Performance Review Deleted Successfully"
    )
    return response_data
