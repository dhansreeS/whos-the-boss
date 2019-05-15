import logging.config
import argparse

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

#For importing config variables
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))

from config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME

logger = logging.getLogger(__name__)

Base = declarative_base()


class UserLines(Base):
    """ Defines the data model for the table `userlines`. """

    __tablename__ = 'userlines'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_text = Column(String(300), unique=False, nullable=False)
    time = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        userlines_repr = "<UserLines(id='%i', user_text='%s', time='%s')>"
        return userlines_repr % (self.id, self.user_text, self.time)


def create_sqlite_db(args):
    """Creates an sqlite database with the data models inherited from `Base` (UserLines).

    Args:
        args (argument from user): String defining SQLAlchemy connection URI in the form of

    Returns:
        None
    """

    engine = sqlalchemy.create_engine(args.engine_string)
    Base.metadata.create_all(engine)


def create_rds_db(args):
    """Creates an rds table? with the data models inherited from `Base` (UserLines).

        Args:
            args (argument from user): String defining RDS in the desrired form

        Returns:
            None
    """

    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, DATABASE_NAME)

    engine = sqlalchemy.create_engine(engine_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--database", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)

