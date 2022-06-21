from datetime import datetime
import time
import tornado.ioloop
from urllib3.exceptions import MaxRetryError
from data.enum import CEvt,CFlags,CPpsm,CPmd,CFlags
from data.biWconst import const
#from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
import general.utility.bit as Bit
from general.utility.logger import log,MatrixFunction
from general.utility.StopWatch import MatrixFunctionEx
import general.utility.bsize as bs
from data.Sounds.SoundHandler import CSoundHandler
from data.Exceptions import NotLoginException,ProcessContinuedException
from process.matrix.modules.biWinning.GetResult import GetResult
from process.matrix.modules.BrowserControl.BrowserControls import PageRefresh
from process.matrix.OnSummary import TradeSummarySetTradeResult,TranSummarySetTransaction


@TranSummarySetTransaction("OnTran1")   #トランザクションを記録する
@TradeSummarySetTradeResult("OnTran1")  #トレード結果を記録する
@MatrixFunction
def OnTran1(Params,sts,evt):

    from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
    if( BrEmv.PlatformMode != CPmd.NOSTART ):
        print(f":TRNでも取引システムと接続を試みます s:{sts} t:{type(sts)}" )
        from processor import GrProcess
        GrProcess.SetCallBack( CEvt.BOPEN,CPpsm.THREAD )
        CSoundHandler().PlaySound( const.NoticeSound )

@TranSummarySetTransaction("OnTran3")   #トランザクションを記録する
@TradeSummarySetTradeResult("OnTran3")  #トレード結果を記録する
@MatrixFunction
def OnTran3(Params,sts,evt):
    from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
    if( Params.PlatformName() == BrEmv.PlatformWindows ):
        from processor import GrProcess
        #GrProcess.SetCallBack( CEvt.BCLOSE,CPpsm.THREAD )
        pass

    print("OnTran::トランザクションの保存だけやる" )

"""
@MatrixFunction
def OnTran6(Params,sts,evt):

    _driver=Params.driver
    if(_driver==None ):
        _e=NotLoginException(f'::OnTran::取引システムと接続が切れています')
        raise _e

    #ここでトランザクションの保存処理が入る
    #多分きっとこう-> OnTran3(Params,sts,evt)

    print("OnTran::購入の事前準備を開始します" )
    from processor import GrProcess
    GrProcess.SetCallBack(CEvt.PREP_TH,CPpsm.THREAD )

"""

@TranSummarySetTransaction("OnTran2")   #トランザクションを記録する
@MatrixFunctionEx
def OnTran2(Params,sts,evt):

    @TradeSummarySetTradeResult("OnTran2")  #トレード結果を記録する
    def  __OnTran2(Params,sts,evt):

        if( Params.trade.Impossible==True ):
            print(f"::OnTran4は起動中の為 スキップします" )
            return

        try:
            #画面サイズを取得する
            Params.bsize=bs.Get_bsize(Params,const.Min)
            #print(f"1 {datetime.datetime.now()}")
            if( Params.PlatformName() =='Android' ):
                PageRefresh(Params.driver)

            Params.driver.get( const.Tranding )              # 通常２秒ほどかかる
            #time.sleep(const.Sleep)                         #これは必要なんだろうか
            Params.driver.switch_to.frame(0)

            # 購入結果取得
            _value=GetResult(Params.driver,Params.bsize,True)   #投資額チェックする
            Params.Flags=Bit.Clr(Params.Flags,CFlags.B_AMERR)

        except ProcessContinuedException as _pc:
            #二回以上は何度読んでも無駄なのでリセット
            if(Bit.Chk(Params.Flags,CFlags.B_AMERR)):
                from selenium.common.exceptions import  WebDriverException
                _we=WebDriverException( "OnTran2 Rwset Request")
                raise _we
                #from data.Exceptions import DriverDownException
                #_de= DriverDownException("OnTran2 Rwset Request")
                #raise _de
            else:
                Params.Flags=Bit.Set(Params.Flags,CFlags.B_AMERR)
                raise _pc
        except MaxRetryError as _me:
            raise _me
        except NotLoginException as _ne:
            raise _ne
        except Exception as e: # origin Exception
            _e=Exception(f'::Error by OnTran4 {e} ty:{type(e)} {e}')
            raise _e

        Params.trade.Assets=_value

        # 集計処理用の情報を設定する
        Params.trade.SummaryFlag=CFlags.SUCCESS
        #CSoundHandler().PlaySound( const.lossUpdateSound )
        print(f"::OnTran4 GetResult 実行結果 Assets={_value } {datetime.now()} -----------")

    try:
        #トレード結果集計
        __OnTran2(Params,sts,evt)
    except ProcessContinuedException:
        print(f"::__OnTran2 投資額が残っている為 事前処理を行いません" )
        return

    #購入準備の実行
    from processor import GrProcess
    GrProcess.SetCallBack(CEvt.PREP_TH,CPpsm.THREAD )
    #Params.Flags=Bit.Clr(Params.Flags,CFlags.B_DOWN)

"""
@MatrixFunctionEx
def OnTran4(Params,sts,evt):
    #from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
    from process.matrix.modules.biWinning.__OnTrade2 import __PrepareTrading
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
        Params.trade.Impossible=False
    finally:
        pass

 #トランザクションの退避
 _data=Params.Receive
 #トランザクションの復旧
 Params.Receive=_data

 if( _value == const.InvalidValue ):
     #oldAsses=0.0
     Params.trade.Impossible=True
     _text=(f'OnTrade4 残高取得失敗 {datetime.now()}')
     log.error(f'{_text} BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
     _e=NotLoginException( _text )
     raise _e
     #return

#トレード事前準備
def SetCallBack2(self,evt,MyParams,func ):
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback( func,evt,MyParams )

    #__PrepareTrading(Params,Params.driver)
    #print(f"4 {datetime.datetime.now()}")


async def __Thread_CallBack2__( evt,MyParams ) :
    log.error("Call __Thread_CallBack__!!!")
    ioloop = tornado.ioloop.IOLoop.current()
    await ioloop.run_in_executor( None,_PrepareTrading,MyParams,MyParams.driver )
"""