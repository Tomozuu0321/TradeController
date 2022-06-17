
# 
# pandas の agg 
#
#df[[].groupBy().max() min
# groupBy(,as_iindex=false )  結合する際　インデックスを追加しない
# df.applymap('{:,.0f}'),format で3桁区切り
#df[[].groupBy().max() min

from datetime import datetime
import pandas as pd
from data.enum import CFlags,CEsti
from data.biWconst import const
from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from general.utility.logger import log,getShortName
from general.utility.math import CalcPercent,CalcAverage
from general.utility.StopWatch import StopWatch
from data.Sounds.SoundHandler import CSoundHandler

#_ExeCnts=[1, -2, 1, -2]
_ExeCnts=[-1, 1]

def _SetExeCnts(self,inpNewlen):
    log.error(f" call _SetExeCnt!!! {datetime.now()}")
    _ExeCnts.clear()  # 全要素を削除
    for i in range(0,inpNewlen):
        _answer = divmod(i,2)
        if( _answer[1] ==0  ):
            _ExeCnts.append(1)
        else:
            _ExeCnts.append(-1)

def __upDateList(value):
    #log.error(f" call __upDateList!!! {datetime.now()}")
    _ExeCnts.pop(0)
    _ExeCnts.append(value)

def _isMarPossible( df,Martingale ):
    _mar = divmod(Martingale,100)
    _isPossible=_mar[0]+(_mar[1]-_mar[0])+1
    _cnt=(df.loc[ BrEmv.SummaryIndex0,"ExeCont"])*-1
    if(_cnt < _mar[0] ):
        _isPossible=0
    else:
        for _ExeCnt in _ExeCnts:
            if(( _ExeCnt*-1 ) > _mar[1] ):
                _isPossible=0

    return(_isPossible )

#@StopWatch
def _SetRequestResult(df,Params,Trn):

    #log.error(f" call {__name__}_SetRequestResult-000 {datetime.datetime.now()}")
    #log.error(f" call SetRequestResult-000 { datetime.now()}")
    #Req=Params.trade
    _Flags=Trn.SummaryFlags

    for _idx in df.index:

        #試行件数の更新
        df.loc[ _idx,"ReqNumA"]+=1

        #うち購入を成功した処理
        if( _Flags == CFlags.SUCCESS ):
            df.loc[ _idx,"ReqNumS"]+=1
            if( Trn.Esti == CEsti.PASS ):
                df.loc[ _idx,"ReqPass"]+=1

        #リクエスト成功率の計算
        df.loc[ _idx,"ReqScsPar"]=CalcPercent(  df.loc[ _idx,"ReqNumS"],df.loc[ _idx,"ReqNumA"] )

        #更新日時の設定
        df.loc[ _idx,"lastUpR"]=pd.Timestamp(datetime.now().replace(microsecond = 0))
        #df.loc[ _idx,"lastUpE"]=datetime.now().replace(microsecond = 0)

        #予測の更新
        df.loc[ _idx,"ReqEsti"]=int(Trn.Esti)

        #連続数の更新
        if( _Flags == CFlags.SUCCESS ):
            if( df.loc[ _idx,"ReqCont"] >0 ):
                df.loc[ _idx,"ReqCont"]+=1
            else:
                df.loc[ _idx,"ReqCont"]=1
        elif( _Flags == CFlags.FAILED ):
            if( df.loc[ _idx,"ReqCont"] <0 ):
                df.loc[ _idx,"ReqCont"]-=1
            else:
                df.loc[ _idx,"ReqCont"]=-1

        #連続数最大最小の更新
        if( df.loc[ _idx,"ReqContS"] > df.loc[ _idx,"ReqCont"] ):
            df.loc[ _idx,"ReqContS"] = df.loc[ _idx,"ReqCont"]
        
        if( df.loc[ _idx,"ReqContB"] < df.loc[ _idx,"ReqCont"] ):
            df.loc[ _idx,"ReqContB"] = df.loc[ _idx,"ReqCont"]

    #print(f'{getShortName(__name__)} Req成功率 {df.loc[ _idx,"ReqScsPar"].round(4)}' )

