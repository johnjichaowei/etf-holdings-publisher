# ETF Holdings Publisher
A python lambda function to publish the holdings of one ETF fund to SNS Topic

## Setup project

install python3.7

```
python3.7 -m pip install --user --upgrade pip
python3.7 -m pip install --user --upgrade pipenv

export PIPENV_VENV_IN_PROJECT=1

pipenv install --dev
```

## Run unit tests

```
pipenv run python -m pytest
```

Or under `pipenv shell`,

```
python -m pytest
```

## Deploy the cloudformation stacks for this lambda function to AWS

```
pipenv run bin/deploy.py
```

Or under `pipenv shell`,

```
bin/deploy.py
```

# Deployment details

The deploy script `bin/deploy.py` deploys the lambda function to AWS with below steps,

- Create the lambda package to `dist/lambda.zip` with the source code and dependencies
- Deploy the S3 bucket cloudformation stack to AWS to store the lambda package
- Upload the lambda package to the S3 bucket
- Deploy the lambda function cloudformation stack to AWS
- Update the lambda function code, so the lambda function can be updated even there is no cloudformation change
