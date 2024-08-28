from http import HTTPStatus

from jwt import decode

from fastapizero.security import (
    create_access_token,
    get_password_hash,
    settings,
    verify_password,
)


def test_jwt():
    data = {'username': 'levyvix'}
    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    assert decoded['username'] == 'levyvix'
    assert decoded['exp']


def test_password_hash():
    password = '123456'
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# user not in database
def test_jwt_invalid_credentials_not_in_database(client):
    token = create_access_token({'sub': 'joaozinho'})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# passou o username vazio
def test_jwt_invalid_credentials_no_username(client):
    token = create_access_token({})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
