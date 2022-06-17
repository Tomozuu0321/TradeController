# %%
import datetime
from general.utility.logger import log

def FunctionDisplay(func):
    def inner_funcF(*args,**kwargs):
        squares1 = [f'{type(a)}' for a in args]
        squares2 = [f'{k},{type(kwargs[k])},{kwargs[k]}'for k in kwargs]
        log.info( f'called {func.__name__} { squares1 } { squares2 } {datetime.datetime.now()}')
        try:
            result = func(*args,**kwargs)
        except KeyError:
            pass
        return result
    return inner_funcF

def FunctionDisplayEx(func):
    def inner_funcFx(*args,**kwargs):
        squares1 = [f'{a},{type(a)}' for a in args]
        squares2 = [f'{k},{type(kwargs[k])},{kwargs[k]}'for k in kwargs]
        log.info( f'called {func.__name__} { squares1 } { squares2 } {datetime.datetime.now()}')
        result = func(*args,**kwargs)
        return result
    return inner_funcFx

