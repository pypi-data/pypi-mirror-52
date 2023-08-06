##  IEXWrapper
This is a simple wrapper to IEXTrading API

### Upload to PyPi
1) ```python3 setup.py sdist bdist_wheel```
2) (Optional) ```python3 -m pip install --user --upgrade twine```
3) ```python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*```
4) ```twine upload dist/*```
