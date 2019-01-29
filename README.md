# holding-data-publisher
A Lambda function to publish the holdings of one ETF found to SNS

## Setup project

```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user --upgrade pipenv

export PIPENV_VENV_IN_PROJECT=1

pipenv install --dev

pipenv run python main.py

pipenv run python -m pytest
```
