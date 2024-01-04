import json
from urllib.request import urlopen

from fastapi import (APIRouter, Depends, Form, Header, HTTPException, Request,
                     Response, status)
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import dao
import settings
from app.auth import dependencies
from app.auth.auth_lib import AuthHandler, AuthLibrary



router = APIRouter(
    prefix='/web',
    tags=['menu', 'landing'],
)

templates = Jinja2Templates(directory='app\\templates')



@router.get('/')
async def get_main_page(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'user': user,
    }

    return templates.TemplateResponse(
        'base.html',
        context=context,
    )



@router.get('/home')
async def get_menu(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Home',
        'user': user,
    }
    print(context)
    return templates.TemplateResponse(
        'home.html',
        context=context,
    )




@router.get('/register')
@router.post('/register')
async def register(request: Request):
    context = {
        'request': request,
        'title': 'Sign in',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )



@router.post('/register-final')
async def register_final(request: Request,
                         x_forwarded_for: str = Header(None),
                         name: str = Form(),
                         second_name: str = Form(),
                         login: EmailStr = Form(),
                         password: str = Form(),
                         age: str = Form(),
                         ip: str = Form(default=''),
                         city: str = Form(default=''),
                         country: str = Form(default=''),
                         region: str = Form(default=''),
                         is_admin: bool = Form(default=False)
                         ): 
    
    is_login_already_used = await dao.get_user_by_login(login)
    
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else None
    

    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    location = json.load(response)

    city = location['city']
    country = location['country']
    region = location['region']


    
    if is_login_already_used:
        context = {
            'request': request,
            'title': 'User error',
            'content': f'User {login} already exists',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    
    hashed_password = password
    
    user_data = await dao.create_user(
        name=name,
        second_name=second_name,
        login=login,
        password=hashed_password,
        age=age,
        ip=ip, 
        city=city,
        country=country,
        region=region,
        is_admin=is_admin
    )

    token = await AuthHandler.encode_token(user_data[0])

    
    context = {
        'request': request,
        'title': 'Register final',
        'user': user_data,
    }

    template_response = templates.TemplateResponse(
        'home.html',
        context=context,
    )


    template_response.set_cookie(key='token', value=token, httponly=True)
    return template_response



@router.get('/login')
async def login(request: Request):
    context = {
        'request': request,
        'title': 'Log in',
        
    }

    return templates.TemplateResponse(
        'login.html',
        context=context,
    )



@router.post('/login-final')
async def login(request: Request, login: EmailStr = Form(), password: str = Form()):
    user = await AuthLibrary.authenticate_user(login=login, password=password)
    token = await AuthHandler.encode_token(user.id)

    
    context = {
        'request': request,
        'title': 'Login final',
        'user': user,
    }

    response =  templates.TemplateResponse(
        'home.html',
        context=context,
    )
    
    response.set_cookie(key='token', value=token, httponly=True)
    return response




@router.post('/logout')
@router.get('/logout')
async def logout(request: Request, response: Response, user=Depends(dependencies.get_current_user_optional)):
    
    
    context = {
        'request': request,
        'title': 'Logout',

    }
    result = templates.TemplateResponse(
        'home.html',
        context=context,
    )
    result.delete_cookie('token')
    return result



@router.get('/message')
async def message(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Message',
        'user': user,

    }

    return templates.TemplateResponse(
        'msg.html',
        context=context,
    )
