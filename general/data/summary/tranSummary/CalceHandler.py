# 
# pandas の agg 
# 
from datetime import datetime
import pandas as pd
import pandas.tseries.offsets as offsets
from data.Estimate.EstiColumns import PEstimateColumns as _c
from general.utility.logger import log
from general.utility.StopWatch import StopWatch
from general.utility.math import CalcBollingerBands

def MakeDataFrame(_data):

  def __comp(a,b):
    if( a > b ):
      return(1)
    else:
      return(-1)

  def __tcmp(o,t) -> int:
    it=int(t)
    if o<it :
      v=it-o
      return(v)
    else:
      return(0)

  def __getVal(o,t,v1,v2 ):
      if( __tcmp(o,t) > 0 ):
          #print("cl")
          return(float(v2))
      else:
          #print("op")
          return(float(v1))

  _key=_data['MT'][0]["Evt"]
  _key

  L0=_data['MT'][0][_key][0]["00"][0].split(',')  #1M
  L1=_data['MT'][0][_key][0]["01"][0].split(',')  #10s
  L2=_data['MT'][0][_key][0]["02"][0].split(',')  #20s
  L3=_data['MT'][0][_key][0]["03"][0].split(',')  #30s
  L4=_data['MT'][0][_key][0]["04"][0].split(',')  #40s
  L5=_data['MT'][0][_key][0]["05"][0].split(',')  #50s

  _df=pd.DataFrame(
  [
    [ pd.to_datetime( L0[ 6],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),0,
        __comp(L0[16],L0[7]),
        int(L0[6][-2:]),float(L0[7]),
        int(L0[9][-2:]),float(L0[10]),
        int(L0[12][-2:]),float(L0[13]),
        int(60),float(L0[16]),
        int(L0[18][-2:]),float(L0[19]),
    ],

    #30秒足前半
    [  pd.to_datetime( L0[6],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),1,
        __comp(L3[16],L0[7]),
        int(L0[6][-2:]),float(L0[7]),
        __tcmp(0,L3[9][-2:]),
        __getVal(0,L3[9][-2:],L0[7],L3[10]),
        __tcmp(0,L3[12][-2:]),
        __getVal(0,L3[12][-2:],L0[7],L3[13]),
        int(L3[15][-2:]),float(L3[16]),
        int(L3[18][-2:]),float(L3[19]),
    ],

    #30秒足後半
    [  pd.to_datetime( L3[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),2,
        __comp(L0[16],L3[16]),
        int(L0[6][-2:]),float(L3[16]),
        __tcmp(30,L0[9][-2:]),
        __getVal(30,L0[9][-2:],L0[16],L0[10]),
        __tcmp(30,L0[12][-2:]),
        __getVal(30,L0[12][-2:],L0[16],L0[13]),
        int(L3[15][-2:]),
        float(L0[16]),
        int(L3[18][-2:]),
        float(L0[19])-float(L3[19]),
    ],

    #10秒足　19
    [  pd.to_datetime( L0[6],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),3,
        __comp(L1[16],L0[7]),
        int(L0[6][-2:]),float(L0[7]),
        __tcmp(0,L1[9][-2:]),
        __getVal(0,L1[9][-2:],L0[7],L1[10]),
        __tcmp(0,L1[12][-2:]),
        __getVal(0,L1[12][-2:],L0[7],L1[13]),
        int(L1[15][-2:]),float(L1[16]),
        int(L1[18][-2:]),float(L1[19]),
    ],
    #10秒足　20
    [  pd.to_datetime( L1[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),4,
        __comp(L2[16],L1[7]),
        int(0),float(L1[16]),
        __tcmp(10,L2[9][-2:]),
        __getVal(10,L2[9][-2:],L1[16],L2[10]),
        __tcmp(10,L2[12][-2:]),
        __getVal(10,L2[12][-2:],L1[16],L2[13]),
        int(10),float(L2[16]),
        int(10),float(L2[19])-float(L1[19]),
    ],
    #10秒足　30
    [  pd.to_datetime( L2[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),5,
        __comp(L3[16],L2[7]),
        int(0),float(L2[16]),
        __tcmp(20,L3[9][-2:]),
        __getVal(20,L3[9][-2:],L2[16],L3[10]),
        __tcmp(20,L3[12][-2:]),
        __getVal(20,L3[12][-2:],L2[16],L3[13]),
        int(10),float(L3[16]),
        int(10),float(L3[19])-float(L2[19]),
    ],
    #10秒足　40
    [  pd.to_datetime( L3[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),6,
        __comp(L4[16],L3[7]),
        int(0),float(L3[16]),
        __tcmp(30,L4[9][-2:]),
        __getVal(30,L4[9][-2:],L3[16],L4[10]),
        __tcmp(30,L4[12][-2:]),
        __getVal(30,L4[12][-2:],L3[16],L4[13]),
        int(10),float(L4[16]),
        int(10),float(L4[19])-float(L3[19]),
    ],
    #10秒足　50
    [  pd.to_datetime( L4[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),7,
        __comp(L5[16],L4[7]),
        int(0),float(L4[16]),
        __tcmp(40,L5[9][-2:]),
        __getVal(40,L5[9][-2:],L4[16],L5[10]),
        __tcmp(40,L5[12][-2:]),
        __getVal(40,L5[12][-2:],L4[16],L5[13]),
        int(10),float(L5[16]),
        int(10),float(L5[19])-float(L4[19]),
    ],
    #10秒足　60
    [  pd.to_datetime( L5[15],format='%Y.%m.%d%H:%M:%S')+offsets.Hour(6),8,
        __comp(L0[16],L5[7]),
        int(0),float(L5[16]),
        __tcmp(50,L0[9][-2:]),
        __getVal(50,L0[9][-2:],L5[16],L0[10]),
        __tcmp(50,L0[12][-2:]),
        __getVal(50,L0[12][-2:],L5[16],L0[13]),
        int(10),float(L0[16]),
        int(10),float(L0[19])-float(L5[19]),
    ],

  ]  # END
  ,columns=["dateTmp","Tid","Result","OT","Open","HT","High","LT","Low","CT","Close","VT","Volume" ])

  return(_df)

#@StopWatch
def _SetTransaction(self,Params,Trade):

  def __comp(a,b):
    if( a > b ):
      return(1)
    else:
      return(-1)

  _data=Params.Receive

  _df=MakeDataFrame(_data)
  _df.index.name="id"

  _df.insert(0,"ExeCont",Params.TradeSummary.ExeCont )
  _df.insert(0,"Result2",Trade.Result)
  _df.insert(0,"Esti",Trade.Esti)
  _df.insert(0,"hour",datetime.now().hour )

  #日付けを先頭へ
  _df.insert(0,"dateD",_df["dateTmp"])
  _df.drop( columns="dateTmp", inplace=True)

  df=self.doDbRead(Params.Mode())
  if( len(df) >0 ):
    _val=df["id"][0]
    _df.index=[_val+1,_val+2,_val+3,_val+4,_val+5,_val+6,_val+7,_val+8,_val+9 ]

  #return(_df)
  self.doDbWrite(Params.Mode(),_df)
  #辞書型で指定すると順番が書き換わってしまう為、リスト型で指定する事
  #self.doCsvWrite(Params.Mode(),_df,['dateD','Esti','Result','Assets','ExeCont'] )
  #self.doCsvWrite(Params.Mode(),_df,_df.columns.tolist())
