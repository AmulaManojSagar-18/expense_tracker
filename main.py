from fastapi import FastAPI

from database.connection import engine, Base
from database import models

from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.expense_routes import router as expense_router


app = FastAPI(
    title="Expense Tracker API"
)


@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)

app.include_router(user_router)

app.include_router(expense_router)