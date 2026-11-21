import os

from sqlalchemy import create_engine, text

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Set it to your PostgreSQL connection URL."
    )

engine = create_engine(database_url)

with engine.connect() as conn:
    for row in conn.execute(text("SELECT * FROM notes")):
        print(row)


