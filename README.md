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

