from config.database import engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from api.v1.routers import (
    employee_router,
    department_router,
    position_router,
    performance_review_router,
)


app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    title="Revploy API",
)

SQLModel.metadata.create_all(bind=engine)

app.include_router(employee_router)
app.include_router(department_router)
app.include_router(position_router)
app.include_router(performance_review_router)


@app.exception_handler(500)
def internal_error(request: Request, exc: str) -> JSONResponse:
    return (
        JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "success": False,
                "message": f"An Error Occured: {exc}",
            },
        ),
    )


@app.exception_handler(404)
def not_found(request, exc: str):
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "success": False,
            "message": f"Resource Not Found: {exc}",
        },
    )


@app.exception_handler(400)
def bad_request(request, exc: str):
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "success": False,
            "message": f"Bad Request: {exc}",
        },
    )


@app.exception_handler(422)
def unprocessable_entity(request, exc: str):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "success": False,
            "message": f"Unprocessable Entity: {exc}",
        },
    )
