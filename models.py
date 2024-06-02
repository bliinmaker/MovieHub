from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, Column, String, DateTime, func
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedColumn,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Token(UUIDMixin, Base):
    __tablename__ = 'token'

    value: MappedColumn[str] = Column(String, unique=True, nullable=False)

    __table_args__ = (UniqueConstraint('value', name='_token_uc'),)


class Actor(UUIDMixin, Base):
    __tablename__ = 'actor'
    full_name: MappedColumn[str]
    birth_date: MappedColumn[str]

    movie_id: Mapped[UUID] = mapped_column(ForeignKey('movie.id'))
    movie: MappedColumn['Movie'] = relationship(
        back_populates='actors')

    __table_args__ = (
        CheckConstraint('length(full_name) <= 30',
                        'full_name_valid_length'),
    )


class Movie(UUIDMixin, Base):
    __tablename__ = 'movie'
    title: MappedColumn[str]
    description: MappedColumn[str]
    genre: MappedColumn[str]
    year: MappedColumn[int]
    trailer: MappedColumn[str]
    poster: MappedColumn[str]
    actors: MappedColumn[list[Actor]] = relationship(
        back_populates='movie')

    __table_args__ = (
        CheckConstraint('length(title) <= 50',
                        'title_valid_length'),
        CheckConstraint('length(description) <= 500',
                        'description_valid_length'),
        UniqueConstraint('title', name='title_unique')
    )