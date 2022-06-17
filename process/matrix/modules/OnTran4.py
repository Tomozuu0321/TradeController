from datetime import datetime
from data.enum import CEvt
from general.utility.StopWatch import MatrixFunctionEx
from process.matrix.modules.biWinning.__OnTrade1 import __PrepareTrading

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
    try:
        Params.trade.Impossible=True

        if( evt != CEvt.PREP_TH ):       # Prepare thread
            #print("err")
            print(f"OnTrade4 スレッド終了します s:{sts} t:{type(sts)}" )
            return

        #次回トレード用の準備
        #CSoundHandler().PlaySound( const.NoticeModeSound )
        print("OnTran4::購入の事前準備を開始します" )
        _Amount=Params.trade.getAmount(Params.TradeSummary,Params.Martingale(),Params)
        Params.action(_Amount[2])
        print(f"  { _Amount[0] } loss {_Amount[1]:0.3f} M: { _Amount[2] } {datetime.now().replace(microsecond = 0)} -------------")
        __PrepareTrading(Params,Params.driver,_Amount[0] )
    finally:
        Params.trade.Impossible=False
        pass
