from datetime import datetime
from dataclasses import dataclass
import pandas as pd
import copy
from data.biWconst import const as wc
from data.enum import CEvt,CEsti
#from data.environment.LivingFieldEnv.BrowserEnv import BrEmv
from data.Estimate.EstiColumns import PEstimateColumns as _c
from general.utility.logger import log
from general.utility.math import GetFutur,CalcBollingerBands
from general.data.Estimate.visualization import GraphDraw

@dataclass
class CEstimate( pd.DataFrame ):

    def copy(self):
        return(copy.copy(self))

    @classmethod
    def getTradeParams( cls,Params,_data ):
    #def getTradeParams( self,_esti,df ):
    
        _Esti=cls.CalcEstimate(None,None,Params )
        return
    
        df=Params.TradeSummary
        _key=_data['MT'][0]["Evt"]

        if( _key != CEvt.ESTI.name ):
            _text=f':CEstimate KeyError key {_key } { datetime.now() }'
            log.error(f'{_text}')
            return

        #_evt=CEvt[_name.ESTI.n]
        #print(_data)

        _e=[]
        _p=[]
        _items=_data['MT'][0][_key][0]["00"][0].split(',')
        _e.append(_items[4])
        _p.append(float(_items[5]))
        for i in range( 1,len(_data['MT'][0][_key][0]) ):
            _idx=f"{i:02d}"
            _items=_data['MT'][0][_key][0][_idx][0].split(',')
            _e.append(_items[1])
            _p.append(float(_items[2]))

        print(f" e={_e}")
        print(f" p={_p}")

        #esti=_e[0]
        #_Esti=CEsti.PASS
        #_Amount=const.Amount
        #20220617 期間を3分から2分に変更
        
        df=pd.DataFrame( [
          GetFutur(_p[3],_p[7],2),
          GetFutur(_p[3],_p[7],1),
          _p[7],_p[6],_p[5],_p[4],_p[1],_p[2],_p[3],
          GetFutur(_p[6],_p[4],1)
         ]
        #,index=[0.0,1.0,1.2,1.3,4.0,5.0,6.0]
        ,columns=[_c.Target])
        
        """
        df=pd.DataFrame( [
                  GetFutur(_p[4],_p[7],2),
                  GetFutur(_p[4],_p[7],1),
                  _p[7],_p[6],_p[5],_p[4],_p[1],_p[2],_p[3],
                  GetFutur(_p[7],_p[4],1)
                 ]
                #,index=[0.0,1.0,1.2,1.3,4.0,5.0,6.0]
                ,columns=[_c.Target])
        """

        # ボリンジャーバンドの計算
        table=CalcBollingerBands(df,_c)
        """
        table[_c.Target]= df[_c.Target]
        table[_c.item1] = df[_c.Target].rolling(window=_c.Period).mean()
        table[_c.item0] = df[_c.Target].rolling(window=_c.Period).std()
        table[_c.item2] = table[_c.item1] + (table[_c.item0] * _c.Division0)
        table[_c.item3] = table[_c.item1] - (table[_c.item0] * _c.Division0)
        table[_c.item4] = table[_c.item1] + (table[_c.item0] * _c.Division1)
        table[_c.item5] = table[_c.item1] - (table[_c.item0] * _c.Division1)
        """

        #不要な行を削除する
        table=table.round(3)
        table=table.drop(table.index[[0, 1]])
        table.reset_index(drop=True, inplace=True)

        # indexを振り直す
        table.insert(0,'id',[0.0,1.0,2.0,3.0,3.2,3.3,3.5,4])
        table.set_index('id', inplace=True)

        AannotateList=[
                [0.0,_e[7]],[1.0,_e[6]],[2.0,_e[5]],[3.0,_e[4]],[3.5,_e[2]],[3.2,_e[2]],[3.3,_e[2]]
                ]

        _Esti=cls.CalcEstimate(table,AannotateList,Params )
        #Params.trade.Amount=_Amount
        #Params.trade.Esti=_Esti

        #GraphDraw(table,AannotateList)

    def CalcEstimate(table,AannotateList,Params ):  # t=Params.trade

        t=Params.trade
        _Esti=CEsti.PASS

        #_Buy =_c.dBuy(_Dev30)
        #_Sell=_c.dSell(_Dev30)

        _df=Params.TranSummary.doDbRead(Params.Mode())
        _df=_df[( _df["Tid"] == 1 )].head(1)

        _info=""
        #f"3.0={round(_Dev30,wc.Dig)} 3.5 {round(t.Dev35,wc.Dig)} 3533M={round(t.diffM3533,wc.Dig)} 3530C={round(_diffC3530,wc.Dig)} B {round(_Buy,wc.Dig)} S {round(_Sell,wc.Dig)} std={round(_std30,wc.Dig)}"

        #_fO0=float(_df["OV"] )
        #_fC9=float(_df["CV"] )
        _Result=int(_df["Result"])

        #前回の取引結果により処理を分岐
        if( _Result > 0  ):     # 前回 上昇
            _Esti=CEsti.Buy
            _text=f"HN 順張りの買い {_info}"
        else:                   # 前回 下落
            _Esti=CEsti.Sell
            _text=f"LN 順張りの売り {_info}"

        _info2=f"{'前回上昇' if _Result > 0 else '前回下落' }"
        #f"{'前回上昇' if t.Result > 0 else '前回下落' } {'拡散方向' if _std35 > 6.29  else '収縮方向' } TR {round(_diffF353230,wc.Dig)} TR0 {_diffF353230_r0} d3.5 {round(t.Dev35,wc.Dig)}{_tdev} std35 {round(_std35,wc.Dig)}{ _stdfiff} "

        #t.Amount=Params.Amount()
        t.Esti=_Esti
        Params.EstiMsg=[_text,_info2]
        print(f"+++ {_text} +++++")
        print(f"++++++  {_info2} +++++")
    