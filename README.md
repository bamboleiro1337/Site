https://www.elephantsql.com/
https://www.pgadmin.org/download/
https://dbeaver.io/download/


pip install python-dotenv
pip install sqlalchemy alembic asyncpg psycopg2 psycopg2-binary
pip install fastapi[all] pytest pytest-asyncio
pip install websockets
pip install pyjwt


alembic init migration
alembic revision --autogenerate -m 'initial' 
 alembic upgrade head
 alembic downgrade -1


pytest -vs .
isort .



-----------------How to start the project-----------------

1. Make sure that you have docker container started(if not, run 'docker compose up')
2. Create venv and run 'pip install -r requirements.txt'
3. Run 'uvicorn settings:app --reload --port [your port]'
4. Link to website: http://127.0.0.1:[your port]
