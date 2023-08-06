# Distribute Config

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Maintainability](https://api.codeclimate.com/v1/badges/c95ee137fde197b24dc1/maintainability)](https://codeclimate.com/github/Net-Mist/distribute_config/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Net-Mist/distribute_config/badge.svg?branch=master)](https://coveralls.io/github/Net-Mist/distribute_config?branch=master)
[![Build Status](https://travis-ci.org/Net-Mist/distribute_config.svg?branch=master)](https://travis-ci.org/Net-Mist/distribute_config)

A package to handle multi-source distributed configuration

This package handle the problem of multi-source configuration in python. For a python program containing a set of configuration variables,
this package will populate the values of these configuration variables by looking for a yaml configuration file, then will overwrite the values of the 
variables by looking for matching environment variables and then, if the program was started with some arguments, will once again overwrite the values of the configuration by loading these variables

Moreover, this package allow you to define configuration variables in multiple python files, using a namespace system so you can't accidentally break other parts of the configuration, so the configuration stay near the code that needs it and you can update your configuration by just importing new python files. 

## Example

Let the following python program app.py:
```python
from distribute_config import Config

Config.define_int("nb", 1, "some number")
Config.define_str_list("list", ["a", "b", "c"], "some list")
Config.define_enum("logger", "debug", ["info", "debug", "warn"], "the logger level")

Config.load_conf()
print(Config.get_dict())
```

by running it with `python app.py` it will create a file config.yml :
```yml
list:
- a
- b
- c
nb: 1
logger: debug
```

and display : `{'nb': 1, 'list': ['a', 'b', 'c'], 'logger' : 'debug'}`

Now if we update config.yml:
```yml
list:
- a
- b
nb: 2
```
- `python app.py` will print `{'nb': 2, 'list': ['a', 'b']}`
- `NB=3 python app.py` will print `{'nb': 3, 'list': ['a', 'b']}`
- `NB=3 python app.py --nb 4` will print `{'nb': 4, 'list': ['a', 'b']}`

Moreover, `python app.py --help` with display all the possible variables and useful comments

## Example 2: namespace
Let change app.py to be:
```python
from distribute_config import Config

Config.define_int("nb", 1, "some number")
with Config.namespace("set1"):
    Config.define_int("nb", 2, "some other number")
    with Config.namespace("set2"):
        Config.define_int("nb", 3, "and again")
Config.define_int("other.nb", 4, "last")        

Config.load_conf()
print(Config.get_dict())
```
Running `python app.py` will display `{'nb': 1, 'set1': {'nb': 2, 'set2': {'nb': 3}}, 'other': {'nb': 4}}`
and the created config.yml is:
```yml
nb: 1
other:
  nb: 4
set1:
  nb: 2
  set2:
    nb: 3
```

- `python app.py` will print `{'nb': 1, 'set1': {'nb': 2, 'set2': {'nb': 3}}, 'other': {'nb': 4}}`
- `SET1__SET2__NB=30 python app.py` will print `{'nb': 1, 'set1': {'nb': 2, 'set2': {'nb': 30}}, 'other': {'nb': 4}}`
- `SET1__SET2__NB=30 python app.py --set1.set2.nb=40` will print `{'nb': 1, 'set1': {'nb': 2, 'set2': {'nb': 40}}, 'other': {'nb': 4}}`


## Features
- The config support single variables (int, float, str, bool) but also list (int, float, str) and enum
- When loading configuration using Config.load_conf(), you can specify the name of the config file you want to create or load, and you can also specify if you don't want a config file to be create or if you want to update the content of the current config file (usefull when adding new features)

## Tests
nosetests -v



