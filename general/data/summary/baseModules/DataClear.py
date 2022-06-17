from datetime import datetime
import numpy
from pandas._libs.tslibs.timestamps import Timestamp
from general.utility.logger import log
#from general.utility.StopWatch import StopWatch
#@StopWatch
def _DataClear(df,index):
    for _column in df.columns:
        _val=df.loc[index,_column]
        _type=type(df.loc[index,_column])
        if _type is numpy.int64 :
            df.loc[index,_column]=0
        elif _type is numpy.float64:
            df.loc[index,_column]=0.0
        elif _type is Timestamp or _type is datetime:
            df.loc[index,_column]=Timestamp(datetime.today())
        elif _type is str:
            df.loc[index,_column]="nop"
        else:
            df.loc[index,_column]=0.0

    #特例　MINPは最低利益率の為初期値を変更する
    df.loc[ index,"MinP"]=numpy.float64(100000.0)

"""
def _DataDisplay( index,df ):
    for _column in df.columns:
        _type=type(_df.loc[index,_column])
        print(_type)

#雛形作成 #1列目 当日 累計　デモとリアルで別々に持つ
def _doCreate():
    _df=pandas.DataFrame(
    #_df = CTradeSummary(
        {
            'ReqNumA':[1,10],
            'ReqNumS':[2,20],
            'ReqCont':[3,30],       # 連続数

            'ExeNumA':[4,40],
            'ExeNumS':[5,50],
            'ExeCont':[30,300],     # 連続数

            'Assets':[6.00,60.00],  # 資産
            'Profit':[7.00,70.00],  # 利益
            'loss'  :[8.00,80.00],  # 損益
            'PayMe' :[9.00,90.00],  # 収支Payments
            'Progr' :[10.00,100.00],# 勝率 Progress

            'lastUp':[datetime.now(),datetime.now()],
            'Term'  :["Term1","Term2"]
        }
        ,index=['Daily', 'Accum']
        )
    
    
    accumulative【略】Accum. Daily
    _df = CTradeSummary(
        {
        'ReqNumA':[1,10],
        'ReqNumS':[2,20],
        }
        , index=['0', '1'])

    #_df = CTradeSummary(
    #{
    #    'ReqNumA':[1,10],
    #    'ReqNumS':[2,20],
    #}
    # index=["Daily", "Accum"]
    #,index=['0', '1'])
    #
    return(_df)
"""
