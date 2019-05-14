import boto3


def load_to_s3 (args) :

    s3 = boto3.resource('s3')

    bucketName = args.bucket
    copy_source = {'Bucket': 'nw-dhansreesuraj-s3', 'Key': 'the_office_lines.csv'}
    bucket = s3.Bucket(bucketName)
    bucket.copy(copy_source, 'the_office_lines.csv')
