
# prettimer

Is a package that gives a timer utility, with prettifiers that prompt a 
prettified runtime to the standard output.

The prettifiers are decorator functions built upon the `Elapsed` object, that 
allow either to assess the runtime of a function without having to explicitly 
call any magic, or to log a step of a process where the `logging.logger` is 
pointing to.

## Examples

Can use the the main time handler this way:

    >>> from prettimer import Elapsed
    
    >>> et = Elapsed()
    >>> # do some process in between
    >>> et.stampFromStart() # this returns a string
    'Elapsed Time: 1 [mins] 3.785 [secs]'

Otherwise, can use decorator functions:

    >>> from prettimer import timeit
    
    >>> @timeit
    ... def prova():
    ...     return np.random.randn(100000)
    >>> prova()
    prova: Elapsed Time: 0.002 [secs]
    
Full documentation can be found [here]()

# Installing prettimer

To install prettimer package, just:

    pip install prettimer

# Developing prettimer

To install prettimer along with the tools you need to develop and run tests, 
run the following in your virtual env:

    pip install -e .[dev]
    
