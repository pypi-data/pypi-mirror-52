'''
Created on 30 nov 2018

@author: giordano.zanoli84@gmail.com
'''

import time 
import copy
import functools
import logging

__all__ = ['Elapsed', 'timeit', 'logit', 'logruntime']


class Elapsed(object):
    """
    Timer class that handles various runtime calculation steps. Has several
    methods (static too) that perform some runtime calculations and 
    prettifications. 

    **Purpose**

    - defining an overall run time using the 
      ``self.stampFromStart`` method
    
    - defining a partial runtime using the ``self.stampFromBreakpoint`` 
      method. Each call to this method allows to reset the last 
      breakpoint, so that sequential calls to this method gives a series 
      of partial runtimes.
    
    - adding several named partial runtimes that measure runtime of 
      multiple steps of code 

    Attributes
    ----------
    start : float
        is the initial time.time()
    breakpoint : float
        is the current / last breakpoint time.time() 
    all_breakpoints : dict
        holds all the named breakpoints
    current_runtime : float
        seconds from instantiation
    last_breakpoint_runtime : float
        seconds from last breakpoint reset

    """
    
    def __init__(self):
        #: is the initial time.time()
        self.start = time.time()
        #: time.time() is the current / last breakpoint
        self.breakpoint = copy.deepcopy(self.start)
        #: dict, holds all the named breakpoints
        self.all_breakpoints = {'last':self.breakpoint}
        
    def __str__(self):
        return Elapsed.runtimePrinter(self.current_runtime)

    @property
    def current_runtime(self): 
        #: seconds from instantiation
        return time.time() - self.start

    @property
    def last_breakpoint_runtime(self): 
        #: seconds from last breakpoint reset
        return time.time() - self.breakpoint

    def breakpointRuntime(self, breakpoint_runtime): 
        """
        Calculate the seconds among the calling moment to a (previous) 
        time.time

        Parameters
        ----------
        breakpoint_runtime : time.time

        Returns
        -------
        float : 
            seconds from valuation instant and the input arg

        """
        return time.time() - breakpoint_runtime

    def resetLastBreakpoint(self):
        """
        Reset the last breakpoint (``self.breakpoint``) to time.time()

        Returns
        -------
        an instance of self
        """
        self.breakpoint = time.time()

    def addBreakpoint(self, name='', reset_last=True):
        """
        Add a new named breakpoint. If ``reset_last==True`` then it also reset 
        the last breakpoint 

        Parameters
        ----------
        name : str
            add a new breakpoint into the ``all_breakpoints`` dict with
            key = ``name``
        
        reset_last : bool
            reset the last breakpoint (``self.breakpoint``)
        
        Returns
        -------
        an instance of self

        """
        self.all_breakpoints[name] = time.time()
        if reset_last:
            self.resetLastBreakpoint()

    @staticmethod
    def runtimeConverter(runtime):
        """
        Static method that converts a float amount of seconds into seconds, 
        minutes, hours, days. 

        Parameters
        ----------
        runtime : float (seconds)
        
        Returns
        -------
        tuple 
            tuple of ([secs],[mins],[hours],[days])
        """
        
        seconds = runtime % 60
        
        mins_tot = runtime / 60
        minutes = int(mins_tot % 60)
        
        hours_tot = mins_tot / 60
        hours = int(hours_tot % 24)
        
        days_tot = hours_tot / 24
        days = int(days_tot)
        
        return seconds, minutes, hours, days

    @staticmethod
    def runtimePrinter(runtime):
        """
        Static method that given a runtime (float in seconds), returns a 
        formatted string of the form 'Elapsed Time: {}[days] {}[hours] {}[mins] 
        {}[secs]'

        Parameters
        ----------
        runtime : float (seconds) 
        
        Returns
        -------
        str
            string of the form 'Elapsed Time: {}[days] {}[hours] {}[mins] 
            {}[secs]'
        
        See Also
        --------
        :meth:`Elapsed.runtimeConverter`

        """
        
        seconds, minutes, hours, days = Elapsed.runtimeConverter(runtime)
        
        ret = 'Elapsed Time:'
        
        if days: ret += ' {days:n} [days]'.format(days=days)
        if hours: ret += ' {hours:n} [hrs]'.format(hours=hours)
        if minutes: ret += ' {minutes:n} [mins]'.format(minutes=minutes)
        if seconds: ret += ' {seconds:.3f} [secs]'.format(seconds=seconds)

        return ret

    def stampFromStart(self, msg='', reset_last=True):
        """
        Prettifier of runtime message. Given a string, adds the formatted 
        string in ``runtimePrinter``.

        Parameters
        ----------
        msg : str
            is the message to be printed before the current runtime 
            of the Elapsed instance

        reset_last : bool
            reset the last breakpoint (``self.breakpoint``)
        
        Returns
        -------
        str
            string given by msg + Elapsed.runtimePrinter(self.current_runtime)
        
        See Also
        --------
        :meth:`Elapsed.runtimePrinter`

        """
        if msg != '':
            ret = str(msg) + ': ' + Elapsed.runtimePrinter(self.current_runtime)
        else:
            ret = Elapsed.runtimePrinter(self.current_runtime)
        if reset_last:
            self.resetLastBreakpoint()
        return ret

    def stampFromBreakpoint(self, msg='', reset_last=True, name=''):
        """
        Prettifier of runtime message. Given a string, adds the formatted 
        string in ``runtimePrinter``.

        Parameters
        ----------
        msg : is the message to be printed before the last breakpoint runtime 
            of the ``Elapsed`` instance

        reset_last : bool 
            reset the last breakpoint (``self.breakpoint``)

        name : str 
            returns the elapsed time from the *name* breakpoint if it 
            exists, otherwise returns the elapsed time from the last one
        
        Returns
        -------
        str 
            string given by msg + 
            Elapsed.runtimePrinter(self.breakpoint_runtime)
        
        See Also
        --------
        :meth:`Elapsed.runtimePrinter`

        """
        if name == '':
            breakpoint_runtime = self.last_breakpoint_runtime
        else:
            try:
                breakpoint_runtime = self.breakpointRuntime(
                    self.all_breakpoints[name]
                )
            except KeyError:
                breakpoint_runtime = self.last_breakpoint_runtime
        if msg != '':
            ret = str(msg) + ': ' + Elapsed.runtimePrinter(breakpoint_runtime)
        else:
            ret = Elapsed.runtimePrinter(breakpoint_runtime)
        if reset_last:
            self.resetLastBreakpoint()
        return ret


