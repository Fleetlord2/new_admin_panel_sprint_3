from uuid import UUID

from pydantic import BaseModel


class AbstractModel(BaseModel):
    id: UUID


class Persons(AbstractModel):
    name: str


class GenresModel(AbstractModel):
    name: str
    description: str | None


class MovieModel(AbstractModel):
    title: str
    description: str | None
    imdb_rating: float | None
    genre: list[str | None]
    director: list[str | None]
    actors: list[Persons | None]
    writers: list[Persons | None]
    actors_names: list[str | None]
    writers_names: list[str | None]
