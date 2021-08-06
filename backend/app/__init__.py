from flask import Flask

"""
This sets up our flask project.

TODO: turn this into a well-structured thing. For now, it's kind of just a module definer.

"""

# Just putting the imports in, but basically won't be doing logging until later on.
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# TODO: integrate sentry.




flask_app = Flask(__name__, instance_relative_config=True)

# Load default configs.
flask_app.config.from_object('config.default')
flask_app.config.from_envvar('APP_CONFIG_FILE')

# Load from the instance folder.
#app.config.from_pyfile('config.py', silent=True)

# Load more options from the environment variable.
#app.config.from_envvar('APP_CONFIG_FILE')
