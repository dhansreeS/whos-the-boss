import boto3
import os
import botocore
import yaml
import sys
import config
import logging.config
logger = logging.getLogger(__name__)


def load_to_s3(args):
    """Loads data from one public S3 bucket to chosen S3 bucket.
    Bucket name can be passed as an argument or updated in the config file.

    Args:
        args (argument from user): Includes name of s3 bucket to transfer data to

    Returns:
        None
    """

    try:
        with open(config.AWS_CONFIG, 'r') as f:
            aws_config = yaml.load(f)
    except FileNotFoundError:
        logger.error('AWS config YAML File not Found')
        sys.exit(1)

    s3 = boto3.resource('s3')

    copy_source = {'Bucket': 'nw-dhansreesuraj-s3', 'Key': 'the_office_lines.csv'}

    if args.s3:
        bucketname = aws_config['DEST_S3_BUCKET']
        bucket = s3.Bucket(bucketname)

        try:
            bucket.copy(copy_source, 'raw/the_office_lines.csv')
            logger.info('File copied to s3 bucket %s', bucketname)

        except botocore.exceptions.NoCredentialsError as e:
            logger.error(e)
            sys.exit(3)

    else:
        source_bucket = s3.Bucket('nw-dhansreesuraj-s3')
        try:
            path = args.path
            os.makedirs(path + 'raw', exist_ok=True)

            source_bucket.download_file('the_office_lines.csv', path + 'raw/the_office_lines.csv')

        except botocore.exceptions.NoCredentialsError as e:
            logger.error(e)
            sys.exit(3)
