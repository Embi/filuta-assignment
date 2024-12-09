from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.utils.conf import ApiSettings
from api.routes import cars, token, users
# from api.middlewares.auth import FakeAuthMiddleware


def get_application() -> FastAPI:
    """
    Initialize FastAPI App.
    This initialization is done inside of a function to allow potential
    unit testing.
    """
    api_settings = ApiSettings()

    app = FastAPI(
        docs_url=api_settings.docs_url,
        redoc_url=api_settings.redoc_url,
    )

    # TODO restrict allowed origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_v1 = APIRouter()
    api_v1.include_router(users.router, prefix="/users")
    api_v1.include_router(cars.router, prefix="/cars")
    api_v1.include_router(token.router, prefix="/token")
    app.include_router(api_v1, prefix="/api/v1")

    return app


app = get_application()
