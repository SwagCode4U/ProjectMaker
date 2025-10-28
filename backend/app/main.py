# backend/app/main.py
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from loguru import logger
import uuid

# Optional rate limiting (slowapi)
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
except Exception:  # pragma: no cover
    Limiter = None  # type: ignore
    get_remote_address = None  # type: ignore
    RateLimitExceeded = None  # type: ignore
    SLOWAPI_AVAILABLE = False

from app.database import Base, init_engine
from app.routes import project_routes, setup_routes, generator_routes
from app.routes import fs_routes

# Initialize engine & create tables
engine = init_engine()
Base.metadata.create_all(bind=engine)  # creates tables automatically

# FastAPI app
app = FastAPI(title="ProjectMaker API", description="Interactive Project Scaffolding Wizard")

# Structured logging (Loguru)
# Rotates daily, keeps 7 days, includes backtrace for easier debugging
logger.add(
    "logs/{time}.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    backtrace=True,
    diagnose=True,
)

# CORS configuration
# Default dev origins (localhost common ports)
_default_origins = (
    "http://localhost:3000,"
    "http://localhost:3010,"
    "http://localhost:5173,"
    "http://127.0.0.1:3000,"
    "http://127.0.0.1:3010,"
    "http://127.0.0.1:5173"
)
raw = os.getenv("FRONTEND_ORIGINS")
if raw is None:
    # Use sensible defaults when env not provided
    origins = [o.strip() for o in _default_origins.split(",") if o.strip()]
    use_regex = False
else:
    raw = raw.strip()
    if raw == "":
        # Explicitly empty -> allow any localhost with regex (no credentials)
        origins = []
        use_regex = True
    else:
        origins = [o.strip() for o in raw.split(",") if o.strip()]
        use_regex = False

allow_credentials = True
cors_common = dict(allow_methods=["*"], allow_headers=["*"], expose_headers=["Content-Disposition"])  # for downloads

if use_regex:
    allow_credentials = False  # regex + credentials not allowed
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0):\d+$",
        allow_credentials=allow_credentials,
        **cors_common,
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        **cors_common,
    )

# Security headers middleware (lightweight)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Basic hardening headers
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("X-XSS-Protection", "1; mode=block")  # legacy but harmless
    # Minimal CSP suitable for API responses; adjust if serving HTML
    response.headers.setdefault("Content-Security-Policy", "default-src 'self' data: blob:")
    # Consider enabling HSTS only behind HTTPS (avoid breaking http dev)
    # response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
    return response

# Request/response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error for {request.method} {request.url}: {e}")
        raise
    logger.info(f"Response: {response.status_code} {request.method} {request.url}")
    return response

# Include routes
app.include_router(project_routes.router)
app.include_router(setup_routes.router)
app.include_router(generator_routes.router)
app.include_router(fs_routes.router)

# Optional global rate limiting (enabled if SLOWAPI_AVAILABLE and env RATE_LIMIT_ENABLED=true)
_rate_enabled = os.getenv("RATE_LIMIT_ENABLED", "true").lower() in ("1","true","yes","on")
_default_limit = os.getenv("RATE_LIMIT_DEFAULT", "120/minute")
if SLOWAPI_AVAILABLE and _rate_enabled:
    limiter = Limiter(key_func=get_remote_address, default_limits=[_default_limit])
    app.state.limiter = limiter  # type: ignore[attr-defined]
    from slowapi.middleware import SlowAPIMiddleware
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)  # type: ignore[misc]
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):  # type: ignore[valid-type]
        logger.warning(f"Rate limit exceeded for {request.client.host if request.client else 'unknown'} on {request.url}")
        return JSONResponse(status_code=429, content={"ok": False, "error": {"code": 429, "message": "Rate limit exceeded"}})

# Unified error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException {exc.status_code} at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url.path),
            }
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "ok": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors(),
                "path": str(request.url.path),
            }
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    rid = str(uuid.uuid4())
    logger.exception(f"Unhandled exception [{rid}] at {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": {
                "code": 500,
                "message": "Internal server error",
                "reference": rid,
                "path": str(request.url.path),
            }
        },
    )

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to ProjectMaker API", "status": "running"}

@app.get("/health")
def health():
    logger.debug("Health check")
    return {"status": "healthy"}
