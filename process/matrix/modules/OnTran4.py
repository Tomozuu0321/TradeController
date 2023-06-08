from datetime import datetime
from data.enum import CEvt,CFlags;
from data.Exceptions import DriverDownException,NotLoginException
from general.utility.StopWatch import MatrixFunctionEx
from general.utility.logger import log,getShortName
from process.matrix.modules.biWinning.__OnTrade1 import __PrepareTrading
import general.utility.bit as Bit

#import time
#import tornado.ioloop
#from data.enum import CEvt,CFlags,CPpsm,CPmd,CFlags
#from data.biWconst import const
#from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
#import general.utility.bit as Bit
#from general.utility.logger import log,MatrixFunction
#import general.utility.bsize as bs
#from data.Sounds.SoundHandler import CSoundHandler
#from data.Exceptions import NotLoginException,ProcessContinuedException
#from process.matrix.modules.biWinning.GetResult import GetResult
#from process.matrix.modules.BrowserControl.BrowserControls import PageRefresh
#from process.matrix.OnSummary import TradeSummarySetTradeResult,TranSummarySetTransaction
#from data.environment.LivingFieldEnv.BrowserEnv import BrEmv

@MatrixFunctionEx
def OnTran4(Params,sts,evt):
    _sts=sts
    try:
        Params.trade.Impossible=True

        if( evt != CEvt.PREP_TH ):       # Prepare thread
            #print("err")
            print(f"OnTrade4 スレッド終了します s:{sts} t:{type(sts)}" )
            return

        #次回トレード用の準備
        #CSoundHandler().PlaySound( const.NoticeModeSound )
        print("OnTran4::購入の事前準備を開始します!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
        _Amount=Params.trade.getAmount(Params.TradeSummary,Params.Martingale(),Params)
        Params.action(_Amount[2])
        print(f"  { _Amount[0] } loss {_Amount[1]:0.3f} M: { _Amount[2] } {datetime.now().replace(microsecond = 0)} -------------")
        __PrepareTrading(Params,Params.driver,_Amount[0] )

    except AttributeError as ae :
        log.error( f'::OnTran4 AttributeError catch!! t:{type(ae)} e:{ ae }')
        Params.Flags=Bit.Clr(Params.Flags,CFlags.B_OPEN)
        _e=DriverDownException(f':: OnTran4 PrepareTrading-001 failed ')
        raise _e
    except Exception as e: # origin Exception
        log.error( f'::OnTran4 Exception catch!!!!!!!!!!! t:{type(e)} e:{ e }')

    finally:
        Params.trade.Impossible=False
        pass
    