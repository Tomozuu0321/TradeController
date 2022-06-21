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
    except AttributeError :
        raise MaxRetryError('Get_bsize AttributeError Reset Request')
    except MaxRetryError as mettributeError :
        raise MaxRetryError('Get_bsize MaxRetryError Reset Request')
