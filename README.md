# smoothie
Python Exception Based Callbacks

Add your Callbacks to functions as decorators, that are slated to be called as per the Exception Raised.

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

To run the unit tests,

 ```bash
 pip install -r test-requirements.txt
 cd smoothie/tests
 nosetests -vs
 ```