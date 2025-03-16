#!/bin/sh
python main.py

python collector.py

exec "$@"