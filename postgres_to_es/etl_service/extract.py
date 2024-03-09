from typing import Iterator, Tuple

import backoff
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from config import BACKOFF_CFG, POSTGRES_DSN
from models import GenresModel, MovieModel


@backoff.on_exception(**BACKOFF_CFG)
def postgres_client() -> connection:
    """Create PostgreSQL connection."""
    with psycopg2.connect(**POSTGRES_DSN, cursor_factory=DictCursor) as conn:
        return conn


@backoff.on_exception(**BACKOFF_CFG)
def data_generator(index: str, cursor: DictCursor) -> Iterator[Tuple[dict, str]]:
    """Create generator that makes records from postgresql query."""
    if index == 'genres':
        model = GenresModel
    if index == 'movies':
        model = MovieModel

    for line in cursor:
        instance = model(**line).model_dump()
        instance["_id"] = instance["id"]
        yield instance, str(line["modified"])


def sql_command(index, last_modified):

    if index == 'genres':
        return f"""
        SELECT genre.id,
            genre.name,
            genre.description,
            genre.modified AS modified
        FROM content.genre genre
        WHERE genre.modified > '{last_modified}'
        GROUP BY genre.id
        ORDER BY genre.modified ASC;
        """

    if index == 'movies':
        return f"""
        SELECT
           fw.id,
           fw.title,
           fw.description,
           fw.rating AS imdb_rating,
           COALESCE(
            JSON_AGG(
                   DISTINCT p.full_name)
                   FILTER (WHERE p.id is not null AND pfw.role = 'director'), '[]') AS director,
           COALESCE(
            JSON_AGG(
                   DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                   FILTER (WHERE p.id is not null AND pfw.role = 'actor'), '[]') AS actors,
           COALESCE(
            JSON_AGG(
                   DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                   FILTER (WHERE p.id is not null AND pfw.role = 'writer'), '[]') AS writers,
           COALESCE(
            JSON_AGG(DISTINCT p.full_name)
               FILTER (WHERE p.id is not null AND pfw.role = 'actor'), '[]') AS actors_names,
           COALESCE(
            JSON_AGG(DISTINCT p.full_name)
               FILTER (WHERE p.id is not null AND pfw.role = 'writer'), '[]') AS writers_names,
           COALESCE(
            JSON_AGG(DISTINCT g.name), '[]') AS genre,
           fw.modified AS modified
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified > '{last_modified}'
        GROUP BY fw.id
        ORDER BY fw.modified ASC;
        """
