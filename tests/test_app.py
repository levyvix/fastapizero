from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.fastapizero.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'john',
            'email': 'john@gmail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'john',
        'email': 'john@gmail.com',
    }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'john', 'email': 'john@gmail.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'john',
            'email': 'john@gmail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'john',
        'email': 'john@gmail.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
