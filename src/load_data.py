import boto3

s3 = boto3.resource('s3')

copy_source = {'Bucket': 'nw-dhansreesuraj-s3', 'Key': 'the_office_lines.csv'}
bucket = s3.Bucket('bucket_boss')
bucket.copy(copy_source, 'the_office_lines.csv')
