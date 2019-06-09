import boto3
import os
import botocore
import sys
import logging.config
logger = logging.getLogger(__name__)


def load_data(args):
    """Loads data from one public S3 bucket to chosen S3 bucket or from public s3 to local
    Bucket name can be passed as an argument or updated in the config file.

    Args:
        args (argument from user): Includes name of s3 bucket to transfer data to

    Returns:
        None
    """

    s3 = boto3.resource('s3')
    s3_config = args.s3config

    copy_source = {'Bucket': s3_config['PUBLIC_S3'], 'Key': s3_config['FILE_NAME']}

    if args.s3:
        bucketname = s3_config['DEST_S3_BUCKET']
        bucket = s3.Bucket(bucketname)

        try:
            bucket.copy(copy_source, s3_config['DEST_FILE_NAME'])
            logger.info('File copied to s3 bucket %s', bucketname)

        except botocore.exceptions.NoCredentialsError as e:
            logger.error(e)
            sys.exit(3)

    else:
        source_bucket = s3.Bucket(s3_config['PUBLIC_S3'])
        try:
            localConf = args.localConf
            os.makedirs(localConf['PATH'], exist_ok=True)

            source_bucket.download_file(s3_config['FILE_NAME'], localConf['PATH'] + '/' + localConf['FILE_NAME'])
            logger.info('File copied to local file path')

        except botocore.exceptions.NoCredentialsError as e:
            logger.error(e)
            sys.exit(3)
