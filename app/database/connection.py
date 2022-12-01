from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Connection:
    def __init__(self):
        self._engine = None
        self._session = None

    def init_connection(self, app: FastAPI, settings: dict):
        url = settings.database_url
        pool_recycle = 900
        echo = True

        self._engine = create_engine(
            url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True
        )
        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

        @app.on_event("startup")
        def startup():
            self._engine.connect()

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()

    def get_db(self):
        if self._session is None:
            raise Exception("Database session is None!")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = Connection()
Base = declarative_base()
