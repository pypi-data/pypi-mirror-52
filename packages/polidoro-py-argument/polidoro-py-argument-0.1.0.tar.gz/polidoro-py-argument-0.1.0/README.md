# Argument [![Latest](https://img.shields.io/github/release/heitorpolidoro/py-argument-utils.svg?label=latest)](https://github.com/heitorpolidoro/py-argument-utils/releases/latest)
Package to create command line arguments for Python.

#### How to use:
- Decorate the method you want to call from command line with `@Argument`.
- Create a `ArgumentParser` (from this package not from argparse)
- Call `parser.parse_args()`

All keywords arguments are the same as in [argparse.ArgumentParser.add_argument](https://docs.python.org/3.7/library/argparse.html#the-add-argument-method) except for 'action' and 'nargs'.
'action' is a custom Action created to run the decorated method and 'nargs' is the number of parameters in the decorated method. 
 
 

###### Exemples:
foo.py
```

from argument import Argument, ArgumentParser

@Argument
def bar():
    print('hi')
    
parser = ArgumentParser()
parser.parse_args()
```
Result:
```
$ python foo.py --bar
hi 
```

You can pass argument to the method
```
@Argument
def bar(baz=None):
    print(baz)
```
```
$ python foo.py --bar Hello
Hello
```


