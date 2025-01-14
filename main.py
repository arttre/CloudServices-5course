from fastapi import FastAPI
from app.routers import expenses, reports, auth

app = FastAPI(title="Budget Management API")

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Budget Management API"}


@app.on_event("startup")
async def on_startup():
    from app.config import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
