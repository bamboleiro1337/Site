import os
from dataclasses import dataclass

from dotenv import load_dotenv



load_dotenv()

@dataclass
class Settings:

    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_USER = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '')

    TOKEN_SECRET=os.getenv('TOKEN_SECRET') or ''
    TOKEN_ALGORITHM=os.getenv('TOKEN_ALGORITHM') or ''

    MAX_NOTES_LEN = 200

    MIN_PASSWORD_LENGTH = 8

    @property
    def DATABASE_CONFIG(self):
        return f'postgresql+asyncpg://{Settings.DATABASE_USER}:{Settings.DATABASE_PASSWORD}@' \
               f'{Settings.DATABASE_HOST}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}'
               
               
               
#do not move these imports to top
import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth import router_auth
from app.web_pages import router_web_pages
from app.sockets import router_websocket

sentry_sdk.init(
    dsn="https://1a6b12e7dbf7418233793cb807de9e53@o4505229726318592.ingest.sentry.io/4505761003864065",
    traces_sample_rate=1.0,
)


app = FastAPI(
    title='First app',
    description='Logger',
    version='0.0.1',
    debug=True,
)

app.mount('/Logger/app/static', StaticFiles(directory='app/static'), name='static')


app.include_router(router_web_pages.router)
app.include_router(router_auth.router)
app.include_router(router_websocket.router)


@app.get('/')
@app.post('/')
async def main_page() -> dict:
    return {'greeting': 'HELLO'}



@app.get('/{username}')
@app.get('/{username}/{user_nick}')
async def user_page(user_name: str, user_nick: str = '', limit: int = 10, skip: int = 0) -> dict:
    
    data = [i for i in range(1000)][skip:][:limit]
    return {'user_name': user_name, 'user_nick': user_nick, 'data': data}
