import boto3
import argparse


def load_to_s3(args):
    """Loads data from one public S3 bucket to chosen S3 bucket.
    Bucket name can be passed as an argument or updated in the config file.

    Args:
        args (argument from user): Includes name of s3 bucket to transfer data to

    Returns:
        None
    """

    s3 = boto3.resource('s3')

    bucketname = args.bucket
    copy_source = {'Bucket': 'nw-dhansreesuraj-s3', 'Key': 'the_office_lines.csv'}
    bucket = s3.Bucket(bucketname)
    bucket.copy(copy_source, 'the_office_lines.csv')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('loadS3')
    sub_process.add_argument("--bucket", type=str, default=BUCKET_NAME, help="Bucket to be copied to")
    sub_process.set_defaults(func=load_to_s3)

    args = parser.parse_args()
    args.func(args)

