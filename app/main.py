from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.config import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.middlewares import ProcessTimeMiddleware
from app.api.api import router as api_router
from app.core.config import API_PREFIX


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # application.add_middleware(ProcessTimeMiddleware)

    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
