from http import HTTPStatus

from fastapi.testclient import TestClient

from src.fastapizero.app import app


def test_read_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'World'}


def test_read_batatinha():
    client = TestClient(app)
    response = client.get('/batatinha')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'batatinha': 'batatinha'}
