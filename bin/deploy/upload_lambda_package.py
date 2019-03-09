import boto3

def upload_lambda_package(package_path, s3_bucket_name, s3_object_key):
    print("Start to upload lambda package {} to S3 bucket {} as {}".format(
        package_path, s3_bucket_name, s3_object_key
    ))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket_name)
    with open(package_path, 'rb') as package_file:
        bucket.put_object(Key=s3_object_key, Body=package_file)
    print('Lambda package uploaded to S3')
