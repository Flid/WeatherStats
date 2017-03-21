## What Is That?
I wrote it long ago as a part of take-home test. The goal is to write an API, which calls some existing weather API and returns you some useful statistics for a given location and given period of time.
It can be used as a skeleton for a new API, it has everything you need: error handling, request form validation, response serialization, swagger documentation generator, pre-commit hooks for isort and flake8, etc.

## Installation

```
$ virtualenv ve
$ . ./ve/bin/activate
$ pip install -r requirements/<env_name>.txt
```

Setup database if needed.

Install pre-commit hooks:

```
$ ./bin/install_hooks.py
```

Run tests: 

```
$ pip install -r requirements/test.txt
$ ./run-tests.sh 
```

Run dev server:

```
$ ./run-server.sh
```

