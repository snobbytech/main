#! /bin/bash
export FLASK_APP=snobby_server.py
export RUN_MODE='LIVE'

exec /home/ubuntu/miniconda3/bin/gunicorn app:app -b 0.0.0.0:8000
