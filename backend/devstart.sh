#! /bin/bash

export FLASK_APP=snobby_server.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=../config/dev.py
export RUN_MODE='DEV'

python -m flask run
