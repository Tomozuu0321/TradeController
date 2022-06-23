from data.enum import CSts,CEvt
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.Sounds.SoundHandler import CSoundHandler
from general.utility.logger import MatrixFunction,log,getShortName
from general.utility.StopWatch import MatrixFunctionEx
from data.Exceptions import DriverDownException,NotLoginException,ProcessContinuedException
from selenium.common.exceptions import WebDriverException #,NoSuchElementException
from urllib3.exceptions import MaxRetryError,ProtocolError

@MatrixFunction
def OnAmount(Params,sts,evt):
    Params.Amount(float(Params.Receive))
def OnSound(Params,sts,evt):
    #_fileName
    _data=Params.Receive
    _key=_data['MT'][0]["Evt"]
    _fileName=_data['MT'][0][_key]
    CSoundHandler().PlaySound2( _fileName )

def OnSetLoss(Params,sts,evt):
    Params.trade.setTradeParams( Params )
    # setIsLimitOver(False)
    #print(f' OnSetLos set={Params.Loss()}')

@MatrixFunction
def OnRlist(Params,sts,evt):
    _Newlen=Params.Receive
    Params.TradeSummary.SetExeCnts(int(_Newlen))
@MatrixFunction
def OnMartin(Params,sts,evt):
    Params.Martingale(int(Params.Receive))
    #print(f'OnMartin set={Params.Martingale()}')
@MatrixFunction
def OnToA(Params,sts,evt):
    Params.PlatformName(BrEmv.PlatformAndroid)
@MatrixFunction
def OnToW(Params,sts,evt):
    Params.PlatformName(BrEmv.PlatformWindows)
@MatrixFunctionEx
def Nop(Params,sts,evt):
    log.error(f'NOP!!!NOP!!! e {evt }')
    pass
#@MatrixFunction
def Get(Params,sts,evt):
    #log.error(f'Get!!!Get!!! e {evt }')
    pass

@MatrixFunctionEx
def ConFin(Params,sts,evt):
    log.error(f'ConFin!! ConFin!! {evt }')
    pass

from process.matrix.modules.OnTimer.Timer1 import OnTimer1
from process.matrix.OnStop import OnStop
from process.matrix.OnRequest import OnRequest1
from process.matrix.modules.BrowserControl.BrowserControls import BrClose,BrOpen,BrRefresh
from process.matrix.OnOpen  import OnOpen
from process.matrix.OnClose import OnClose
from process.matrix.OnTrade import OnTrade1,OnTrade2,OnTrade3,OnTrade4
from process.matrix.OnTran import OnTran1,OnTran2,OnTran3
from process.matrix.modules.OnTran4 import OnTran4
from process.matrix.OnSummary import OnSummary1,OnSummary2,OnSummary3
from process.matrix.OnLogin import OnLoginD,OnLoginR
from process.matrix.OnVisual import OnVisual

# エラーは状態を変えない　
# INSIDEならマトリクス処理のリターンコードを使う
# NOCHGなら変更しない
# 列 ステータス
# 行 イベント
__TABLE2D__=  [
                                                    # CONNECT
    [[Get,CSts.NOCHG],      [Get,CSts.NOCHG ],      [Get,CSts.NOCHG ]],
    [[Nop,CSts.LOGIN],      [Nop,CSts.CONNECT ],    [Nop,CSts.LOGOUT ]],
    [[OnTrade1,CSts.NOCHG], [OnTrade2,CSts.CONNECT],[OnTrade3,CSts.LOGIN ]],
    [[OnTran1,CSts.LOGIN],  [OnTran2,CSts.NOCHG],   [OnTran2,CSts.LOGIN  ]],
    #[[OnTran1,CSts.LOGIN],  [OnTran2,CSts.CONNECT], [OnTran3,CSts.LOGIN ]],
    [[OnTimer1,CSts.NOCHG], [OnTimer1,CSts.NOCHG ], [OnTimer1,CSts.NOCHG ]],
]

