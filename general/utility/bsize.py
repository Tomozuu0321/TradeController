from urllib3.exceptions import MaxRetryError
from data.enum import CBSize
from data.Exceptions import DriverDownException

def Get_bsize( Params,minimum):
    if( Params.PlatformName() =='Android' ):
        return(CBSize.SMALL)
    try:
        size=Params.driver.get_window_size()
        #type(size); size
        if( size['width'] > minimum ):
            return(CBSize.LARGE)
        else:
            return(CBSize.SMALL)
    except MaxRetryError as me:
        _e= DriverDownException(f'{__name__} open failed !! e:{ me }')