# 
# pandas の agg 
# 
from datetime import datetime
import pandas as pd
from data.Estimate.EstiColumns import PEstimateColumns as _c
from general.utility.logger import log
from general.utility.StopWatch import StopWatch
from general.utility.math import CalcBollingerBands

#@StopWatch
def _SetTransaction(self,Params,Trade):

   def CreateCollection(df,Timestamp):
      _tag=str(df.index[0].round(1))
      _dic={}
      for _column in _df1.columns:
         _newCol=f'{_column}_{_tag}'
         _dic[_column]=_newCol
      _df=df.rename(columns=_dic)
      _df.insert(0,"dateD",Timestamp )
      return(_df)

   def AddCollection( df,df1,_Timestamp):
      _df3=df.copy()
      for i in range(0,len(df1.index)) :
         _df2=CreateCollection(df1[df1.index[i]:df1.index[i]],_Timestamp)
         _df3=pd.merge(_df3,_df2,on='dateD')

      #日付けを先頭へ
      _df3.drop( columns="dateD", inplace=True)
      _df3.insert(0,"dateD",_Timestamp)

      return(_df3)

   #Params.trade.table=_data['MT'][0][_key][0]
   #$Params.trade.AannotateList=_data['MT'][0][_key][1]
   _table=Params.trade.table

   if( type(_table) is not pd.DataFrame ):
      print("_SetTransaction Not ready ====v========")
      return

   #print("_SetTransaction Start !!!! ====v========")

   _df=pd.DataFrame( [Trade.Assets],columns=["Assets"])

   _df.insert(0,"ExeCont",Params.TradeSummary.ExeCont )
   #_df.insert(0,"Assets",Trade.Assets)
   _df.insert(0,"Result",Trade.Result)
   _df.insert(0,"Dev35",Trade.Dev35)
   _df.insert(0,"std35",Trade.std35)
   _df.insert(0,"diffM3533",Trade.diffM3533)
   _df.insert(0,"diffC3533",Trade.diffC3533)
   _df.insert(0,"Esti",Trade.Esti)
   _df.insert(0,"hour",datetime.now().hour )

   _Timestamp=pd.Timestamp(datetime.now().replace(second=0,microsecond=0))
   _df.insert(0,"dateD",_Timestamp )

   _df1=_table[3.0:4.0]
   _df1.insert(0,'id',[3.0,3.2,3.3,3.5,3.9])
   _df1.set_index('id', inplace=True)
   _df=AddCollection( _df,_df1,_Timestamp)

   _data=Params.Receive
   _key=_data['MT'][0]["Evt"]
   _df2=pd.DataFrame(_data['MT'][0][_key][0])

   val=float(_data['MT'][0][_key][0]["00"][0].split(',')[11])
   df2=pd.DataFrame(_table[_c.Target][0.0:3.0])
   df2.loc[4.0]=float(_data['MT'][0][_key][0]["00"][0].split(',')[11])
   table2=CalcBollingerBands(df2,_c)
   _df2=table2[4.0:4.0]

   _df=AddCollection( _df,_df2,_Timestamp)

   #_df.insert(3,"diffC3040",(_df["close_3.0"]-_df["close_4.0"])) #間違い
   _df.insert(3,"diffC4030",(_df["close_4.0"]-_df["close_3.0"]))

   df=self.doDbRead(Params.Mode())
   if( len(df) >0 ):
      _df.index={df["id"][0]+1}

   #return(_df)
   self.doDbWrite(Params.Mode(),_df)
   #辞書型で指定すると順番が書き換わってしまう為、リスト型で指定する事
   #self.doCsvWrite(Params.Mode(),_df,['dateD','Esti','Result','Assets','ExeCont'] )
   #self.doCsvWrite(Params.Mode(),_df,_df.columns.tolist())

"""
# 
# 受け取ったトランザクションをDBに書き込む旧ロジック
# 
def __SetTransaction__Old(self,Params,Trade):
    
   _data=Params.Receive

   _key=_data['MT'][0]["Evt"]

   _df=pd.DataFrame(_data['MT'][0][_key][0])

   for _column in _df.columns:
      #print(_column )
      _newComl=_df[_column][0].split(',')[0]
      _df=_df.rename(columns={ _column: _newComl })

   _df.insert(0,"ExeCont",Params.TradeSummary.ExeCont )
   _df.insert(0,"Assets",Trade.Assets)
   _df.insert(0,"Result",Trade.Result)
   _df.insert(0,"Dev35",Trade.Dev35)
   _df.insert(0,"std",Trade.std)
   _df.insert(0,"diffM3530",Trade.diffM3530)
   _df.insert(0,"diffC3530",Trade.diffC3530)
   _df.insert(0,"Esti",Trade.Esti)
   _df.insert(0,"dateD",pd.Timestamp(datetime.now().replace(second=0,microsecond=0)))

   df=self.doDbRead(Params.Mode())
   if( len(df) >0 ):
      _df.index={df["id"][0]+1}

   #from general.data.summary.TranSummary import CTranSummary
   #_df=CTranSummary(_df)

   #print(f"dfを表示します {type(_df)} {_df} ")

   #return(_df)
   self.doDbWrite(Params.Mode(),_df)
   #辞書型で指定すると順番が書き換わってしまう為、リスト型で指定する事
   self.doCsvWrite(Params.Mode(),_df,['dateD','Esti','Result','Assets','ExeCont'] )
"""
