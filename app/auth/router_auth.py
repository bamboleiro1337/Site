from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)

import dao
from app.auth import dependencies

from .auth_lib import AuthHandler, AuthLibrary
from .schemas import AuthDetails, AuthLogin, AuthRegistered

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register', response_model=AuthRegistered, status_code=status.HTTP_201_CREATED)
async def register_api(request: Request, response: Response, auth_details: AuthDetails):
    is_login_already_used = await dao.get_user_by_login(auth_details.login)
    
    if is_login_already_used:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'User with email {auth_details.login} already exists'
        )

    hashed_password = await AuthHandler.get_password_hash(auth_details.password)

    user_data = await dao.create_user(
        name=auth_details.name,
        second_name=auth_details.second_name,
        login=auth_details.login,
        password=hashed_password,
        age=auth_details.age,   
        ip=auth_details.ip,
        city=auth_details.city,
        country=auth_details.country,
        region=auth_details.region,
        is_admin=auth_details.is_admin
    )

    token = await AuthHandler.encode_token(user_data[0])
    response.set_cookie(key='my_name', value='Oleg', max_age=10, httponly=True)
    response.set_cookie(key='token', value=token, httponly=True)

    return AuthRegistered(success=True, id=user_data[0], login=user_data[1])


@router.post('/login')
async def login_api(response: Response, user_data: AuthLogin):
    user = await AuthLibrary.authenticate_user(user_data.login, user_data.password)
    token = await AuthHandler.encode_token(user.id)
    response.set_cookie(key='token', value=token, httponly=True)
    return {'user': user.login, "logged_in": True}


@router.post('/logout')
async def logout_api(response: Response, user=Depends(dependencies.get_current_user_optional)):
    response.delete_cookie('token')
    return {'user': 'yep', "logged_out": True}

