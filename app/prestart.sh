#! /usr/bin/env bash

# Let the DB start
sleep 10;

cd /
alembic upgrade head
