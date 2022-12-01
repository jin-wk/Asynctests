from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.common.config import get_settings
from app.database.connection import db
from app.routes import index, auth


def create_app():
    app = FastAPI()
    settings = get_settings()
    db.init_connection(app, settings)

    # app.add_middleware(middleware_class=BaseHTTPMiddleware)
    app.add_middleware(
        middleware_class=CORSMiddleware, allow_origins=["*"], allow_methods=["*"]
    )
    app.include_router(index.router)
    app.include_router(auth.router)
    return app


app = create_app()
