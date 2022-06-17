from datetime import datetime
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

def _getHtml( df,Digits):

    #df.loc["Accum","lastUp"]=None
    #df.loc["Daily","ReqNumA"]+=1
    #df.loc["Daily","Assets"]*=0.111
    #pd.to_datetime(datetime.now(),format='%H:%M')
    #print(df)
    _df=df.copy()
    #_df.insert(8,'TimeR',0)
    _df.insert(9,'TimeR',0)
    #_df.insert(25,'TimeE',0)
    _df.insert(29,'TimeE',0)
    _df.insert(31,'TimeS',0)
    _df=_df.round(Digits+2).T
    #_df=_df.round(3).T
    #_df=_df.T
    _df=_df.rename(index={'lastUpR': 'DateR'})
    _df=_df.rename(index={'lastUpE': 'DateE'})
    _df=_df.rename(index={'first'  : 'DateS'})
    #print(_df)
    #print( f'{_df.loc["Date",:]} {type(_df.loc["Date","Daily"])}')

    #for i in range(0,len(_df.loc["Date",: ])) :
    for column in _df.columns:
        val=_df.loc["DateR",column]
        if type(val) is Timestamp:
            _datetime= pd.to_datetime(val)
            _df.loc["DateR",column]=_datetime.strftime('%Y/%m/%d')
            _df.loc['TimeR',column]=_datetime.strftime('%H:%M:%d')

    for column in _df.columns:
        val=_df.loc["DateE",column]
        if type(val) is Timestamp:
            _datetime= pd.to_datetime(val)
            _df.loc["DateE",column]=_datetime.strftime('%Y/%m/%d')
            _df.loc['TimeE',column]=_datetime.strftime('%H:%M:%d')

    for column in _df.columns:
        val=_df.loc["DateS",column]
        if type(val) is Timestamp:
            _datetime= pd.to_datetime(val)
            _df.loc["DateS",column]=_datetime.strftime('%Y/%m/%d')
            _df.loc['TimeS',column]=_datetime.strftime('%H:%M:%d')

    #_df.loc['Term'].index=13
    #print( f'{_df.loc["lastUp",: ]}')
    #_df.loc['Term'].index=13
    #_df.loc['Time']=[ datetime.now().strftime('%H:%M:%S'),datetime.now().strftime('%H:%M:%S')]
    #_df.insert(0, 'Time', datetime.now().strftime('%H:%M:%S'))
    #_df.loc["lastUp","Daily" ]=f"{datetime.now():%y%m%d }" #\n{datetime.now().time:'%H:%M:%S'}"
    #_df.insert(12, 'Time', strftime('%Y/%m/%d %H:%M:%S'))
    #print( f'{_df.loc["lastUp",:"Daily"]}')
    return(_df.to_html())


"""
pd,options.disply.flort_format='{:0f}',format
                             Daily                       Accum
0 ReqNumA                           1                          10
1 ReqNumS                           2                          20
2 ReqCont                           3                          30
3 ExeNumA                           4                          40
4 ExeNumS                           5                          50
5 ExeCont                          30                         300
6 Assets                            6                          60
7 Profit                            7                          70
8 loss                              8                          80
9 PayMe                             9                          90
10 Progr                            10                         100
11 lastUp   2022-05-11 06:43:39.687000  2022-05-11 06:43:39.687000
12 Term                          Term1                       Term2
"""
