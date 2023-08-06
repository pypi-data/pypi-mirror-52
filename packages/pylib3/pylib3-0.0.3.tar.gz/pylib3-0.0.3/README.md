# PYLIB3

- The pylib3 is a shared python library, that includes common functions
  that can be used in any python package.
- This package can be used both with python2 and python3

## Usage:
- Install the pylib3 package (inside your project virtual environment)
```
pip install pylib3
```

- To import the pylib3 package
```
import pylib3
```

- To use one of the common functions from the pylib3 package
```
from pylib3 import timer
```

## Common Functions:

```
get_version(caller, version_file)
```

Gets the version number from the version_file

param str caller: source file caller (i.e __file__)
param str version_file: a version file to get the version number from
returns (str): version number or '0.0.0' if the version_file doesn't exists

```
init_logging(log_file, verbose=False, console=False)
```

Logger initialization

param str log_file: log file name
param bool console: if set to True will print logs both to a file and to stdout (console)
param bool verbose: if set to True will print more information

```
timer(func)
```

This function used as a decorator function to print the
elapsed time of the passed function

param obj func: original function
returns (obj): wrapper function

