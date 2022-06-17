# %%
import logging
#logging.basicConfig()
from datetime import datetime
from data.enum import CSts,CEvt
from data.Param import CParam

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#logger = logging.getLogger("TradeController")
log = logging.getLogger("TradeController")

def MatrixFunction(func):

    def IsClassOK( Params ):
        _c=type(Params)
        if _c == CParam :
            return( True,f"Params OK" )
        else:
            return( False,f"Params NG {_c}" )

    def IsStsOK( Sts ):
        _c=type(Sts)
        if _c == CSts :
            return( Sts.name )
        else:
            _e=Exception(f'Func Chk::Sts Err ')
            raise _e

    def IsEvtOK( Evt ):
        _c=type(Evt)
        if _c == CEvt :
            return( Evt.name )
        else:
            _e=Exception(f'Func Chk:: Evt Err ')
            raise _e

    def inner_funcM( Params,Sts,Evt):
        #log.info( f'called {func.__name__} {IsClassOK(Params)} s:{IsStsOK( Sts )} e:{IsEvtOK(Evt)} {datetime.datetime.now()}')
        log.critical( f'called {func.__name__} {IsClassOK(Params)} s:{IsStsOK( Sts )} e:{IsEvtOK(Evt)} {datetime.now()}')
        result = func(Params,Sts,Evt)
        return result
    return inner_funcM

def MatrixSupportFunction(func):
    def IsClassOK( Params ):
        _c=type(Params)
        if _c == CParam :
            return( True,f"Params OK" )
        else:
            return( False,f"Params NG {_c}" )

    def inner_funcMx( Params,*args,**kwargs):
        squares1 = [f'{a},{type(a)}' for a in args]
        squares2 = [f'{k},{type(kwargs[k])},{kwargs[k]}'for k in kwargs]
        log.critical( f'called {func.__name__} {IsClassOK(Params)} {datetime.now()}')
        #log.critical( f'called {func.__name__} {IsClassOK(Params)}  { squares1 } { squares2 } {datetime.datetime.now()}')
        result = func(Params,*args,**kwargs)
        return result
    return inner_funcMx

def MatrixSupportClassMethod(func):
    def IsClassOK( Params ):
        _c=type(Params)
        if _c == CParam :
            return( True,f"Params OK" )
        else:
            return( False,f"Params NG {_c}" )
    def inner_funcMc( self,Params,*args,**kwargs):
        #squares1 = [f'{a},{type(a)}' for a in args]
        #squares2 = [f'{k},{type(kwargs[k])},{kwargs[k]}'for k in kwargs]
        log.critical( f'called {func.__name__} {IsClassOK(Params)} {datetime.now()}')
        result = func( self,Params,*args,**kwargs)
        return result
    return inner_funcMc

def getShortName( inpString ):
    _list=inpString.split(".")
    return(_list[len(_list)-1])

