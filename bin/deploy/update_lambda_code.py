import boto3

def update_lambda_code(func_name, source_code_bucket_name, source_code_key):
    print("Start to update function code for lambda {} with {} - {} in S3".format(
        func_name, source_code_bucket_name, source_code_key
    ))
    client = boto3.client('lambda')
    client.update_function_code(
        FunctionName=func_name,
        S3Bucket=source_code_bucket_name,
        S3Key=source_code_key
    )
    print("Updating lambda function code finished")
    
