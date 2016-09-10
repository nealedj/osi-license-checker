# OSI License Checker

Takes a URL to a library and tries to identify what it is licensed under.

## Usage


Full URLs:

- Github: https://osi-license-checker.appspot.com/check/github.com/nealedj/osi-license-checker
- PyPi: https://osi-license-checker.appspot.com/check/pypi.python.org/pypi/enum34
- Npm: https://osi-license-checker.appspot.com/check/www.npmjs.com/package/underscore

More concise:

- Github: https://osi-license-checker.appspot.com/check/github/nealedj/osi-license-checker
- PyPi: https://osi-license-checker.appspot.com/check/pypi/enum34
- Npm: https://osi-license-checker.appspot.com/check/npm/underscore


## Command line usage

Run `./setup.sh`

### PyPi requirements

Pipe your requirements file to the read_pypi_requirements script:

`cat requirements.txt | python scripts/read_pypi_requirements.py`

### Npm requirements

Pipe your package.json file to the read_npm_package_json script:

`cat package.json | python scripts/read_npm_package_json.py`
