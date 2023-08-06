<p align="center">
  <img alt="Image" src="https://i.imgur.com/XSacNPD.png?2"/>
</p>

[![Build Status](https://travis-ci.org/GenesisCoast/conditions-py.svg?branch=master)](https://travis-ci.org/GenesisCoast/conditions-py) [![codecov](https://codecov.io/gh/GenesisCoast/conditions-py/branch/master/graph/badge.svg)](https://codecov.io/gh/GenesisCoast/conditions-py) [![PyPI version](https://badge.fury.io/py/conditions-py.svg)](https://badge.fury.io/py/conditions-py)

# Conditions-PY

Conditions is a Python port of the famous .NET library [Conditions](https://github.com/ghuntley/conditions) which helps developers write pre- and postcondition validations in a fluent manner. Writing these validations is easy and it improves the readability and maintainability of code.

## Contents
- [Installation](#installation) 
- [Conditions](#conditions)
- [Tests](#tests)
- [Examples](#examples)
- [Acknowledgements](#acknowledgements)

## Installation

Installation is done via PIP:

    pip install conditions-py

## Conditions

A full list of all the available conditions can be found in the [Wiki](https://github.com/GenesisCoast/conditions-py/wiki).

## Tests

Currently both unit and integration tests are written using the `pytest` library. Execution of tests in Visual Studio Code is performed using the `pytest` test runner.

## Examples

```python
import conditions_py


def speak(message: str):
    Condition\
        .requires_str(message, 'message')\
        .is_not_null_or_whitespace()

    # Do speaking...


def multiple(left: int, right: int):
    Condition\
        .requires_num(left, 'left')\
        .is_positive()

    Condition\
        .requires_num(right, 'right')\
        .is_greater_than(4)
        
    # Do multiplication
    
    
def is_true(value: bool):
    Condition\
        .requires_bool(value, 'value')\
        .is_true()
        
    # Do other stuff
    
    
def animals(dog: object, cat: object):
    Condition\
        .requires_obj(dog, 'dog')\
        .is_not_null()
        
    Condition\
        .requires_obj(cat, 'cat')\
        .is_null()
        
    # Do other stuff
```

A particular validation is executed immediately when it's method is called, and therefore all checks are executed in the order in which they are written:

## Acknowledgements

- The icon "<a href="http://thenounproject.com/term/tornado/2706/" target="_blank">Tornado</a>" designed by <a href="http://thenounproject.com/adamwhitcroft/" target="_blank">Adam Whitcroft</a> from The Noun Project.
- <a href="https://github.com/ghuntley">Geoffrey Huntley (ghuntley)</a> who is the original author of "<a href="https://github.com/ghuntley/conditions">Conditions</a>" from which this project was based on.
