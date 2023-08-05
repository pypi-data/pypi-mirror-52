import os
import pytest
import tempfile
from app.router import app as testapp
from app import db, engine, Base


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    yield testapp, db_path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.yield_fixture()
def db():
    Base.metadata.create_all(engine)
    yield db
    Base.metadata.drop_all(engine)


@pytest.yield_fixture
def client(app):
    with app[0].test_client() as cli:
        yield cli
