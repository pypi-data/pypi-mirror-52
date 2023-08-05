#!/bin/bash

set -ex

gc() {
  retval=$?
  echo "Stopping redis container"
  docker stop redis || :
  echo "Removing test containers"
  docker rm redis || :
  exit $retval
}

trap gc EXIT SIGINT

echo "Starting redis"
docker run --rm -d -p 6379:6379 --name=redis registry.fedoraproject.org/f28/redis

echo "Starting test suite"
python3 -m pytest --color=yes --verbose --showlocals

echo "Test suite passed \\o/"
