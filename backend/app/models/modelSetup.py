"""
Basic stuff for setting up our database.
I'm kind of doing this insecurely right now. Don't mind, but in the future this needs
to be better.

To make a database locally, I followed these instructions.
https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e

For the future: probably don't need to touch this file, except for when you need to make
your own db.

"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# TODO: figure out if I can decouple app from the models here.

# might need this diff
from app import flask_app

def connect():
    url = "postgresql://{}:{}@{}:{}/{}"

    # All right, this is tough. But oh well.
    url = url.format(flask_app.config['DB_USERNAME'], flask_app.config['DB_PASSWORD'],
                     flask_app.config['DB_HOST'], flask_app.config['DB_PORT'], flask_app.config['DB_DBNAME'])
    connection = sqlalchemy.create_engine(url, client_encoding='utf8')

    # Bind this to metadata.
    meta = sqlalchemy.MetaData()
    meta.reflect(bind=connection)
    return connection, meta

con, meta = connect()
Session = sessionmaker(bind=con)


def dropAllTables():
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(flask_app.config['DB_USERNAME'], flask_app.config['DB_PASSWORD'],
                     flask_app.config['DB_HOST'], flask_app.config['DB_PORT'], flask_app.config['DB_DBNAME'])
    engine = sqlalchemy.create_engine(url)
    myMeta = sqlalchemy.MetaData(url)
    myMeta.reflect()
    myMeta.drop_all()

# Scoped session for db actions.
@contextmanager
def session_scope():
    s = Session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()
