"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

python3 run.py load --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>
python3 run.py process --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>
python3 run.py createSqlite --engine_string=<Database URI for sqlite db>
python3 run.py createRDS --rdsConfig=<RDS configurations> --username=<Username for RDS> --password=<Password for RDS>
python3 run.py train --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>
python3 run.py evaluate --localConf=<local data configurations> --s3=<True or False> --s3config=<s3 configurations>
python3 run.py app
"""
import argparse
import logging.config
import sys
import config
import yaml
from os import path
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('run-whos-the-boss')

from src.clean_data import process_data
from src.load_data import load_data
from src.data_model import create_sqlite_db, create_rds_db
from src.train_model import train
from src.evaluate_model import evaluate
from config import PROJECT_HOME


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Data processes')
    subparsers = parser.add_subparsers()

    try:
        with open(config.CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
    except FileNotFoundError:
        logger.error('config YAML File not Found')
        sys.exit(1)

    sql_config = config['sqldb']
    DB_PATH = path.join(PROJECT_HOME, sql_config['DB_PATH'])
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)

    sub_process = subparsers.add_parser('load')
    sub_process.add_argument('--localConf', default=config['first_load'],
                             help='Local data configurations ')
    sub_process.add_argument('--s3', default=False, help='Load to S3 bucket or not')
    sub_process.add_argument('--s3config', default=config['s3'], help='s3 configurations')
    sub_process.set_defaults(func=load_data)

    sub_process = subparsers.add_parser('process')
    sub_process.add_argument('--localConf', default=config['processed'],
                             help='Configurations for local processed data')
    sub_process.add_argument('--s3', default=False, help='Load from s3 or not')
    sub_process.add_argument('--s3config', default=config['s3'], help='s3 configurations')
    sub_process.set_defaults(func=process_data)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                             help='Engine String for local sqlite db')
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument('--rdsConfig', type=str, default=config['rds'],
                             help='RDS configurations')
    sub_process.add_argument('--username', type=str, default=None,
                             help='Username for RDS')
    sub_process.add_argument('--password', type=str, default=None,
                             help='Password for RDS')
    sub_process.set_defaults(func=create_rds_db)

    sub_process = subparsers.add_parser('train')
    sub_process.add_argument('--localConf', default=config['train'],
                             help='Configurations for training')
    sub_process.add_argument('--s3', default=False, help='Load from s3 or not')
    sub_process.add_argument('--s3config', default=config['s3'], help='s3 configurations')
    sub_process.set_defaults(func=train)

    sub_process = subparsers.add_parser('evaluate')
    sub_process.add_argument('--localConf', default=config['evaluate'],
                             help='Configurations for evaluation')
    sub_process.add_argument('--s3', default=False, help='Load from s3 or not')
    sub_process.add_argument('--s3config', default=config['s3'], help='s3 configurations')
    sub_process.set_defaults(func=evaluate)

    from app.app import start_app
    sub_process = subparsers.add_parser('app')
    sub_process.set_defaults(func=start_app)

    args = parser.parse_args()
    args.func(args)

