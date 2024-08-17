import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapizero.app import app
from fastapizero.models import User, table_registry

client = TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as sess:
        yield sess

    table_registry.metadata.drop_all(engine)


def test_create_user(session):
    new_user: User = User(
        username='maria',
        password='123456',
        email='maria@example.com',
    )
    session.add(new_user)
    session.commit()

    user: User = session.scalar(select(User).where(User.username == 'maria'))

    assert user.username == 'maria'
