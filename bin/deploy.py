#!/usr/bin/env python3.7
from deploy.create_lambda_package import create_lambda_package
from deploy.deploy_stack import deploy_stack
from deploy.upload_lambda_package import upload_lambda_package

LAMBDA_PACKAGE_PATH = 'dist/lambda.zip'
VENV_SITE_PACKAGES_PATH = '.venv/lib/python3.7/site-packages'
SOURCE_CODE_STACK_NAME = 'etf-holdings-publisher-source-code-stack'
SOURCE_CODE_BUCKET_NAME = 'etf-holdings-publisher-lambda-source-code'
SOURCE_CODE_OBJECT_KEY = 'etf-holdings-publisher-lambda.zip'
TEMPLATE_FILE_PATH = "cloudformation/{stack_name}/template.yml"
PARAMS_FILE_PATH = "cloudformation/{stack_name}/params.json"
LAMBDA_STACK_NAME = 'etf-holdings-publisher-stack'

def deploy():
    print('\nCreating lambda package')
    create_lambda_package(LAMBDA_PACKAGE_PATH, VENV_SITE_PACKAGES_PATH)

    print('\nDeploying source code stack')
    deploy_stack(
        SOURCE_CODE_STACK_NAME,
        TEMPLATE_FILE_PATH.format(stack_name=SOURCE_CODE_STACK_NAME),
        PARAMS_FILE_PATH.format(stack_name=SOURCE_CODE_STACK_NAME)
    )

    print('\nUploading lambda package to S3')
    upload_lambda_package(
        LAMBDA_PACKAGE_PATH, SOURCE_CODE_BUCKET_NAME, SOURCE_CODE_OBJECT_KEY
    )

    print('\nDeploying the lambda function stack')
    deploy_stack(
        LAMBDA_STACK_NAME,
        TEMPLATE_FILE_PATH.format(stack_name=LAMBDA_STACK_NAME),
        PARAMS_FILE_PATH.format(stack_name=LAMBDA_STACK_NAME)
    )

deploy()
