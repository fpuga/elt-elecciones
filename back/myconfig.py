from pathlib import Path

from sqlalchemy import create_engine, event


DATA_FOLDER = Path(__file__).resolve().parent / "data"

engine = create_engine("postgresql://postgres:postgres@localhost:5432/elecciones")


@event.listens_for(engine, "connect", insert=True)
def create_schemas(dbapi_connection, _):
    existing_autocommit = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor = dbapi_connection.cursor()
    cursor.execute("CREATE SCHEMA IF NOT  EXISTS raw")
    cursor.close()
    dbapi_connection.autocommit = existing_autocommit