#######@staticmethod
__TABLE1D__={

    CEvt.TO_DEMO.name:  [OnLoginD,  CSts.LOGIN],
    CEvt.TO_REAL.name:  [OnLoginR,  CSts.LOGIN],
    CEvt.TIMER.name:    [OnTimer1,  CSts.NOCHG],
    CEvt.REQU.name:     [OnRequest1,CSts.NOCHG],
    CEvt.STOP.name:     [OnStop,    CSts.NOCHG],
    CEvt.ESTI.name:     [Nop,       CSts.NOCHG],
    CEvt.OTHER.name:    [Nop,       CSts.LOGOUT],
    CEvt.TO_A.name:     [OnToA,     CSts.NOCHG],
    CEvt.TRADE_TH.name: [OnTrade4,  CSts.LOGIN],
    CEvt.PREP_TH.name:  [OnTran4,   CSts.LOGIN],
    CEvt.CON_FIN.name:  [ConFin,    CSts.LOGIN],
    CEvt.TO_W.name:     [OnToW,     CSts.NOCHG],
    CEvt.BCLOSE.name:   [BrClose,   CSts.LOGOUT],
    CEvt.REFRESH.name:  [BrRefresh, CSts.NOCHG],
    CEvt.BOPEN.name:    [BrOpen,    CSts.LOGIN],
    CEvt.CLOSE.name:    [OnClose,   CSts.LOGOUT],
    CEvt.OPEN.name:     [OnOpen,    CSts.LOGOUT],
    CEvt.SREQCLR.name:  [OnSummary1,CSts.NOCHG],
    CEvt.STRNCLR.name:  [OnSummary2,CSts.NOCHG],
    CEvt.SREQEEXCEL.name:[OnSummary3,CSts.NOCHG],
    CEvt.MART.name:     [OnMartin,  CSts.NOCHG],
    CEvt.RLIST.name:    [OnRlist,   CSts.NOCHG],
    CEvt.SETLOSS.name:  [OnSetLoss, CSts.NOCHG],
    CEvt.SOUND.name:    [OnSound,   CSts.NOCHG],
    CEvt.ViSUAL.name:   [OnVisual,  CSts.NOCHG],
    CEvt.AMOUNT.name:   [OnAmount,  CSts.NOCHG],
    CEvt.MAX.name:      [Nop,       CSts.NOCHG]
}

def __getNextStatus(TableSts,BeforeSts,MatrixSts):
    if( BeforeSts >= CSts.MAX ):
        return( CSts.LOGOUT )
    elif(TableSts==CSts.INSIDE):
        return(MatrixSts)
    elif(TableSts==CSts.NOCHG):
        return(BeforeSts)
    return(TableSts)

