## About upload to lib pypi

1. The account and password was saved in .pypic.
2. Please update lib version in setup.py before upload to pypi.
3. Please do not upload unnessary file (ex: egg.info, pycache...etc).
4. `Web` : <https://pypi.org/project/AIMaker/>

## If this is the first time to upload, please execute the following
Please copy .pypic to your home directory.

`$ cp .pypic ~`

Register account info.

`$ python setup.py register -r pypi`

## Upload lib to pypi
In current directory use the following command:

`$ python setup.py sdist upload -r pypi`


## Usage
`$ pip install AIMaker`

```python
import AIMaker as ai
ai.sendUpdateRequest({result})
ai.saveValidationResult({result})
```