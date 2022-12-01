import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base, db
from app.common.config import Settings
from main import app

settings = Settings()
engine = create_engine(settings.test_database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()


app.dependency_overrides[db.get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def clear_all_data():
    session = next(override_get_db())
    session.execute("SET FOREIGN_KEY_CHECKS = 0;")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()
