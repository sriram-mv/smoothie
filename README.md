# smoothie [![Build Status](https://api.travis-ci.org/TheSriram/smoothie.png)](https://travis-ci.org/TheSriram/smoothie)


Installation
============


```bash
    pip install smoothie  
```


Example
========

Python Exception Based Callbacks

Add your callbacks to functions as decorators, that are slated to be called as per the Exception raised.

```python
from smoothie.king import Dispenser

def err_callback(*args, **kwargs):
    print("Error handled")

juice = Dispenser()

@juice.attach(exception=IndexError,
              callback=err_callback)
def vending_machine():
    drinks = ['Tea','Coffee', 'Water']
    return drinks[4]

vending_machine()
```


Tests
=====
To run the unit tests,

 ```bash
     pip install -r test-requirements.txt
     cd smoothie/tests
     nosetests -vs
 ```
