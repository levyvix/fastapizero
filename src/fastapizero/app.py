from fastapi import FastAPI

from fastapizero.routers import auth, users
from fastapizero.schemas import (
    Message,
)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hello World'}
