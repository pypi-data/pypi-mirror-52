pip install pypi
python setup.py register -r pypi
python setup.py sdist upload -r pypi

mypy models/account/account.py