#@StopWatch
def _SetTradeResult(df,Params,Trn):

    #log.error(f" call _SetTradeResult-000 { } {datetime.now()}")
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #_text=f" call _SetTradeResult-000 W={'勝ち' if _Flag==CEsti.Win else '負け'} d:={ _diff }  A:={ _Assets } {datetime.now()}"
    _Assets=Trn.Assets

    if( df.loc[ BrEmv.SummaryIndex0,"Assets"] < _Assets ):
        _Flag=CEsti.Win
    elif ( df.loc[ BrEmv.SummaryIndex0,"Assets"] > _Assets ):
        _Flag=CEsti.Lose
    else:
        _Flag=CEsti.PASS
    
    Trn.Result=_Flag
    #df.loc[ BrEmv.SummaryIndex0 ,"Assets"]=_Assets

    if(_Flag==CEsti.PASS):
        print(f"-------------売買の結果 見送り -------------_SetTradeResult!! ")
        Params.Msg="call _SetTradeResult-000 NoTrade!!!"

    _diff=_Assets-df.loc[BrEmv.SummaryIndex0,"Assets"]
    #print(_diff)

    try:
        __SetTradeResultExeNums(df,_Flag)
        __SetTradeResultExeValues(df,_diff,_Flag)
        pass
    except Exception as e: # origin Exception
        log.error( f'{getShortName(__name__)} _SetTradeResult Error t:{type(e)} ') #e:{ e }')

    finally:
        pass
        Params.TradeSummary.doUpdate(Params.Mode())
        #log.error( f'_SetTradeResult Uodate success !!!')

    print(f"-------------売買の結果 {df.loc[ BrEmv.SummaryIndex0,'ExeCont']}連 W={'勝ち' if _Flag==CEsti.Win else '負け' if _Flag==_Flag==CEsti.Lose else '見送り'} -------------")
    print(f'-------------現在の勝敗状況  {_ExeCnts}  ---------------------------------------')
    #_text=f" call _SetTradeResult-000 W={'勝ち' if _Flag==CEsti.Win else '負け'} d:={ _diff }  A:={ _Assets } {datetime.now()}"
    _text=f"::売買の結果 {df.loc[ BrEmv.SummaryIndex0,'ExeCont']}連 W={'勝ち' if _Flag==CEsti.Win else '負け' if _Flag==_Flag==CEsti.Lose else '見送り' } \
                                    d:={ _diff }  A:={ _Assets } { datetime.now().replace(microsecond = 0) }"
                                    #d:={ _diff:0.3f }  A:={ _Assets:0.3f } { datetime.now().replace(microsecond = 0) }"
    Params.Msg=_text
    #log.error(_text)


