https://www.elephantsql.com/
https://www.pgadmin.org/download/
https://dbeaver.io/download/


pip install python-dotenv
pip install sqlalchemy alembic asyncpg psycopg2 psycopg2-binary
pip install fastapi[all] pytest pytest-asyncio
pip install websockets
pip install pyjwt


If you made some changes in models:
1. alembic init migration
2. alembic revision --autogenerate -m 'your_name' 
3. alembic upgrade head


If something gone wrong in db:
 alembic downgrade -1
 It`s like backup btw

 Result: "second -> first" 



If you need to test this piece of shit:
pytest -vs .

If you need to make clear code
isort .



-----------------How to start the project-----------------

1. Make sure that you have docker container started(if not, run 'docker compose up')
2. Create venv and run 'pip install -r requirements.txt'
3. Run 'uvicorn app.main:app --reload --port [your port]'
4. Link to website: http://127.0.0.1:[your port]


Admin account
Login: user2@user.use
Password: qwerqrweqwer