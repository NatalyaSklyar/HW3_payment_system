from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from payments.repositories.base import Session, create_tables
from payments.routers.account import router as account_router
from payments.services.inbox import InboxService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    tasks = [
        create_task(InboxService(Session).inbox_daemon()),
    ]
    yield
    for task in tasks:
        task.cancel()
        try:
            await task
        except CancelledError:
            pass


app = FastAPI(
    title="Payments Service",
    description="Service for managing user accounts and transactions.",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
