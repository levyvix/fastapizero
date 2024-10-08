from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapizero.database import get_session
from fastapizero.models import User
from fastapizero.schemas import Token
from fastapizero.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[Session, Depends(get_session)]
T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    session: T_Session,
    form_data: T_FormData,
):
    user = session.scalar(
        select(User).where((User.email == form_data.username))
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )

    # usuario existe
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