def timeit(_func=None, *, msg='{}'):
    """
    This is a timer decorator with arguments.

    Parameters
    ----------
    msg : str, optional
        the message to be passed to the `Elapsed.stampFromStart` routine

    Examples
    --------
    >>> @timeit(msg='Prova')
    ... def prova():
    ...     return np.random.randn(100000)
    >>> prova()
    Prova: Elapsed Time: 0.002 [secs]

    When run with no arguments it outputs by default the class and name of
    the function:

    >>> @timeit
    ... def prova():
    ...     return np.random.randn(100000)
    >>> prova()
    prova: Elapsed Time: 0.002 [secs]

    Or:

    >>> @timeit()
    ... def prova():
    ...     return np.random.randn(100000)
    >>> prova()
    prova: Elapsed Time: 0.002 [secs]

    """
    def decorator_timeit(f):
        @functools.wraps(f)
        def wrapper_timeit(*args, **kwargs):
            timer = Elapsed()
            ret = f(*args, **kwargs)
            print(timer.stampFromStart(msg.format(f.__name__)))
            return ret
        return wrapper_timeit
    if _func is None:
        return decorator_timeit
    else:
        return decorator_timeit(_func)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
std_handler = logging.StreamHandler()
std_handler.setFormatter(log_formatter)
LOGGER.addHandler(std_handler)


