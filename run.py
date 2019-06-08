"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

python3 run.py process --path=<name of path> --s3=<True or False>
python3 run.py load
python3 run.py createSqlite
python3 run.py createRDS --username=<Username for RDS> --password=<Password for RDS>

"""
import argparse
import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('run-whos-the-boss')

from src.clean_data import process_data
from src.load_data import load_to_s3
from src.data_model import create_sqlite_db, create_rds_db
from config import SQLALCHEMY_DATABASE_URI


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Data processes')
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('process')
    sub_process.add_argument('--path', type=str, default='./data/', help='Path for the data')
    sub_process.add_argument('--s3', default=False, help='Load from s3 or not')
    sub_process.set_defaults(func=process_data)

    sub_process = subparsers.add_parser('load')
    sub_process.add_argument('--path', type=str, default='./data/', help='Path to load data to')
    sub_process.add_argument('--s3', default=False, help='Load to S3 bucket or not')
    sub_process.set_defaults(func=load_to_s3)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                             help='Engine String for local sqlite db')
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument('--username', type=str, default=None,
                             help='Username for RDS')
    sub_process.add_argument('--password', type=str, default=None,
                             help='Password for RDS')
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)

