import socket
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from loguru import logger

from constants import c
from services.api.routers.v1 import router as router_v1
from task import app as celery_app
from task import refresh_task

if c.structured_logging:
    logger.remove()
    logger.add(sys.stdout, serialize=True)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    logger.debug("Starting Server 🚀")
    yield
    logger.warning("Shutting down gracefully...")
    logger.warning("Cleanup complete. Server will now exit.")


app = FastAPI(
    root_path="/api",
    title=c.title,
    description=c.description,
    summary="",
    terms_of_service="",
    docs_url="/docs",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit",
    },
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(router_v1)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time: float = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    client_host = request.client.host if request.client else "unknown"
    logger.debug(
        f"[{client_host}] Request: "
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s",
        client_host=client_host,
        method=request.method,
        url=request.url,
        path_params=request.path_params,
        query_params=request.query_params,
        headers=request.headers,
        status_code=response.status_code,
        response_time=process_time,
    )
    return response


@app.get("/ping")
async def ping() -> Response:
    """Test if the server is up and running"""
    return Response(content="pong!", media_type="text/plain")


redis_client = {}


@app.post("/refresh")
def request_refresh():
    task_id = redis_client.get("current_refresh_task")
    if task_id:
        result = celery_app.AsyncResult(task_id)
        if result.state in ("PENDING", "STARTED"):
            return {"status": "already_queued", "task_id": task_id}

    task = refresh_task.delay()
    redis_client["current_refresh_task"] = task.id
    return {"status": "queued", "task_id": task.id}


@app.get("/")
async def read_root():
    return {"message": "Hello!", "container_id": socket.gethostname()}
