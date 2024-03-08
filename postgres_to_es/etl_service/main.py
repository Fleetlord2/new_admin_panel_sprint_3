import time
from datetime import datetime

from elasticsearch import helpers

from config import ELASTIC_PATH, INDEXES, ITERSIZE, TIME_SLEEP
from extract import data_generator, postgres_client, sql_command
from load import elastic_client, es_loader
from state import get_state

if __name__ == "__main__":

    while True:

        for index in INDEXES:

            last_modified = get_state(index, default=str(datetime.min))
            sql = sql_command(index, last_modified)

            psql_cursor = postgres_client().cursor()
            psql_cursor.itersize = ITERSIZE
            psql_cursor.execute(sql)
            extracted_data = data_generator(index, psql_cursor)

            docs = es_loader(index, extracted_data)
            client = elastic_client(ELASTIC_PATH)

            lines, _ = helpers.bulk(
                client=client,
                actions=docs,
                index=index,
            )

        time.sleep(TIME_SLEEP)