def logit(_func=None, *, logger_level=LOGGER.info, msg='{}'):
    """
    This is a function decorator with arguments

    Parameters
    ----------
    logger_level : logging.Logger.level callable, default logging.Logger.info
        where the logging.Logger is set to handle the stdout

    msg : str, default None
        the string to be logged before Elapsed.stampFromStart running time

    Examples
    --------
    First of all need to create a logging.Logger instance:

    >>> import logging
    >>> logger = logging.getLogger(__name__)
    >>> logger.setLevel(logging.INFO)
    >>> log_handler = logging.FileHandler(logfilepath, 'a', 'utf8')
    >>> log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    >>> log_handler.setFormatter(log_formatter)
    >>> logger.addHandler(log_handler)
    >>> std_handler = logging.StreamHandler()
    >>> std_handler.setFormatter(log_formatter)
    >>> logger.addHandler(std_handler)

    Then decorate the function want to log in the standard fashion:
    
    >>> @logit # uses default logger to stdout
    ... def mickey(n=10000000):
    ...     return list(range(n))
    >>> a = mickey()
    2019-01-18 17:15:51 INFO: mickey: Elapsed Time: 0.192 [secs]
    >>> @logit(logger_level=logger.error) 
    ... def mickey(n=10000000):
    ...     return list(range(n))
    >>> a = mickey()
    2019-01-18 17:15:51 INFO: mickey: Elapsed Time: 0.183 [secs]

    This will redirect the logged message to both the logfilepath set in the 
    logger as well as to the stdout, as it is set in the logger.

    You can otherwise just pass a message to be printed to the stdout:

    >>> @logit(msg='MICKEY')
    ... def mickey(n=10000000):
    ...     return list(range(n))
    >>> a = MICKEY()
    2019-01-18 17:15:51 INFO: MICKEY: Elapsed Time: 0.183 [secs]

    See Also
    --------
    :meth:`timeit`

    """
    def decorator_logit(f):
        @functools.wraps(f)
        def wrapper_logit(*args, **kwargs):
            timer = Elapsed()
            ret = f(*args, **kwargs)
            try:
                logger_level(timer.stampFromStart(msg.format(f.__name__)))
            except:
                logger_level(timer.stampFromStart(msg))
            return ret
        return wrapper_logit
    if _func is None:
        return decorator_logit
    else:
        return decorator_logit(_func)


def logruntime(f_=None, *, logger_attr='params.logger',
               timer_attr='params.timer'):
    """
    This is a function decorator with arguments. Used to log methods runtime
    execution. Used in classes that have both a logger and an :meth:`Elapsed`
    instances. Notice that the info level is used.

    Parameters
    ----------
    logger_attr : str
        logging.Logger attribute name in the decorated method, used as argument
        of the getattr built-in, default 'params.logger'

    timer_attr : str
        :meth:`Elapsed` attribute name in the decorated method, used as argument
        of the getattr built-in, default 'params.timer'

    Examples
    --------
    First of all need to create a logging.Logger and an Elapsed instance:

    >>> timer = Elapsed()
    >>> logger = logging.getLogger(__name__)
    >>> logger.setLevel(logging.INFO)
    >>> formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(formatter)
    >>> logger.addHandler(handler)

    Suppose we have a Params object that collects such instances:

    >>> class Params(object):
    ...   ...  def __init__(self, logger, timer):
    ...         self.logger = logger
    ...         self.timer = timer

    Then decorate the function want to log in the standard fashion:

    >>> class ExampleWithDefault(object):
    ...     def __init__(self, params):
    ...         self.params = params
    ...     @logruntime
    ...     def mickey(self, n=10000000):
    ...         return list(range(n))
    >>> ex = ExampleWithDefault(Params(logger, timer))
    >>> ret = ex.mickey()
    2019-01-18 17:15:51 INFO: ExampleWithDefault.mickey: Elapsed Time: 0.192 [secs]

    Otherwise, if the logger and the timer are defined inside the same object:

    >>> class Example(object):
    ...     def __init__(self, logger, timer):
    ...         self.logger = logger
    ...         self.timer = timer
    ...     @logruntime(logger_attr='logger', timer_attr='timer')
    ...     def mickey(self, n=10000000):
    ...         return list(range(n))
    >>> ex = Example(logger, timer)
    >>> ex.mickey()
    2019-01-18 17:15:51 INFO: Example.mickey: Elapsed Time: 0.192 [secs]

    See Also
    --------
    :meth:`Elapsed`

    """

    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            self = args[0]

            name = type(self).__name__ + '.' + f.__name__

            def get_attr_recursive(o, attr, default=None):
                attrs = attr.split('.')
                for a in attrs:
                    o = getattr(o, a, default)
                    if not o:
                        return None
                return o

            # TODO: add try except? Here a silent pass is anyway done
            logger = get_attr_recursive(self, logger_attr, None)
            timer  = get_attr_recursive(self, timer_attr,  None)

            if logger and timer:
                timer.addBreakpoint(name=name)
                ret = f(*args, **kwargs)
                msg = timer.stampFromBreakpoint(msg=name, name=name)
                logger.info(msg)
            else:
                ret = f(*args, **kwargs)

            return ret

        return wrapper

    if f_ is None:
        return decorator
    return decorator(f_)

# TODO: timeit for functions
# TODO: timeit for methods
# TODO: logruntime for functions
# TODO: logruntime for methods
