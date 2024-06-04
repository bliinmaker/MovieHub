"""Module for creating and managing the database."""

import os
from datetime import date

import dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Actor, Base, Movie, Token

dotenv.load_dotenv()


def get_db_url() -> str:
    """
    Construct and return the SQLAlchemy database URL using environment variables.

    Returns:
        str: The formatted database URL string.
    """
    ENV_VARIABLE_NAMES = 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD', 'PG_DBNAME'
    credentials = {env_var: os.environ.get(env_var) for env_var in ENV_VARIABLE_NAMES}
    return 'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'.format(**credentials)


if __name__ == '__main__':
    engine = create_engine(get_db_url())
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        token = Token(
            value='5720906c',
        )
        session.add(token)
        session.commit()