def MatrixHandler(owner,Params,evt):

    if evt==CEvt.NOP :
        return(True)

    _isMatrix=True
    try:
        #Params.Msg=""
        _sts=Params.sts(); _iSts=int(Params.sts())
        if( CSts.MiN >= _sts ) | ( _sts >= CSts.MAX ) :
            _isMatrix=False
        _iEvt=int(evt)
        if( CEvt.MiN >= evt)  | ( evt >= CEvt.MAX ) :
            _isMatrix=False

        _RetSts=_sts
        _TableSts=CSts.NOCHG
        if( _isMatrix ):
            #log.debug(type(evt.value))
            #マトリクス処理
            #log.error(type(Params.sts()))
            _RetSts=__TABLE2D__[_iEvt][_iSts][0](Params,_sts,evt)
            _TableSts=__TABLE2D__[_iEvt][_iSts][1]
            #log.error(f" no= {_TableSts }")
        else:
            # イベント処理(全ての状態同処理を受けつける)
            try:
                #log.error( f" evt={evt.name} {evt.value} n={CEvt.TRAN.name}")
                _RetSts=__TABLE1D__[evt.name][0](Params,_sts,evt)
                _TableSts=__TABLE1D__[evt.name][1]
                #log.error(f" no= {_TableSts }")
            except KeyError:
                log.error(" Key Error " )

        # 変数を格納
        Params.sts(__getNextStatus(_TableSts,Params.sts(),_RetSts))
        Params.evt(evt)

    #
    # 以下は通常の運用で発生するもの　基本敵に対処
    #
    except NotLoginException as ne:
        log.error( f'{getShortName(__name__)} NotLoginException catch!! e:{ ne }')
        Params.sts(CSts.LOGOUT)

    except ProcessContinuedException:
        log.error( f'{getShortName(__name__)} ProcessContinuedException catch!!' )
        pass

    except ProtocolError as _pe:
        log.error( f'{getShortName(__name__)} ProtocolError catch!!' )
        DriverErrorHandler(Params,_pe)
        pass

    except WebDriverException as we:
        log.error( f'{getShortName(__name__)} WebDriverException catch!! f:0x{Params.Flags:x}' ) #e:{ we }')
        Params.sts(CSts.LOGOUT)
        from data.enum import CFlags
        import general.utility.bit as Bit
        _FlagsBk=Params.Flags
        Params.Flags=Bit.Set(Params.Flags,CFlags.B_DOWN)

        if( Params.PlatformName() == BrEmv.PlatformWindows ):
            if(Bit.Chk(_FlagsBk,CFlags.B_DOWN)):
                try:
                    #BrClose(Params,Params.sts(),CEvt.BCLOSE)
                    #Params.driver.close()
                    Params.driver.quit()
                    pass
                except Exception : # origin Exception
                    pass
                finally:
                    pass
                    Params.driver=None
                    Params.Flags=Bit.Clr(Params.Flags,CFlags.B_OPEN)
        #DriverErrorHandler(Params,we)
        #_e=DriverDownException(f'{__name__} open failed !! e:{ type(we) }')
        #raise _e
        pass

    except DriverDownException as de:
        log.error( f'{getShortName(__name__)} DriverDownException catch!!' ) #e:{ we }')
        try:
            pass
            #Params.driver.close()
            Params.driver.quit()
            #Params.driver=None
        except Exception : # origin Exception
            pass
        Params.sts(CSts.LOGOUT)
        DriverErrorHandler(Params,de)

    except MaxRetryError as me:
        log.error( f'{getShortName(__name__)} MaxRetryError catch!!' ) #e:{ me }')
        DriverErrorHandler(Params,me)

    #
    # 以下は潜在的な処理のバグなので、なるたけ取りきる
    #

    except AttributeError as ae :
        log.error( f'{getShortName(__name__)} AttributeError catch!! t:{type(ae)} e:{ ae }')

    except UnboundLocalError as ue:
        log.error( f'{getShortName(__name__)} UnboundLocalError catch!! e:{ ue }')
        #Params.sts(CSts.LOGOUT)
        #pass

    except Exception as e: # origin Exception
        _e=Exception(f'::MatrixTable.py MatrixHandler ty:{type(e)} {e}')
        Params.e=_e
        log.error( f'{__name__} origin Exception t:{type(e)} e:{ e }')
        raise _e
        #pass

    #except NoSuchElementException as _ns:
    #log.error( f'{getShortName(__name__)} NoSuchElementException t:{type(_ns)} e:{ _ns }')
    ##raise _ns

    finally:
        # False 処理継続 True 処理終了
        #if( evt==CEvt.STOP or evt==CEvt.CLOSE ):
        if( evt==CEvt.STOP ):
            return(True)
        pass
    return(False)

    # ドライバーエラーハンドリング
def DriverErrorHandler(Params,e):
    from data.enum import CFlags
    import general.utility.bit as Bit
    Params.Flags=Bit.Set(Params.Flags,CFlags.B_DOWN)
    Params.Flags=Bit.Clr(Params.Flags,CFlags.B_OPEN)
    Params.driver=None
    Params.sts(CSts.LOGOUT)
    log.error(f"::MatrixTable.py ドライバーがダウンしています {type(e)}")
            