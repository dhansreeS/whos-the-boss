import logging.config
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os
import sys


logger = logging.getLogger(__name__)

Base = declarative_base()


class UserLines(Base):
    """ Defines the data model for the table `userlines`. """

    __tablename__ = 'userlines'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_text = Column(String(300), unique=False, nullable=False)
    predicted = Column(String(30), unique=False, nullable=False)
    time = Column(DateTime, unique=False, nullable=False)

    def __repr__(self):
        userlines_repr = "<UserLines(id='%i', user_text='%s', predicted='%s', time='%s')>"
        return userlines_repr % (self.id, self.user_text, self.predicted, self.time)


def create_sqlite_db(args):
    """Creates an sqlite database with the data models inherited from `Base` (UserLines).
    URI can be passed as an argument or updated in the config file.

    Args:
        args (argument from user): String defining SQLAlchemy connection URI in the desired form

    Returns:
        None
    """

    try:
        engine = sqlalchemy.create_engine(args.engine_string)
        logger.info('SQLite database created')

        Base.metadata.create_all(engine)
        logger.info('Table created in SQLite database')

    except Exception as e:
        logger.error(e)
        sys.exit(5)


def create_rds_db(args):
    """Creates an rds table with the data models inherited from `Base` (UserLines).
    Host, password, user and port are accessed from environment variables.
    Database name can be passed as argument or updated in the config file.

        Args:
            args (argument from user): Includes username and password

        Returns:
            None
    """

    aws_config = args.rdsConfig

    conn_type = aws_config['CONN_TYPE']
    host = aws_config['HOST_NAME']
    port = aws_config['PORT_NO']
    database = aws_config['DATABASE_NAME']

    if args.username is None:
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
    else:
        user = args.username
        password = args.password

    engine_string = '{}://{}:{}@{}:{}/{}'. \
        format(conn_type, user, password, host, port, database)

    try:
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)

        logger.info('Table created in RDS database')
    except Exception as e:
        logger.error(e)
        sys.exit(3)

