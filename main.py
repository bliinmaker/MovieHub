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
    # Base.metadata.drop_all(engine)

    with Session(engine) as session:
    #     movie1 = Movie(
    #             title='The Matrix',
    #             description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
    #             genre='Action, Sci-Fi',
    #             year=1999,
    #             trailer='https://www.youtube.com/embed/vKQi3bBA1y8?si=mVPfwqmnL2v9NscU',
    #             poster='https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Keanu Reeves',
    #                     birth_date='September 2, 1964'
    #                 ),
    #                 Actor(
    #                     full_name='Laurence Fishburne',
    #                     birth_date='July 30, 1961'
    #                 ),
    #                 Actor(
    #                     full_name='Carrie-Anne Moss',
    #                     birth_date='August 21, 1967'
    #                 ),
    #             ]
    #         )
    #     movie2 = Movie(
    #             title='Avatar: The Way of Water',
    #             description='Jake Sully, a paralyzed former Marine, is recruited by a company to be a body for an Avatar AI, which is used to control a remotely operated vehicle to extract a valuable mineral from an alien planet. However, when the Avatar is attacked, Jake takes control and becomes stranded on the planet. As Jake explores the planet and its people, he uncovers a conspiracy that threatens the entire alien civilization.',
    #             genre='Action, Adventure, Fantasy, Sci-Fi',
    #             year=2022,
    #             trailer='https://www.youtube.com/embed/a8Gx8wiNbs8?si=G0H29GEx-eM9_vtO',
    #             poster='https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Sam Worthington',
    #                     birth_date='August 2, 1976'
    #                 ),
    #                 Actor(
    #                     full_name='Zoe Saldana',
    #                     birth_date='June 19, 1978'
    #                 ),
    #                 Actor(
    #                     full_name='Sigourney Weaver',
    #                     birth_date='October 8, 1949'
    #                 ),
    #             ]
    #         )
    #     movie3 = Movie(
    #             title='Spider-Man: Across the Spider-Verse',
    #             description='After reuniting with Gwen Stacy, Brooklyn’s full-time, friendly neighborhood Spider-Man is catapulted across the Multiverse, where he encounters the Spider Society, a team of Spider-People charged with protecting the Multiverse’s very existence. But when the heroes clash on how to handle a new threat, Miles finds himself pitted against the other Spiders and must set out on his own to save those he loves most.',
    #             genre='Animation, Action, Adventure',
    #             year=2023,
    #             trailer='https://www.youtube.com/embed/cqGjhVJWtEg?si=1pNwsJ4oYO9oDfuN',
    #             poster='https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Shameik Moore',
    #                     birth_date='May 4, 1995'
    #                 ),
    #                 Actor(
    #                     full_name='Hailee Steinfeld',
    #                     birth_date='December 11, 1996'
    #                 ),
    #                 Actor(
    #                     full_name='Brian Tyree Henry',
    #                     birth_date='March 31, 1982'
    #                 ),
    #             ]
    #         )
    #     movie4 = Movie(
    #             title='Loki',
    #             description='The mercurial villain Loki resumes his role as the God of Mischief in a new series that takes place after the events of “Avengers: Endgame.',
    #             genre='Action, Adventure, Fantasy',
    #             year=2021,
    #             trailer='https://www.youtube.com/embed/nW948Va-l10?si=tcLUhnEuwanJ8Hz-',
    #             poster='https://m.media-amazon.com/images/M/MV5BNTY1ZDQzNzQtZGM1Yy00YjRhLTliYmMtOGM2OWFlYTRjOTc2XkEyXkFqcGdeQXVyMTY3MDE5MDY1._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Tom Hiddleston',
    #                     birth_date='February 9, 1981'
    #                 ),
    #                 Actor(
    #                     full_name='Owen Wilson',
    #                     birth_date='November 18, 1968'
    #                 ),
    #                 Actor(
    #                     full_name='Sophia Di Martino',
    #                     birth_date='November 15, 1983'
    #                 ),
    #             ]
    #         )
    #     movie5 = Movie(
    #             title='Superman & Lois',
    #             description='The world`s most famous superhero and comic books most famous journalist face the pressures and complexities that come with balancing work, justice, and parenthood in today`s society.',
    #             genre='Action, Adventure, Drama',
    #             year=2021,
    #             trailer='https://www.youtube.com/embed/SJPJPUpNvDw?si=slIToSe3_XB2LIoB',
    #             poster='https://m.media-amazon.com/images/M/MV5BMzdmYjAyODUtMTFkOS00MDg1LTljMDAtNzhiYTg5NjY1NjM5XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Tyler Hoechlin',
    #                     birth_date='September 11, 1987'
    #                 ),
    #                 Actor(
    #                     full_name='Elizabeth Tulloch',
    #                     birth_date='January 19, 1981'
    #                 ),
    #             ]
    #         )
    #     movie6 = Movie(
    #             title='John Wick',
    #             description='Keanu Reeves stars as John Wick, a legendary hitman who comes out of retirement to seek revenge against the men who killed his puppy, a final gift from his recently deceased wife.',
    #             genre='Action, Mystery, Thriller',
    #             year=2014,
    #             trailer='https://www.youtube.com/embed/C0BMx-qxsP4?si=AYK56ly0QnVWhskS',
    #             poster='https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Keanu Reeves',
    #                     birth_date='September 2, 1964'
    #                 ),
    #                 Actor(
    #                     full_name='Michael Nyqvist',
    #                     birth_date='November 8, 1960'
    #                 ),
    #             ]
    #         )
    #     movie7 = Movie(
    #             title='Interstellar',
    #             description='A team of explorers travel through a wormhole in space in an attempt to ensure humanity`s survival.',
    #             genre='Adventure, Drama, Sci-Fi',
    #             year=2014,
    #             trailer='https://www.youtube.com/embed/zSWdZVtXT7E?si=91yt8Qlyfvw30Cm4',
    #             poster='https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Matthew McConaughey',
    #                     birth_date='November 4, 1969'
    #                 ),
    #                 Actor(
    #                     full_name='Anne Hathaway',
    #                     birth_date='November 12, 1982'
    #                 ),
    #                 Actor(
    #                     full_name='Jessica Chastain',
    #                     birth_date='March 24, 1977'
    #                 ),
    #             ]
    #         )
    #     movie8 = Movie(
    #             title='Supernatural',
    #             description='Two brothers follow their father`s footsteps as hunters, fighting evil supernatural beings of many kinds, including monsters, demons and gods that roam the earth.',
    #             genre='Drama, Fantasy, Horror, Mystery, Thriller',
    #             year=2005,
    #             trailer='https://www.youtube.com/embed/HPKiZaEzMko?si=-cnbkdvRTrRIElFG',
    #             poster='https://m.media-amazon.com/images/M/MV5BNzRmZWJhNjUtY2ZkYy00N2MyLWJmNTktOTAwY2VkODVmOGY3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
    #
    #             actors=[
    #                 Actor(
    #                     full_name='Jared Padalecki',
    #                     birth_date='July 19, 1982'
    #                 ),
    #                 Actor(
    #                     full_name='Jensen Ackles',
    #                     birth_date='March 1, 1978'
    #                 ),
    #                 Actor(
    #                     full_name='Jim Beaver',
    #                     birth_date='August 12, 1950'
    #                 ),
    #             ]
    #         )
        token = Token(
            value='5720906c'
        )
        session.add(token)
        session.commit()
    #
    #     session.add(movie1)
    #     session.add(movie2)
    #     session.add(movie3)
    #     session.add(movie4)
    #     session.add(movie5)
    #     session.add(movie6)
    #     session.add(movie7)
    #     session.add(movie8)
