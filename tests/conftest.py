from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapizero.app import app
from fastapizero.database import get_session
from fastapizero.models import User, table_registry
from fastapizero.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def created_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'manolo',
            'email': 'user@example.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    return response.json()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session) -> User:
    hashed_password = get_password_hash('testtest')
    user: User = User(
        username='Teste', email='teste@test.com', password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
