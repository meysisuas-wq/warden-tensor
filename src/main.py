from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog, time
from src.config import settings
from src.api.routes import router as api_router
from src.db.database import init_db, close_db

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting WardenTensor")
    await init_db()
    yield
    await close_db()

def create_app() -> FastAPI:
    app = FastAPI(title="WardenTensor", description="Security Surveillance & Threat Detection",
                  version="1.0.0", docs_url="/docs" if settings.APP_DEBUG else None, lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.middleware("http")
    async def add_timing(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
        return response

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        logger.error("unhandled_exception", exc_info=exc)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    @app.get("/health", tags=["System"])
    async def health():
        return {"status": "healthy", "service": "warden-tensor", "version": "1.0.0"}

    app.include_router(api_router, prefix="/api/v1")
    return app

app = create_app()
