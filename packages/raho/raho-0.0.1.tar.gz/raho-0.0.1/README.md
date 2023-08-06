# Simple symmetric encryption built on cryptography

[![Build Status](https://travis-ci.org/abhayagiri/raho.svg?branch=master)](https://travis-ci.org/abhayagiri/raho)
[![codecov](https://codecov.io/gh/abhayagiri/raho/branch/master/graph/badge.svg)](https://codecov.io/gh/abhayagiri/raho)
[![PyPI version](https://badge.fury.io/py/raho.svg)](https://pypi.org/project/raho/)

`raho` is a simple wrapper library for the
[cryptography](https://cryptography.io/) module.

## Installation

```sh
pip install raho
```

And in your Python file:

```python
>>> import raho

```

## Usage

### With Fernets

```python
>>> fernet = raho.generate_fernet()
>>> message = raho.encrypt('he is hiding behind the rock', fernet)
>>> message
'Z0FB...'
>>> raho.decrypt(message, fernet)
'he is hiding behind the rock'

```

### With passwords

```python
>>> message = raho.encrypt_with_password('they know water', 'dragon123')
>>> raho.decrypt_with_password(message, 'dragon123')
'they know water'

```

### With key files

```python
>>> fernet = raho.generate_key_file('key-file')
>>> message = raho.encrypt_with_key_file('falcon flies at dawn', 'key-file')
>>> raho.decrypt_with_key_file(message, 'key-file')
'falcon flies at dawn'

```

### Command line

See `raho --help` for command-line usage examples.

## Development

### Environment Setup

Install `python3`, `tox`, `twine` and other dependencies:

```sh
sudo apt-get install -y curl git python3-dev python3-setuptools python3-wheel \
    tox twine

Install [pyenv](https://github.com/pyenv/pyenv-installer) (if not already
installed):

```sh
curl https://pyenv.run | bash
cat <<'EOF' >> "$HOME/.bashrc"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
source "$HOME/.bashrc"
```

Clone the source:

```sh
git clone https://github.com/abhayagiri/raho.git
cd raho
```

Install the test Python versions with `pyenv`:

```sh
for v in $(cat .python-version); do
    [ "$v" != "system" ] && pyenv install -s $v
done
```

### Commands

Test:

```sh
tox
```

Build:

```sh
python3 setup.py sdist bdist_wheel --universal
```

Test upload:

```sh
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload:

```sh
twine upload dist/*
```

Clean:

```sh
rm -rf __pycache__ .coverage .tox build coverage.xml dist *.egg-info *.pyc
```
