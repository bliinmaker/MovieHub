"""Defines SQLAlchemy models for a movie database application."""

from uuid import UUID, uuid4

from sqlalchemy import (CheckConstraint, Column, ForeignKey, String,
                        UniqueConstraint)
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedColumn,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    """Base class."""

    pass


class UUIDMixin:
    """Represents uuid in the model."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Token(UUIDMixin, Base):
    """Represents a token in the database."""

    __tablename__ = 'token'
    value: MappedColumn[str] = Column(String, unique=True, nullable=False)
    __table_args__ = (UniqueConstraint('value', name='_token_uc'),)


class Actor(UUIDMixin, Base):
    """Represents an actor in the database."""

    __tablename__ = 'actor'
    full_name: MappedColumn[str]
    birth_date: MappedColumn[str]
    movie_id: Mapped[UUID] = mapped_column(ForeignKey('movie.id'))
    movie: MappedColumn['Movie'] = relationship(back_populates='actors')
    __table_args__ = (CheckConstraint('length(full_name) <= 30', 'full_name_valid_length'),)


class Movie(UUIDMixin, Base):
    """Represents a movie in the database."""

    __tablename__ = 'movie'
    title: MappedColumn[str]
    description: MappedColumn[str]
    genre: MappedColumn[str]
    year: MappedColumn[int]
    trailer: MappedColumn[str]
    poster: MappedColumn[str]
    actors: MappedColumn[list[Actor]] = relationship(back_populates='movie')
    __table_args__ = (
        CheckConstraint('length(title) <= 50', 'title_valid_length'),
        CheckConstraint('length(description) <= 500', 'description_valid_length'),
        UniqueConstraint('title', name='title_unique'),
    )
