#!/usr/bin/env bash
pip install --user --upgrade setuptools wheel
pip install --user --upgrade twine

python3 setup.py sdist bdist_wheel
twine upload dist/*