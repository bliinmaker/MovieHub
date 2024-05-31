import os
from datetime import date

import dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, Movie, Actor


def get_db_url() -> str:
    dotenv.load_dotenv()
    PG_VARS = 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD', 'PG_DBNAME'
    credentials = {var: os.environ.get(var) for var in PG_VARS}
    return 'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'.format(**credentials)


if __name__ == '__main__':
    engine = create_engine(get_db_url())
    # Base.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(engine)

    # with Session(engine) as session:
    #     movie = Movie(
    #         category_title='Выпечка',
    #         category_description='Любая выпечка на ваш вкус!',

    #         actors=[
    #             Actor(
    #                 product_title='Булочка с маком',
    #                 product_price=40.0,
    #                 product_description='Много мака',
    #                 product_due_date='2024-05-19'
    #             ),
    #             Actor(
    #                 product_title='Чизкейк',
    #                 product_price=189.9,
    #                 product_description='Натуральный сыр',
    #                 product_due_date='2024-05-18'
    #             ),
    #         ]
    #     )
    #     session.add(category)
    #     session.commit()
    # productsSelect = select(Actor).where(Actor.product_price <= 60.0)
    # for product in Session(engine).scalars(productsSelect):
    #     print(product.product_price)