def __SetTradeResultExeNums(df,_Flags):

    #log.error(f" call SetTradeResultExeNums-000 { datetime.now()}")

    for _idx in df.index:

        #試行件数の更新
        df.loc[ _idx,"ExeNumA"]=df.loc[ _idx,"ReqNumS"]

        #うち予測がヒットした数
        if( _Flags == CEsti.Win ):
            df.loc[ _idx,"ExeNumS"]+=1
        #うち予測が外れた数
        elif( _Flags == CEsti.Lose ):
            df.loc[ _idx,"ExeNumF"]+=1
        #うち購入を見送った数
        elif( _Flags == CEsti.PASS ):
            df.loc[ _idx,"ExeNumP"]+=1
        #のこりはエラー等の取引失敗すう（購入間に合わない、タイムアウト、約定拒否など）

        #勝率の計算
        df.loc[ _idx,"ExeScsPar"]=CalcPercent(  df.loc[ _idx,"ExeNumS"],df.loc[ _idx,"ExeNumA"] )

        #更新日時の設定
        df.loc[ _idx,"lastUpE"]=pd.Timestamp(datetime.now().replace(microsecond = 0))

        #連続数の更新
        if( _Flags == CEsti.Win ):
            if( df.loc[ _idx,"ExeCont"] >0 ):
                df.loc[ _idx,"ExeCont"]+=1
            else:
                if( _idx == BrEmv.SummaryIndex0 ):
                    __upDateList(df.loc[ _idx,"ExeCont"])   #更新あり
                df.loc[ _idx,"ExeCont"]=1
        elif( _Flags == CEsti.Lose ):
            if( df.loc[ _idx,"ExeCont"] <0 ):
                df.loc[ _idx,"ExeCont"]-=1
            else:
                if( _idx == BrEmv.SummaryIndex0 ):
                    __upDateList(df.loc[ _idx,"ExeCont"])   #更新あり
                df.loc[ _idx,"ExeCont"]=-1

        #連続数最大最小の更新
        if( df.loc[ _idx,"ExeContS"] > df.loc[ _idx,"ExeCont"] ):
            df.loc[ _idx,"ExeContS"] = df.loc[ _idx,"ExeCont"]
            CSoundHandler().PlaySound( const.lossUpdateSound )

        if( df.loc[ _idx,"ExeContB"] < df.loc[ _idx,"ExeCont"] ):
            df.loc[ _idx,"ExeContB"] = df.loc[ _idx,"ExeCont"]

        #連続数平均の更新
        df.loc[ _idx,"ExeContM"]=CalcAverage( df.loc[ _idx,"ExeContM"],df.loc[ _idx,"ExeCont"],(df.loc[ _idx,"ExeNumS"]))

    #print(f'{getShortName(__name__)} 勝率 {df.loc[ _idx,"ExeScsPar"].round(4)}' )
    pass

def __SetTradeResultExeValues(df,diff,Flag):

    #log.error(f" call SetTradeResultExeValues-000 { datetime.now()}")

    #_Assets= #日計の初期値
    #_Assets_bk=0.0
    #_diff=diff

    for _idx in df.index:

        _Assets=diff
        #print(f'idx={_idx } a={_Assets }')

        #残額の更新
        if( _idx == BrEmv.SummaryIndex1 ):
            if( diff > 50000 or diff < -50000 ):
                #if( diff > 2000 and _idx == BrEmv.SummaryIndex1 ):
                print(f"計算異常 idx={_idx} {diff} ")
            else:
                df.loc[ BrEmv.SummaryIndex1,"Assets"]+=diff
        else:
            df.loc[ _idx,"Assets"]+=diff

        #収支の更新
        df.loc[ _idx,"PayMe"]=df.loc[ _idx,"Assets"]-df.loc[ _idx,"Base"]

        #最大利益 最大損益の更新
        _key="PayMe"
        if( df.loc[ _idx,"loss"] > df.loc[ _idx,_key] ):
            df.loc[ _idx,"loss"] = df.loc[ _idx,_key]

        if( df.loc[ _idx,"Profit"] < df.loc[ _idx,_key] ):
            df.loc[ _idx,"Profit"] = df.loc[ _idx,_key]

        #利益率の更新
        df.loc[ _idx,"Progr"]=CalcPercent( df.loc[ _idx,"Assets"],df.loc[ _idx,"Base"] )
    
        #最大利益率 最大損益率の更新
        if( df.loc[ _idx,"MinP"] > df.loc[ _idx,"Progr"] ):
            df.loc[ _idx,"MinP"] = df.loc[ _idx,"Progr"]
        if( df.loc[ _idx,"MaxP"] < df.loc[ _idx,"Progr"] ):
            df.loc[ _idx,"MaxP"] = df.loc[ _idx,"Progr"]
    
        #利益率平均の更新
        df.loc[ _idx,"MidP"]=CalcAverage( df.loc[ _idx,"MidP"],df.loc[ _idx,"Progr"],(df.loc[ _idx,"ExeNumS"]))
    
        #累計用の残額を計算する
        #_diff=df.loc[ _idx,"PayMe"]
    
    pass
