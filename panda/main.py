import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from panda import models
from panda.core.config import settings
from panda.database import engine
from panda.routers import address_router, appointments_router, patients_router

LOGGING = os.getenv('ENABLE_LOGGING', None)
if LOGGING == "true":
    logging.basicConfig(
        filename='app.log',
        filemode='w',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(address_router.router)
    _app.include_router(patients_router.router)
    _app.include_router(appointments_router.router)

    return _app


app = get_application()
logging.info('Running...')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} request to {request.url}\n"
                f"\tStatus_code: {response.status_code}\n"
                f"\tRequest_Body: {request.body()}\n")  # [ ] TODO get body and params
    return response


@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>PANDA CRUD API</title>
        </head>
        <body>
            <h1>Welcome to the PANDA API</h1>
            <p>See OPENAPI docs at: <a href="/docs">/docs</a></p>
            <p>Or Redoc docs at: <a href="/redoc">/redoc</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
