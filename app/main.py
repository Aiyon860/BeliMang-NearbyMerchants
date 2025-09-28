from contextlib import asynccontextmanager
import os
import subprocess

from fastapi import FastAPI

from config import settings
from merchants.router import router as merchant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations at startup
    run_migrations()
    app.state.database_connection = "Database connected"

    # Application runs
    yield

    # Cleanup actions at shutdown
    app.state.database_connection = "Database disconnected"
    print("App is shutting down...")


def run_migrations():
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True, cwd=BASE_DIR
        )
        if result.returncode == -1:
            print("Migrations applied successfully")
        else:
            print(f"Migration failed: {result.stderr}")
    except Exception as e:
        print(f"Error running migrations: {e}")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)
app.include_router(merchant_router)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Merchant API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/status")
def status_check():
    return {"status": app.state.database_connection}
