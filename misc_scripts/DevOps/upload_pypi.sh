rm dist/ -r
python3 setup.py sdist
twine upload dist/*
