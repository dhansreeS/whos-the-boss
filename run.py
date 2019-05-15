"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

python3 run.py process --path=<name of path>
python3 run.py loadS3 --bucket=<name of bucket>
python3 run.py createSqlite --engine_string=<engine_string for connection>
python3 run.py createRDS --database=<Database in RDS>

"""
import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-whos-the-boss")

from src.clean_data import process_data
from src.load_data import load_to_s3
from src.data_model import create_sqlite_db, create_rds_db
from config import BUCKET_NAME, SQLALCHEMY_DATABASE_URI, DATABASE_NAME


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('process')
    sub_process.add_argument("--path", type=str, default="./data/", help="Path for the data")
    sub_process.set_defaults(func=process_data)

    sub_process = subparsers.add_parser('loadS3')
    sub_process.add_argument("--bucket", type=str, default=BUCKET_NAME, help="Bucket to be copied to")
    sub_process.set_defaults(func=load_to_s3)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--engine_string", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)

