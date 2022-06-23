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

        GraphDraw(table,AannotateList)

    def CalcEstimate(table,AannotateList,Params ):  # t=Params.trade

        t=Params.trade
        _Esti=CEsti.PASS
        t.diffC3533=(table[_c.Target][3.5]-table[_c.Target][3.3]).round(1) 
        t.diffM3533=(table[_c.item1][3.5]-table[_c.item1][3.3]).round(1)
        t.std35=table[_c.item0][3.5] #標準偏差
        t.Dev35=table[_c.item6][3.5] #標準値
        _std30=table[_c.item0][3.0] #標準偏差
        _Dev30=table[_c.item6][3.0] #標準値
        #_Dev35=t.Dev35
        _diffC3530=(table[_c.Target][3.5]-table[_c.Target][3.0]).round(1)
        
        _diffC3230=(table[_c.Target][3.2]-table[_c.Target][3.0]).round(3)
        _diffF353230=t.diffC3533-_diffC3230

        _Buy =_c.dBuy(_Dev30)
        _Sell=_c.dSell(_Dev30)

        _std32=table[_c.item0][3.2]
        _std33=table[_c.item0][3.3]
        _std35=table[_c.item0][3.5]

        _diff3532=_std35-_std32
        _diff3533=_std35-_std33
        _diff3530=_std35-_std30

        _info=f"3.0={round(_Dev30,wc.Dig)} 3.5 {round(t.Dev35,wc.Dig)} 3533M={round(t.diffM3533,wc.Dig)} 3530C={round(_diffC3530,wc.Dig)} B {round(_Buy,wc.Dig)} S {round(_Sell,wc.Dig)} std={round(_std30,wc.Dig)}"

        #前回の取引結果により処理を分岐
        _diffF353230_r0=_diffF353230.round(0)
        if(t.Result > 0 ):  # 前回 上昇
            #_ted=">=0.77"
            _tdev=">=0.087"
            _stdfiff=">=6.2"
            if( -20.0 <= _diffF353230_r0 and _diffF353230_r0 <= 20.0 ):  # 連勝したデータの集中する範囲を取る
                _Esti=CEsti.Buy
                _text=f"HN 順張りの買い {_info}"
            else:
                _Esti=CEsti.RSell
                _text=f"HR 逆張りの売り {_info}"
        else:               # 前回 下落
            #_ted="<=-0.93"
            _tdev="<=-0.065"
            _stdfiff=">=6.43"
            if( -20.0 <= _diffF353230_r0 and _diffF353230_r0 <= 20.0 ):  # 連勝したデータの集中する範囲を取る
                _Esti=CEsti.Sell
                _text=f"LN 順張りの売り {_info}"
            else:
                _Esti=CEsti.RBuy
                _text=f"LR 逆張りの買い {_info}"

        _info2=f"{'前回上昇' if t.Result > 0 else '前回下落' } {'拡散方向' if _std35 > 6.29  else '収縮方向' } TR {round(_diffF353230,wc.Dig)} TR0 {_diffF353230_r0} d3.5 {round(t.Dev35,wc.Dig)}{_tdev} std35 {round(_std35,wc.Dig)}{ _stdfiff} "
        #t.Amount=Params.Amount()
        t.Esti=_Esti
        Params.EstiMsg=[_text,_info2]
        print(f"+++ {_text} +++++")
        print(f"++++++  {_info2} +++++")
    