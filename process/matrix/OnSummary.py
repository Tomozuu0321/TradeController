from datetime import datetime
from data.enum import CFlags
from general.utility.logger import MatrixFunction,log,getShortName
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.TradeInfo import CTrade
from data.Exceptions import NotLoginException,ProcessContinuedException

def TradeSummarySetRequestResult(ownerName):
    def inner_funcTradeS1(func):
        def inner_funcTradeS2(*args,**kwargs):
            from data.Param import CParam
            Params=None
            if len(args) > 0 and type(args[0]) is CParam :
                #print(f"とれました11 {len(args)} {type(args[0])}")
                Params=args[0]
            else:
                Params=CParam()
                #print("ありませせん11" )
            try:
                Params.trade.SummaryFlag=CFlags.FAILED
                #log.critical( f'called {ownerName } in TradeSummarySetRequestResult {datetime.now()}')
                #log.critical( f'called {ownerName } in TradeSummarySetRequestResult {datetime.now()}')
                result = func(*args,**kwargs)
            except NotLoginException as _ne:
                raise _ne
            except Exception as _e: # origin Exception
                _ErrText=f'::Error by { ownerName } in TradeSummarySetRequestResult ty:{type(_e)} {_e}'
                Params.e=_e
                log.critical( _ErrText )
                raise _e
                #pass
            finally:
                #購入を記録する
                _trade=Params.trade.copy()
                Params.TradeSummary.SetRequestResult(Params,_trade)
            return result
        return inner_funcTradeS2
    return inner_funcTradeS1

def TradeSummarySetTradeResult(ownerName):
    def inner_funcTradeS1(func):
        def inner_funcTradeS2(*args,**kwargs):
            from data.Param import CParam
            Params=None
            if len(args) > 0 and type(args[0]) is CParam :
                #print(f"とれました11 {len(args)} {type(args[0])}")
                Params=args[0]
            else:
                Params=CParam()
                #print("ありませせん11" )
            try:
                Params.trade.SummaryFlag=CFlags.FAILED
                #log.critical( f'called {ownerName } in TradeSummarySetTradeResult {datetime.now()}')
                result = func(*args,**kwargs)
            except ProcessContinuedException as _pc:
                #呼び出し元で処理している為、ここはなにもしなくてよい
                raise _pc
            except NotLoginException as _ne:
                raise _ne
            except Exception as _e: # origin Exception
                _ErrText=f'::Error by { ownerName } in TradeSummarySetTradeResult ty:{type(_e)} {_e}'
                Params.e=_e
                log.critical( _ErrText )
                raise _e
                #pass
            finally:
                #取引結果を記録する
                #log.critical( f'Re2集計 { ownerName } in TradeSummarySetTradeResult {datetime.now()}')
                _trade=Params.trade.copy()
                Params.TradeSummary.SetTradeResult(Params,_trade)
                #print(f"取引結果を記録した  R:{_trade.Result} a::{_trade.Assets } e::{_trade.Esti }  {datetime.now()} aaaaaaaaaaaaa")
                #更新した処理結果を格納
                Params.trade.Result=_trade.Result   #これはここでしかわからない
            return result
        return inner_funcTradeS2
    return inner_funcTradeS1

def TranSummarySetTransaction(ownerName):
    def inner_funcTradeS1(func):
        def inner_funcTradeS2(*args,**kwargs):
            from data.Param import CParam
            Params=None
            if len(args) > 0 and type(args[0]) is CParam :
                #print(f"とれました11 {len(args)} {type(args[0])}")
                Params=args[0]
            else:
                Params=CParam()
                #print("ありませせん11" )
            try:
                Params.tran.SummaryFlag=CFlags.FAILED
                #log.critical( f'called { getShortName(ownerName) } in TranSummarySetTransaction {datetime.now()}')
                result = func(*args,**kwargs)
            except NotLoginException as _ne:
                raise _ne
            except Exception as _e: # origin Exception
                _ErrText=f'::Error by { getShortName(ownerName) } in TranSummarySetTransaction ty:{type(_e)} {_e}'
                Params.e=_e
                log.critical( _ErrText )
                raise _e
                #pass
            finally:
                #トランザクションを記録する
                #_Tra=CTrade(False,const.Amount)
                #log.critical( f'TR集計 { ownerName } in TranSummarySetTransaction {datetime.now()}')
                _tran=Params.trade.copy()
                #print(f"トランウションを記録する  R:{_tran.Result} a::{_tran.Assets } e::{_tran.Esti }  {datetime.now()} aaaaaaaaaaaaa")
                Params.TranSummary.SetTransaction(Params,_tran)
                Params.tran.SummaryFlag=CFlags.SUCCESS
            return result
        return inner_funcTradeS2
    return inner_funcTradeS1

@MatrixFunction
def OnSummary1(Params,sts,evt):
    from data.biWconst import const
    _idx=BrEmv.SummaryIndex0
    _base=const.InvalidValue
    _ExeCont=100
    if( type(Params.Receive) is list ):
        _idx=Params.Receive[0]
        _base=Params.Receive[1]
        _ExeCont=Params.Receive[2]
    Params.TradeSummary.doDataClear(_idx,_base,_ExeCont)
@MatrixFunction
def OnSummary2(Params,sts,evt):
    Params.TranSummary.doDataClear(BrEmv.SummaryIndex0)
@MatrixFunction
def OnSummary3(Params,sts,evt):
    #print( Params.TradeSummary )
    Params.TradeSummary.doEexcelWrite(Params.Mode())
