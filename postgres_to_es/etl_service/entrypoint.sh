#!/usr/bin/env bash

readonly cmd="$*"

while ! nc -z elasticsearch 9200; do
      sleep 5
      echo "Elasticsearch not ready"
done

echo "Elasticsearch is ready"

curl -XPUT http://elasticsearch:9200/movies -H 'Content-Type: application/json' -d @/movies.json
curl -XPUT http://elasticsearch:9200/genres -H 'Content-Type: application/json' -d @/genres.json

echo "Elasticsearch indexes were created"

exec $cmd
