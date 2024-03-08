from typing import Iterator, Tuple

import backoff
from elasticsearch import Elasticsearch

from config import BACKOFF_CFG
from state import set_state


@backoff.on_exception(**BACKOFF_CFG)
def elastic_client(connection_path: str) -> Elasticsearch:
    """Create Elasticsearch connection."""
    return Elasticsearch(connection_path)


@backoff.on_exception(**BACKOFF_CFG)
def es_loader(index, data: Iterator[Tuple[dict, str]]) -> Iterator[dict]:
    """Create iterator that give records from generated data."""
    last_modified = ''
    for record, modified in data:
        last_modified = modified
        yield record

        set_state(index, last_modified)
