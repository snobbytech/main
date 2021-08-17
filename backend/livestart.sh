#! /bin/bash
export FLASK_APP=snobby_server.py
export RUN_MODE='LIVE'
export APP_CONFIG_FILE=../config/prod.py

exec /home/ubuntu/miniconda3/bin/gunicorn app:flask_app -b 0.0.0.0:8000
