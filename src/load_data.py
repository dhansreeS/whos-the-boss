import boto3

s3 = boto3.resource('s3')

copy_source = {'Bucket': 'nw-dhansreesuraj-s3'}
bucket = s3.Bucket('bucket_boss')
bucket.copy(copy_source, '/raw/the-office-lines.csv')
