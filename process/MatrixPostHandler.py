# %%
from data.enum import CEvt
from general.utility.logger import log

# %%
#if __name__ == '__main__':
def MatrixPostHandler(Handle,Process):

    _evt=CEvt.NOP
    _isExit=False
    if Handle.request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
    
        body = Handle.get_argument('body')
        if(body=='aaa'):
            #_evt=CEvt.OTHER
            body=CEvt.STOP
            _evt=CEvt.REQU
        elif( body=='bopen'):
            _evt=CEvt.BOPEN
        elif( body=='bclose'):
            _evt=CEvt.BCLOSE
        elif( body=='todemo'):
            _evt=CEvt.TO_DEMO
        elif( body=='toreal'):
            _evt=CEvt.TO_REAL
        elif( body=='toA'):
            _evt=CEvt.TO_A
        elif( body=='toW'):
             _evt=CEvt.TO_W
        elif( body=='rexel'):
            _evt=CEvt.SREQEEXCEL # EexcelExport
        elif( body=='trnclrXXXXXXX'):
            _evt=CEvt.STRNCLR    # tranSummary Clear
        elif( body=='up'):
            _evt=CEvt.OPEN
        elif(body=='stop'):
            _evt=CEvt.STOP
            #body=CEvt.STOP
            #_evt=CEvt.REQU
        elif( body.startswith('mar')):
            strings=body.split(",")
            if( len(strings)>1 ):
                body=strings[1]
                _evt=CEvt.MART
            else:
                _evt=CEvt.POST

        elif( body.startswith('amo')):
            strings=body.split(",")
            if( len(strings)>1 ):
                body=strings[1]
                _evt=CEvt.AMOUNT
            else:
                _evt=CEvt.POST

        elif( body.startswith('loss')):
            strings=body.split(",")
            if( len(strings)>1 ):
                body=strings
                _evt=CEvt.SETLOSS
            else:
                _evt=CEvt.POST

        elif( body.startswith('rlist')):
            strings=body.split(",")
            if( len(strings)>1 ):
                body=strings[1]
                _evt=CEvt.RLIST
            else:
                _evt=CEvt.POST

        elif( body.startswith('srclr')):
        #elif( str in 'srclr' ):
            import numpy as np
            from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
            from data.biWconst import const
            strings=body.split(",")
            #print(f"{strings[1]} {type(strings[1])}")
            _mode=BrEmv.SummaryIndex0
            _value=np.float64(const.InvalidValue)
            _ExeCont=100;
            if( len(strings)>1 and strings[1]=="1" ):
                _mode=BrEmv.SummaryIndex1

            if( len(strings)>2 ):
                _value=np.float64(strings[2])
                print(f"{_value} {type(_value)}")

            if( len(strings)>3 ):
                _val=int(strings[3])
                if( -21 < _val and _val < 21 ):
                    _ExeCont=_val
                    print(f" execnt {_ExeCont} {type(_ExeCont)}")

            body=[_mode,_value,_ExeCont ]
            _evt=CEvt.SREQCLR    # tradeSummary Clear
        else :
            _evt=CEvt.POST

    _isExit=Process.MatrixPostHandler(Handle,_evt,body)
    if( _isExit ):
        len_body=0
    else:
        if(type(body) == CEvt ):
            len_body=len(type(body))
        else:
            len_body=len(body)
        #log.info(body)
        #log.info(type(body))

    return(len_body)


