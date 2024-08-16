from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapizero.schemas import (
    Message,
    UserDB,
    UserListWithId,
    UserPublicId,
    UserPulic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPulic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users', response_model=UserListWithId)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPulic)
def update_user(user_id: int, user: UserSchema):
    if user_id not in [user.id for user in database]:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id not in [user.id for user in database]:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    del database[user_id - 1]
    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublicId)
def read_user(user_id: int):
    if len(database) < user_id or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    return database[user_id - 1]
