#!/usr/bin/env python3.7
import os
import zipfile
import glob

LAMBDA_PACKAGE_PATH = 'dist/lambda.zip'
VENV_SITE_PACKAGES_PATH = '.venv/lib/python3.7/site-packages'

def create_lambda_package():
    print("Creating lambda package")
    try:
        os.remove(LAMBDA_PACKAGE_PATH)
    except FileNotFoundError:
        pass
    with zipfile.ZipFile(LAMBDA_PACKAGE_PATH, 'w', zipfile.ZIP_DEFLATED) as package_file:
        [package_file.write(f) for f in glob.glob('src/**/*.py', recursive=True)]
        add_package_dependencies(package_file)
    print("Lambda package created at {}".format(LAMBDA_PACKAGE_PATH))

def add_package_dependencies(package_file):
    print("Adding package dependencies")
    os.environ['PIPENV_VENV_IN_PROJECT'] = '1'
    os.system('pipenv install')
    [package_file.write(f) for f in glob.glob("{}/*/**".format(VENV_SITE_PACKAGES_PATH), recursive=True)]
    print("Package dependencies added")

create_lambda_package()
