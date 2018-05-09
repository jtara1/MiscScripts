rm dist/ -rf
python3 setup.py sdist
twine upload dist/*
