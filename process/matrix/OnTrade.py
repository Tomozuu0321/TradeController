#from datetime import datetime,time
from datetime import datetime
import time
from data.enum import CEvt,CFlags,CPpsm,CEsti,CPmd
from data.biWconst import const
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
#from data.Exceptions import DriverDownException,NotLoginException
from general.utility.logger import MatrixFunction,log
from general.utility.StopWatch import MatrixFunctionEx
#from general.data.TradeInfo import CTrade
from general.data.Estimate.modules import CEstimate

import general.utility.bit as Bit
from data.Sounds.SoundHandler import CSoundHandler
from process.matrix.OnSummary import TradeSummarySetRequestResult
from process.matrix.modules.biWinning.__OnTrade2 import __OnTrade,__OnReject

@TradeSummarySetRequestResult("OnTrade1")   #トレードリクエストを記録する
@MatrixFunction
def OnTrade1(Params,sts,evt):


    if( BrEmv.PlatformMode != CPmd.NOSTART ):
    #print(f":いまは何もしません s:{sts} t:{type(sts)}" )
        print(f":取引システムと接続を試みます s:{sts} t:{type(sts)}" )
        from processor import GrProcess
        GrProcess.SetCallBack( CEvt.BOPEN,CPpsm.THREAD )
        #CSoundHandler().PlaySound( const.NoticeSound )
        #GrProcess.SetTradeCallBack( CEvt.BOPEN )

@MatrixFunction
def OnTrade4(Params,sts,evt):

    #print(f"購入の手続きを開始します s:{sts} t:{type(sts)}" )
    from processor import GrProcess
    #GrProcess.SetCallBack(CEvt.TRADE_TH,CPpsm.THREAD )
    GrProcess.SetCallBack(CEvt.TRADE_TH,CPpsm.SINGLE )
    #GrProcess.SetTradeCallBack( CEvt.TRADE_TH )

@TradeSummarySetRequestResult("OnTrade3")   #トレードリクエストを記録する
@MatrixFunction
def OnTrade3(Params,sts,evt):

    if( Params.PlatformName() == BrEmv.PlatformWindows ):
        from processor import GrProcess
        #GrProcess.SetCallBack( CEvt.BCLOSE,CPpsm.THREAD )
        pass

    print(f":購入リクエストを破棄します s:{sts.name} e:{evt.name}" )

@TradeSummarySetRequestResult("OnTrade2")   #トレードリクエストを記録する
@MatrixFunctionEx
def OnTrade2(Params,sts,evt):

    """"
    if( evt != CEvt.TRADE_TH ):
        #print("err")
        print(f"OnTrade4 スレッド終了します s:{sts} t:{type(sts)}" )
        return
    """

    #トランザクションの退避
    if( type(Params.Receive) is dict ):
        _data=Params.Receive.copy()
    else:
        _data=Params.Receive

    #CSoundHandler().PlaySound( const.NoticeModeSound )
    _max=10
    for i in range(0,_max):
        if( Params.trade.Impossible ):
            if( i >=(_max-1)):
                print(f":: OnTrade2 事前処理が完了してない為、購入を中止します {i} {datetime.now()} " )
                Params.trade.Esti=CEsti.PASS
                return
        else:
            break
        #print("wait!!")
        time.sleep(1)

    print(f"購入の手続きを開始します {datetime.now()} s:{sts} t:{type(sts)}" )

    #トランザクションの復旧
    Params.Receive=_data

    #購入判定
    CEstimate().getTradeParams( Params,_data )
    #Params.trade.getTradeParams(_estis[0],Params.TradeSummary)

    # 見送り
    if(Params.trade.Esti==CEsti.PASS ):
        return

    #購入処理
    if(Bit.Chk(Params.Flags,CFlags.REJECT)):
        print(f"call  __OnReject {Bit.Chk(Params.Flags,CFlags.REJECT):x} ")
        Params.Flags=Bit.Clr(Params.Flags,CFlags.REJECT)
        __OnTrade(Params,Params.driver,Params.trade)
        #__OnReject(Params,Params.driver,Params.trade)
    else:
        __OnTrade(Params,Params.driver,Params.trade)

